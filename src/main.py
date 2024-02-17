from image_filtering.Image_Filter import Image_Filter
from script_generation.gpt_handler import *
from web_scraping.article_contents import *
from web_scraping.embed import *
from web_scraping.url_source import *
from web_scraping.vector_db import *
from user_interface.user_input import *
from browser_bot.bot import *
from text_to_speech.tts_handler import generate_speech

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

# since the length of script is one longer (due to hook statement) than the number of chunks from database, need to restructure data
def concat_data(db_data, script):
    #data will be returned as a list of dictionaries
    output_data = []
    output_data.append({'script_chunk': script[0], 'source_text': "", 'publisher':"", 'url':""}) #since this is a tagline no associated sources included

    # remove first element from script
    script = script[1:len(script)]

    #len script and len db_data are the same now
    for chunk in range(len(script)):    
        #indexes accompanying data from database data and script data
        script_chunk = script[chunk]
        article_text_chunk = db_data['text'][chunk]
        source_publisher = db_data['source'][chunk]
        link = db_data['url'][chunk]

        output_data.append({'script_chunk': script_chunk, 'source_text': article_text_chunk, 'publisher':source_publisher, 'url':link})
    
    return output_data  #returns a list of dictionaries

#takes in a list of dictionaries corresponding to chunks of script and appends image urls to each chunk
def add_image_urls(script_data, n_images):
    for dict in script_data:
        
        search_query = suggest_images(dict['script_chunk'])
        print(f"Searching for images of: {search_query}")
        print("Opening Chrome DO NOT PRESS BUTTONS OR MOVE MOUSE PLEASE <<<-------------")
        time.sleep(random.randrange(5,10))
        dict['images'] = get_images_from_google(search_query,n_images)

    return script_data




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
    print("query to DB complete")
    script_list = generate_article(output_data_structure['text'], "news about iran and how it affects shipping in the oceanls")
    print("finished script")
    cleaned_output = concat_data(output_data_structure, script_list) #combines both outputs into one standard data structure
    print("cleaned the data")
    cleaned_output = add_image_urls(cleaned_output,1) # 1 image per chunk

    #adding speech files to output directory and saving their location in cleaned_output
    cleaned_output = generate_speech(cleaned_output)


    
    
    

    print(cleaned_output)

    





if __name__ == '__main__':
    main()