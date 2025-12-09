#Load the required packages (you need to face them downloaded on your device to work)
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Load the dataset
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

# Fill BLANK values in final_dataset.csv with predictions
ds_with_predictions = ds.copy()
# Predict labels for rows with BLANK values
mask = ds_with_predictions['label'].isna() | (ds_with_predictions['label'] == 'BLANK')
if mask.any():
    # Get the indices of rows with BLANK values
    blank_indices = ds_with_predictions[mask].index
    # Vectorize the text for prediction
    X_blank = tfidf.transform(ds_with_predictions.loc[blank_indices, 'TEXT'].fillna(''))
    # Get predictions
    predictions = model.predict(X_blank)
    # Fill the BLANK values with predictions
    ds_with_predictions.loc[blank_indices, 'label'] = predictions

# Save the updated dataset
ds_with_predictions.to_csv("final_dataset.csv", index=False)



