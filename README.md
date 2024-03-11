This Repository builds on the work done in the News-Video-Generator, allowing for prompt-based Tiktok/Instagram automation. First, it scrapes the internet for recent news based on a topic, finds associated articles, and loads vector embedded, semantically similar chunks, into a vector database hosted on Pinecone. This allows for a semantic search to source only the most relevant chunks of information to include in the video. Through clever prompt engineering, and a varitey of calls to the GPT-4 API, a video script is constructed piece by piece, while storing associated information's source (in the form of a link to the article). This script is then used to generate a narration, utilizing a custom Text-To-Speech API, hosted on Google Cloud. Sections of the script are then passed into GPT-3.5 Turbo, via the API, in order to extract propper nouns which are mentioned. These propper nouns are very important as they allow for an efficient way to source images via google search, which is automated using selenium. 

Once all of the images are downloaded, the video generation piece of the program begins by pulling what I call a "white noise" video (typically video game footage or scenes from a movie) in order to display at the bottom of the video. Based on research I have performed, it appears there is a high correlation between viewer retention and including white noise videos in short form content, hopefully boosting the liklihood of a video, or account going viral, hence increasing the potential for advertising revenue. This "white noise" video is resized to perfectly fit at the bottom 25 percent of a 16:9 aspect ratio screen. The images are then displayed and removed sequentially based on their location relative to which piece of news information is being mentioned. After all of the pieces needed for the video are gathered and organized, the video is rendered, completing the process. 

Check out some demos on my Instagram accounts:
(Disclaimer - All of the opinions presented in these videos are based off of the source articles (and not my own) if an opion is presented.)

In my 3rd Iteration, I intend on polishing many of the features utilized in this repository, and adding a realistic AI "Anchor", hopefully to capitalize on the novelty aspect of AI Avatars.
World News Daily: https://www.instagram.com/world._news_daily/
Tech News Daily: https://www.instagram.com/tech._news_daily/

Improvements for V3:
    - Add transitions and audio clips to image swaps__
    - Add background audio (news theme)__
    - Better prompt engineering to avoid redundant information being displayed__
    - Implement OpenAI Vision API to validate images__
    - Improve time complexity overall__
    - Host Wav2Lip Model on Google Cloud App Run and set up API (for AI "Anchor")__
    - Optimize GPT API Costs__
    - Investigate storing text embeddings locally to avoid Vector DB Costs in the future__
    - Use pandas DataFrame instead of generic list of dictionaries__
    
    













Get sentence by sentence text chunks



#For Windows Users, install ImageMagick if not already installed to prevent issues with text
