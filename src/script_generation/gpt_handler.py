from script_generation.GPT_Wrapper import GPT_Wrapper


def generate_hook_statement(text_chunk_list, research_question):
    gpt = GPT_Wrapper()
    article_chunks = " ".join(text_chunk_list)
    #prompt says to make a hook based on text chunks and research question
    prompt = [
        {"role": "system", "content": "You are a television news editor. Given a large collection of text, you accurately write content to engage the viewer by conveying the importance of the news being reported and how the events that occured can impact the viewer."},
        {"role": "user", "content": f"Here is the topic of the news today and the task: {research_question}. Write between 1 and 2 sentences in this style: Breaking News! If you are a [blank] type of person or if you live in [blank], you should do [blank], since [blank] events have happened. Fill in those blanks based on this text:{article_chunks}. Always begin with Breaking News"}
    ]

    return gpt.model_call_text(prompt=prompt, temp=0.4)

def generate_article(text_chunk_list, research_question):
    #first generates the hook then goes through remainer of text chunks from there
    script_hook = generate_hook_statement(text_chunk_list, research_question)
    script_chunks = []
    gpt = GPT_Wrapper()
    #iterate trough text_chunk_list
    for i in range(len(text_chunk_list)):
        previous_chunk = ""
        if i == 0:
            previous_chunk += script_hook
        else:
            previous_chunk += script_chunks[i-1] 

        #prompted on article text, research question, and previous text chunk
        prompt = [
        {"role": "system", "content": "You are a television news editor. You are given a few sentences of text which you should summarize. Summary should tie into what you previously wrote and sound fluid. You always report the real news, so do not make anything up."},
        {"role": "user", "content": f"Here is the topic of the news today and the task: {research_question}. Write between 1 and 2 sentences which summarize this chunk of text from a fellow news writer: {text_chunk_list[i]}. The summary you make will come after these sentences that you previously wrote: {previous_chunk}."}
        ]
        #append output of model to list
        script_chunks.append(gpt.model_call_text(prompt=prompt, temp=0.4))

    #retuns the hook added in front of the rest of the script's chunks
    return [script_hook] + script_chunks 

#returns a list of google search queries for each text chunk in the same order to search for images later
def suggest_images(script_chunks):
    image_suggestions = []
    gpt = GPT_Wrapper()
    for chunk in script_chunks:
        prompt = [
        {"role": "system", "content": "You are a google search pro editing a video. You come up with the best possible google search to find an image to put in your video, if that image is related to a piece of text from the video's script. The google search should be no more than 3 words long and it should be something that you would type into the search bar."},
        {"role": "user", "content": f"Here is the chunk from the video script: {chunk}. Prepare a google search query for an image that would convey the meaining of the text from the video script. The query should be no more than 3 words. Do not include quotation marks"}
        ]
        image_suggestions.append(gpt.model_call_text(prompt=prompt, temp=0.9))
    return image_suggestions





