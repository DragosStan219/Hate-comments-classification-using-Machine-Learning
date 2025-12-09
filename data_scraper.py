#url-s
# https://www.youtube.com/watch?v=ZJ-jI6i1kzo (Sen. Cassidy reacts to RFK Jr.'s changes to the CDC website)
# https://www.youtube.com/watch?v=1ZYbU82GVz4 (Flying: Relaxing Sleep Music for Meditation, Stress Relief & Relaxation by Peder B. Helland)

from youtube_comment_downloader import YoutubeCommentDownloader
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Browser User Agent
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}


url = "https://www.youtube.com/watch?v=ZJ-jI6i1kzo"
page = requests.get(url, headers=headers)
print(page.text)

#Pulling the information from raw HTML code
soup = BeautifulSoup(page.text, 'html.parser')
print(soup.prettify())

#Extract specific data (where the information matters)
quotes = []
quote_boxes = soup.find_all('div', class_='style-scope ytd-comment-thread-renderer')
for box in quote_boxes:
    quote_text = box.img['alt'].split(" #")
    quote = {
        'theme': box.h5.text.strip(),
        'image_url': box.img['src'],
        'lines': quote_text[0],
        'author': quote_text[1] if len(quote_text) > 1 else 'Unknown'
    }
    quotes.append(quote)
# Display extracted quotes
for q in quotes[:5]:  # print only first 5 for brevity
    print(q)
