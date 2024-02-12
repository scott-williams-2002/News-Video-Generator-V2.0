from bs4 import BeautifulSoup
import requests, json, lxml

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
        # Get the urls of the images.
        image_urls = [image['src'] for image in images]
        if len(image_urls) == 0:
            return []
        return image_urls
    #if error, return empty list
    except:
        return []

