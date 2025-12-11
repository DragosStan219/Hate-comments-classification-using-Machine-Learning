#Load the required packages (you need to face them downloaded on your device to work)
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Load the dataset
try:
    ds = pd.read_csv("final_dataset.csv", encoding='utf-8-sig')
except:
    ds = pd.read_csv("final_dataset.csv")

# Clean the dataset
clean_dataset = ds.dropna()

toxic_keywords = [
    'clown', 'stupid', 'idiot', 'bullshit', 'whack', 'lie', 'liar', 'crazy', 
    'mental', 'unfit', 'joke', 'trash', 'dumb', 'disgusting', 'hypocrite',
    'useless', 'nonsense', 'terrible', 'horrible', 'worst', 'kill', 'die', 
    'racist', 'sexist', 'shame', 'shut up', 'fake', 'hate', 'coward', 'spineless',
    'scum', 'propaganda', 'weak', 'pathetic', 'moron', 'fuck', 'kys'
]

ds['label'] = ds['TEXT'].apply(lambda x: 1 if any(k in str(x).lower() for k in toxic_keywords) else 0)

# Vectorize
tfidf = TfidfVectorizer(stop_words='english', max_features=1000)
X = tfidf.fit_transform(ds['TEXT'].fillna(''))
y = ds['label']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Get the indices for train/test split
train_indices = y_train.index
test_indices = y_test.index

# Create separate CSV files for training and testing data
train_data = ds.loc[train_indices].copy()
test_data = ds.loc[test_indices].copy()

train_data.to_csv("train_dataset.csv", index=False)
test_data.to_csv("test_dataset.csv", index=False)

# Training procedure
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate
print(classification_report(y_test, model.predict(X_test)))

ds_final = ds.copy()

# Organize data in csv
def creareCSVFinal(valoare):
    if valoare == 1:
        return "TOXIC"
    else:
        return "NON-TOXIC"
    
ds_final['IS_TOXIC'] = ds_final['label'].apply(creareCSVFinal)

# Remove the label column from csv
ds_final = ds_final.drop(columns=['label'])

# Save final results in an external csv file
ds_final.to_csv("rezultate_model.csv", index=False, encoding='utf-8-sig')
