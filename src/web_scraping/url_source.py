import requests
from bs4 import BeautifulSoup
import requests, json, lxml

#This function returns a list of urls given a query
def get_urls_from_google(query):
  #alert user
  print(f"Gathering Articles for the query: {query}")
  page_limit = 10          
  page_num = 0
  data = []
  params = {"q": query, "hl": "en", "gl": "us", "start": 0}

  headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"}

  while True:
    page_num += 1
    html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
    soup = BeautifulSoup(html.text, 'lxml')
    #dont understand this stuff but helps get links associated
    for result in soup.select(".tF2Cxc"):
        title = result.select_one(".DKV0Md").text
        links = result.select_one(".yuRUbf a")["href"] 
        #appends the assicated data in a json format
        data.append(links)
    # stop loop due to page limit condition
    if page_num == page_limit:
        break
    # stop the loop on the absence of the next page
    if soup.select_one(".d6cvqb a[id=pnnext]"):
        params["start"] += 10
    else:
        break
  return data

