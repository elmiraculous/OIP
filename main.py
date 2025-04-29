from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os
from typing import Set, Dict
from pydantic import BaseModel

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

with open('inverted_index.json', 'r', encoding='utf-8') as f:
    inverted_index_data = json.load(f)

inverted_index: Dict[str, Set[int]] = {k: set(v) for k, v in inverted_index_data.items()}
all_docs = set(range(1, 193))

class SearchRequest(BaseModel):
    query: str

class SearchResponse(BaseModel):
    success: bool
    results: list[int] = []
    count: int = 0
    error: str = ""

def get_docs(term: str) -> Set[int]:
    return inverted_index.get(term.lower(), set())

def balanced_parens(s: str) -> bool:
    balance = 0
    for char in s:
        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1
            if balance < 0:
                return False
    return balance == 0

def split_expr(expr: str, op: str) -> list[str]:
    parts = []
    depth = 0
    start = 0
    op_len = len(op)
    for i in range(len(expr)):
        if expr[i] == '(':
            depth += 1
        elif expr[i] == ')':
            depth -= 1
        elif expr[i:i+op_len] == op and depth == 0:
            parts.append(expr[start:i])
            start = i + op_len
    if parts:
        parts.append(expr[start:])
    return parts

def eval_expr(expr: str) -> Set[int]:
    expr = expr.strip()
    
    if expr.startswith('(') and expr.endswith(')') and balanced_parens(expr[1:-1]):
        return eval_expr(expr[1:-1])
    
    for op in [' OR ', ' AND ']:
        parts = split_expr(expr, op)
        if parts:
            sets = [eval_expr(p) for p in parts]
            return set.union(*sets) if op == ' OR ' else set.intersection(*sets)
    
    if expr.startswith('NOT '):
        return all_docs - eval_expr(expr[4:])
    
    return get_docs(expr)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/search")
async def search(search_request: SearchRequest) -> SearchResponse:
    try:
        result = eval_expr(search_request.query)
        return SearchResponse(
            success=True,
            results=sorted(result),
            count=len(result)
        )
    except Exception as e:
        return SearchResponse(
            success=False,
            error=str(e)
        )

@app.get("/page/{page_id}")
async def get_page(page_id: int):
    page_path = f"pages/page_{page_id}.html"
    if os.path.exists(page_path):
        return FileResponse(page_path)
    return {"error": "Page not found"}, 404

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)