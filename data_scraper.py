#url-s
# https://www.youtube.com/watch?v=ZJ-jI6i1kzo (Sen. Cassidy reacts to RFK Jr.'s changes to the CDC website)
# https://www.youtube.com/watch?v=cmnru0H1JlI (Geneva hosts Ukraine talks as Trump pushes peace plan | BBC News)

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Browser User Agent
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}

# Setup Selenium Chrome driver
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={headers["User-Agent"]}')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://www.youtube.com/watch?v=ZJ-jI6i1kzo"
driver.get(url)

# Scroll to load comments
time.sleep(3)  # Wait for page load
for _ in range(5):  # Scroll down 5 times
    driver.execute_script("window.scrollBy(0, 3000)")
    time.sleep(2)  # Wait for comments to load

# Extract comments from HTML
soup = BeautifulSoup(driver.page_source, 'html.parser')
comments = []

# Find comment elements (YouTube structure may vary)
comment_containers = soup.find_all('ytd-comment-thread-renderer')

for comment in comment_containers:
    comments.append({
        'text': comment.get_text(strip=True),
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    })

# Save to CSV
df = pd.DataFrame(comments)
df.to_csv('youtube_comments.csv', index=False, encoding='utf-8')
print(f"Scraped {len(comments)} comments")

driver.quit()