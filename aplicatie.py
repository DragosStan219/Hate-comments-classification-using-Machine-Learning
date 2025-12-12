from flask import Flask, request, render_template
import joblib
import pandas as pd
import random

app = Flask(_name_)

print(" Loading models and dataset...")
try:
    model = joblib.load('toxic_model.pkl')
    vectorizer = joblib.load('tfidf_vectorizer.pkl')
    print(" Modes loaded.")
except:
    print("ERROR: We can't find 'toxic_model.pkl'. Run main.py first!")
    exit()

try:
    df = pd.read_csv("final_dataset.csv", encoding='utf-8-sig') 
    
    if 'TEXT' in df.columns:
        col_text = 'TEXT'
    elif 'text' in df.columns:
        col_text = 'text'
    else:
        col_text = df.columns[1] 

    print("Analysing comments from CSV...")
    
    toate_textele = df[col_text].astype(str).fillna("")
    X_toate = vectorizer.transform(toate_textele)
    
    df['label_predis'] = model.predict(X_toate)
    
    print(f"Done! We analyzed {len(df)} comments and prepared them for a demo.")

except Exception as e:
    print(f"ERROR at reading CSV: {e}")
    df = pd.DataFrame(columns=[col_text, 'label_predis'])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def actiune():
    try:
        tip_buton = request.form['buton_apasat']
        text_ales = ""
        
        if tip_buton == 'toxic':
            comentarii_toxice = df[df['label_predis'] == 1]
            
            if not comentarii_toxice.empty:
                text_ales = comentarii_toxice[col_text].sample(1).values[0]
            else:
                text_ales = "We haven't found a toxic example in folder!"
                
        else:
            comentarii_safe = df[df['label_predis'] == 0]
            
            if not comentarii_safe.empty:
                text_ales = comentarii_safe[col_text].sample(1).values[0]
            else:
                text_ales = "We haven't found a safe example in folder!"

        text_vectorizat = vectorizer.transform([str(text_ales)])
        rezultat = model.predict(text_vectorizat)[0]
        
        if rezultat == 1:
            mesaj = " MODEL RESULT: TOXIC"
            clasa_css = "toxic-result"
        else:
            mesaj = " MODEL RESULT: NON-TOXIC"
            clasa_css = "safe-result"
            
        return render_template('index.html', 
                               text_simulat=text_ales, 
                               prediction_text=mesaj, 
                               clasa=clasa_css)
                               
    except Exception as e:
        return f"Application Error : {e}"

if _name_ == "_main_":
    app.run(debug=True)
