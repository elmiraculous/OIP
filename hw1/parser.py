import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL='https://ya-uznayu.ru/'


def get_category():
    res=requests.get(BASE_URL)
    soup=BeautifulSoup(res.text,'html.parser')
    soup.find_all('a', class_='categir-img')
    category_links=[]
    for i in soup.find_all('div', class_="categir-img"):
        link=i.find('a').get('href')
        full_url = urljoin(BASE_URL, link)
        category_links.append(full_url)
    return category_links
def get_info(category_links):
    info_link=[]
    for category_url in category_links:
        page=0
        max_page=1
        while page//10+1<=max_page:
            res2 = requests.get(category_url + '?start=' + str(page))
            soup2=BeautifulSoup(res2.text,'html.parser')
            links=soup2.find_all('a', class_="readMore")
            for link in links:
                link=link.get('href')
                info_link.append(link)
            pagination = soup2.find_all('a', class_='pagenav') 
            pages = [int(p.text.strip()) for p in pagination if p.text.strip().isdigit()]
            page=page+10
            max_page=max(pages) if pages else 1
    return info_link
        

def download(info_link):
    with open("index.txt", "w", encoding="utf-8") as index_file:
        for i in range(len(info_link)):
            full_url = urljoin(BASE_URL, info_link[i])
            res = requests.get(full_url)
            filename='pages/page_'+ str(i+1)+'.html'
            with open(filename, 'w', encoding="utf-8") as file:
                file.write(res.text)

            index_file.write(str(i+1)+ " "+ str(full_url)+'\n')

def main():
    category_links = get_category()
    info_link = get_info(category_links)
    download(info_link)

if __name__ == "__main__":
    main()