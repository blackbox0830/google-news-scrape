import feedparser
import gspread
from oauth2client.service_account import ServiceAccountCredentials
 
url = 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp0Y1RjU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en' 
feed = feedparser.parse(url) 
 
news_results = []

for el in feed.entries: 
    news_results.append({
        "link": el.link,
        "title": el.title,
        "date": el.published,
        "source": el.source.title
    })

scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
]

file_name = 'secure-wonder-427419-i0-ff51cf840c02.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
client = gspread.authorize(creds)

sheet = client.open('cryil-news').sheet1

# Function to check if a news item already exists in the Google Sheet
def news_exists_in_sheet(news):
    existing_news = sheet.findall(news["link"])  # Assuming "link" is a unique identifier
    return len(existing_news) > 0

# Function to add new news item to the Google Sheet
def add_news_to_sheet(news):
    sheet.append_row([news["link"], news["title"], news["date"], news["source"]])

# Check each scraped news item and add to Google Sheet if it doesn't already exist
for news_item in news_results:
    if not news_exists_in_sheet(news_item):
        add_news_to_sheet(news_item)
        print(f"Added news: {news_item['title']}")
