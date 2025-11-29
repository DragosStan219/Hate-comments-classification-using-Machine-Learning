#url-s
# https://www.youtube.com/watch?v=ZJ-jI6i1kzo (Sen. Cassidy reacts to RFK Jr.'s changes to the CDC website)
# https://www.youtube.com/watch?v=cmnru0H1JlI (Geneva hosts Ukraine talks as Trump pushes peace plan | BBC News)

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

# Click on the comments section to load comments
time.sleep(10)  # Wait for page load
driver.find_element_by_name('yt-button-shape').click()


# Scroll to load comments
time.sleep(8)  # Wait for page load
for _ in range(5):  # Scroll down 5 times
    driver.execute_script("window.scrollBy(0, 500)")
    time.sleep(4)  # Wait for comments to load

    wait = WebDriverWait(driver,10)
    comments_section = wait.until(EC.presence_of_element_located((By.TAG_NAME, "ytd-comments")))

# Find comment elements (YouTube structure may vary)
comment_blocks = driver.find_elements(By.TAG_NAME, "ytd-comment-thread-renderer")

for comment in comment_blocks:
    author = comment.find_element(By.ID,"author-text").text
    text = comment.find_element(By.ID, "content-text").text

# Save to CSV
df = pd.DataFrame(comment)
df.to_csv('youtube_comments.csv', index=False, encoding='utf-8')
print(f"Scraped {len(comment)} comments")

driver.quit()