import json
import re

with open('inverted_index.json', 'r', encoding='utf-8') as f:
    inverted_index = json.load(f)

inverted_index = {k: set(v) for k, v in inverted_index.items()}
all_docs = set(range(1, 193))

def get_docs(term):
    return inverted_index.get(term.lower(), set())

def eval_expr(expr):
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

def split_expr(expr, op):
    parts = []
    depth = 0
    start = 0
    for i in range(len(expr)):
        if expr[i] == '(':
            depth += 1
        elif expr[i] == ')':
            depth -= 1
        elif expr[i:i+len(op)] == op and depth == 0:
            parts.append(expr[start:i])
            start = i + len(op)
    if parts:
        parts.append(expr[start:])
    return parts

def balanced_parens(s):
    balance = 0
    for char in s:
        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1
            if balance < 0:
                return False
    return balance == 0

def boolean_search():
    while True:
        query = input('\nВведите запрос (или "exit" для выхода): ')
        if query.lower() == 'exit':
            break
        try:
            result = eval_expr(query)
            if result:
                print('Документы:', sorted(result))
            else:
                print('Ничего не найдено.')
        except Exception as e:
            print(f'Ошибка: {e}')

if __name__ == '__main__':
    boolean_search()
