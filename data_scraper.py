#url-s
# https://www.youtube.com/watch?v=ZJ-jI6i1kzo (Sen. Cassidy reacts to RFK Jr.'s changes to the CDC website)
# https://www.youtube.com/watch?v=1ZYbU82GVz4 (Flying: Relaxing Sleep Music for Meditation, Stress Relief & Relaxation by Peder B. Helland)

from youtube_comment_downloader import YoutubeCommentDownloader
import pandas as pd
import itertools

# For generating the comment id
import random
import string
ID_LENGHT = 8

def download(url ,limit=500):
    dowloader = YoutubeCommentDownloader()
    print(f" Begin download from {url}...\n")

    CommentGenerator = dowloader.get_comments_from_url(url, sort_by=1)

    text = []

    for i in itertools.islice(CommentGenerator, limit):
        text.append(i['text'])

    print(f"{len(text)} has been downloaded!\n")
    return text

def generate_id():
    id = ''.join(random.choices(string.ascii_letters + string.digits, k = ID_LENGHT))
    return id


url_toxic = 'https://www.youtube.com/watch?v=ZJ-jI6i1kzo'
url_non_toxic = 'https://www.youtube.com/watch?v=1ZYbU82GVz4'

good_comments = download(url_toxic, limit=500)
bad_comments = download(url_non_toxic, limit=500)
#ADD COMMENTARY ID USING A RANDOM FUCNTION
good_soup = [{'COMMENT_ID': generate_id(), 'TEXT': comentariu, 'IS_TOXIC': 'BLANK'} for comentariu in bad_comments]
bad_soup = [{'COMMENT_ID': generate_id(), 'TEXT': comentariu, 'IS_TOXIC': 'BLANK'} for comentariu in good_comments]

dataset_final = bad_soup + good_soup

df = pd.DataFrame(dataset_final)

df = df.sample(frac=1).reset_index(drop=True)

fileName = 'final_dataset.csv'
df.to_csv(fileName, index=False, encoding='utf-8-sig')

print(f"\n {fileName} file has been created with {len(df)} comments in it!\n")
#AFTER RUNNING THIS FILE, RUN THE main.py TO MAKE FURTHER PROCESSING ON THE final_dataset.csv
#AN TRAINING THE MODEL