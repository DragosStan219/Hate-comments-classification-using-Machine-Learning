from flask import Flask, request, render_template
import joblib
import pandas as pd
import random

app = Flask(__name__)

# --- 1. Încărcăm Modelele ---
print("⏳ Se încarcă modelele și baza de date...")
try:
    model = joblib.load('toxic_model.pkl')
    vectorizer = joblib.load('tfidf_vectorizer.pkl')
    print("✅ Modele încărcate.")
except:
    print("❌ EROARE: Nu găsesc 'toxic_model.pkl'. Rulează antrenarea mai întâi!")
    exit()

# --- 2. Încărcăm și Procesăm CSV-ul ---
try:
    # Citim fișierul tău
    df = pd.read_csv("final_dataset.csv", encoding='utf-8-sig') # Sau 'latin-1' dacă dă eroare
    
    # Ne asigurăm că avem coloana de text (o redenumim dacă e cazul)
    # În fișierul tău pare să fie 'TEXT' cu litere mari
    if 'TEXT' in df.columns:
        col_text = 'TEXT'
    elif 'text' in df.columns:
        col_text = 'text'
    else:
        # Dacă nu găsește, luăm prima coloană care pare a fi text
        col_text = df.columns[1] 

    # --- PASUL NOU: ETICHETARE AUTOMATĂ ---
    # Deoarece fișierul nu are etichete (label), le generăm acum!
    print("⚙️ Se analizează comentariile din CSV (poate dura câteva secunde)...")
    
    # Transformăm toate textele în numere
    toate_textele = df[col_text].astype(str).fillna("")
    X_toate = vectorizer.transform(toate_textele)
    
    # Modelul decide care sunt toxice (1) și care nu (0)
    df['label_predis'] = model.predict(X_toate)
    
    print(f"Done! We analyzed {len(df)} comments and prepared them for a demo.")

except Exception as e:
    print(f"❌ EROARE la citirea CSV: {e}")
    # Creăm un set de date gol de avarie
    df = pd.DataFrame(columns=[col_text, 'label_predis'])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def actiune():
    try:
        tip_buton = request.form['buton_apasat']
        text_ales = ""
        
        # Folosim coloana noastră nouă 'label_predis' pentru filtrare
        if tip_buton == 'toxic':
            # Extragem doar ce a crezut modelul că e TOXIC (1)
            comentarii_toxice = df[df['label_predis'] == 1]
            
            if not comentarii_toxice.empty:
                text_ales = comentarii_toxice[col_text].sample(1).values[0]
            else:
                text_ales = "We haven't found a toxic example in folder!"
                
        else:
            # Extragem doar ce a crezut modelul că e SAFE (0)
            comentarii_safe = df[df['label_predis'] == 0]
            
            if not comentarii_safe.empty:
                text_ales = comentarii_safe[col_text].sample(1).values[0]
            else:
                text_ales = "We haven't found a safe example in folder!"

        # --- RE-VERIFICARE (Doar pentru show) ---
        # Îl mai trecem o dată prin model ca să afișăm rezultatul
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

if __name__ == "__main__":
    app.run(debug=True)
