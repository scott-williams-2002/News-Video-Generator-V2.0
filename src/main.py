from image_filtering.Image_Filter import Image_Filter
from script_generation.gpt_handler import *
from web_scraping.article_contents import *
from web_scraping.embed import *
from web_scraping.url_source import *
from web_scraping.vector_db import *
from user_interface.user_input import *

def load_all_data(db,queries):
    for query in queries:
        article_urls = get_urls_from_google(query)
        # get text chunk list for each url
        for url in article_urls:
            article_publisher = get_article_publisher(url)
            article_text_list = get_article_text(url)
            #add text chunks to vector database
            for article_text in article_text_list:
                db.populate(embed_string(article_text),article_text=article_text, article_source=article_publisher, article_url=url)
def main():
    #user input 
    research_question = get_research_question_from_user()
    queries = get_queries_from_user()

    #instantiate vector db
    db = Vector_DB()
    db.create_database()
    #load_all_data(db,queries)

    #output has a dictionary of lists - one for text chunks, one for urls, and one for publisher
    output_data_structure = db.make_query(embed_string("why is iran a threat"), 3)
    script_list = generate_article(output_data_structure['text'], "what is occuring between the United States and Iran currently")

    #add section to output of query for images
    output_data_structure['img'] = []
    #first check if possible to get images from article
    for url in output_data_structure['url']:
        output_data_structure['img'].append(get_article_images(url))

    #now that we have the urls, filter them and update with only the best
    

    print(output_data_structure)

    





if __name__ == '__main__':
    main()