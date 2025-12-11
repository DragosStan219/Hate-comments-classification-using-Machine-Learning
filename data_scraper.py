from youtube_comment_downloader import YoutubeCommentDownloader
import pandas as pd
import itertools

def descarca(url ,limita=500):
    dowloader = YoutubeCommentDownloader()
    print(f" Starting download from: {url} ...")

    generatorComentarii = dowloader.get_comments_from_url(url, sort_by=1)

    text = []

    for i in itertools.islice(generatorComentarii, limita):
        text.append(i['text'])

    print(f" Done! We downloaded {len(text)} comements.")
    return text

url_toxic = 'https://www.youtube.com/watch?v=ZJ-jI6i1kzo'
url_non_toxic = 'https://www.youtube.com/watch?v=1ZYbU82GVz4'

comentarii_rele = descarca(url_toxic, limita=500)
comentarii_bune = descarca(url_non_toxic, limita=500)

dataset_rau = [{'text': comentariu, 'eticheta': 1} for comentariu in comentarii_rele]
dataset_bun = [{'text': comentariu, 'eticheta': 0} for comentariu in comentarii_bune]

dataset_final = dataset_rau + dataset_bun

df = pd.DataFrame(dataset_final)

df = df.sample(frac=1).reset_index(drop=True)

numeFisier = 'datasetFinal.csv'
df.to_csv(numeFisier, index=False, encoding='utf-8-sig')
