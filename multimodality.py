import sys
from yt_transcript import get_yt_transcript
from website_scraper import get_website_information

if len(sys.argv) != 3:
    raise Exception("Invalid number of arguments given.")

if sys.argv[1] == "youtube":
    youtube_link = sys.argv[2]
    text = get_yt_transcript(youtube_link)  
    print(text)

elif sys.argv[1] == "website":
    website_link = sys.argv[2]
    text = get_website_information(website_link)
    print(text)
else:
    raise Exception("Invalid flag given.")
