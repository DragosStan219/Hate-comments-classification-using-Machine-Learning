#url
# https://www.youtube.com/watch?v=ZJ-jI6i1kzo (Sen. Cassidy reacts to RFK Jr.'s changes to the CDC website)
# https://www.youtube.com/watch?v=cmnru0H1JlI (Geneva hosts Ukraine talks as Trump pushes peace plan | BBC News)

from bs4 import BeautifulSoup
import requests

url = 'https://www.youtube.com/watch?v=ZJ-jI6i1kzo'
page = requests.get(url)

#Pulling the information from URL
soup =  BeautifulSoup(page.text, 'html')
print(soup)