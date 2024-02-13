from bs4 import BeautifulSoup
import requests, json, lxml
import newspaper

#given a url, a list of text chunks are returned
def get_article_text(URL):
    # Send an HTTP GET request to the URL
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'lxml')
        all_text = []
        # Find news articles using article tags or other relevant tags
        for p_element in soup.find_all('p'):
            if(len(p_element.text) != 0 ):
                all_text.append(p_element.text)
        return all_text
    #if error with getting article url return empty list
    except:         
        return []


#given a url, a list of all images are returned
def get_article_images(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all images on the page.
        images = soup.find_all('img')
        # Get the urls of the images into a list
        image_urls = []
        for image in images:
            try: #handles the case where no src element to access 
                image_urls.append(image['src'])
            except:
                continue
        if len(image_urls) == 0:
            return []
        return image_urls
    #if error, return empty list
    except:
        return []

#uses newspaper library to get the article's publisher
def get_article_title(url):
    try:
        article = newspaper.Article(url)
        return article.source_url.split('/')[2] #returns www.forbes.com for example from url
    except:
        return "Anonymous Source" # says anonymous source if can't find the publisher
