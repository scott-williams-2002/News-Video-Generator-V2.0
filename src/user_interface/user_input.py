
#simple function to get the research question from user using terminal input
def get_research_question_from_user():
    research_question = str(input("Enter a research question for the video: "))
    return research_question

#simple functino to get possible queries from the user
def get_queries_from_user():
    print("Enter possible queries to find sources related to the research question")
    print("Once you are done, enter 'q' or 'quit")

    queries = []
    continue_prompting_user = True
    while continue_prompting_user:
        query = str(input("Enter a query to add or quit: "))
        if (query.lower() == "q" or query.lower() == "quit"):
            print("Searching for articles: \n")
            break
        else:
            queries.append(query)

    return queries