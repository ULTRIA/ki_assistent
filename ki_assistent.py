import speech_recognition as sr
import pyttsx3
import wikipedia
import wolframalpha
import sys

# Initialisiere die Sprachengine
engine = pyttsx3.init()

def sprich(text):
    """Spricht den gegebenen Text aus."""
    engine.say(text)
    engine.runAndWait()

def hoere(sprache='de-DE'):
    """Nimmt Spracheingaben über das Mikrofon auf und gibt den erkannten Text zurück."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Ich höre...")
        audio = recognizer.listen(source)
    try:
        befehl = recognizer.recognize_google(audio, language='de-DE')
        print(f"Du sagtest: {befehl}")
        return befehl.lower()
    except sr.UnknownValueError:
        print("Entschuldigung, ich habe dich nicht verstanden.")
        sprich("Entschuldigung, ich habe dich nicht verstanden.")
        return ""
    except sr.RequestError:
        print("Sprachdienst nicht verfügbar.")
        sprich("Sprachdienst nicht verfügbar.")
        return ""



def wiki_suche(begriff):
    """Sucht nach dem Begriff auf Wikipedia und gibt eine Zusammenfassung zurück."""
    wikipedia.set_lang('de')
    try:
        ergebnis = wikipedia.summary(begriff, sentences=2, auto_suggest=False, redirect=True)
        print(ergebnis)
        sprich(ergebnis)
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"Mehrdeutige Anfrage: {e.options}")
        sprich("Es gibt mehrere Möglichkeiten. Bitte sei spezifischer.")
    except wikipedia.exceptions.PageError:
        sprich("Ich konnte keine Informationen zu diesem Thema finden.")
    except Exception as e:
        print(f"Fehler: {e}")
        sprich("Es ist ein Fehler aufgetreten.")

# Initialisiere den WolframAlpha-Client
wolfram_client = wolframalpha.Client('2PQWQP-HQXT6572H4')  # Ersetze durch deinen API-Schlüssel

def wolfram_suche(frage):
    """Stellt eine Anfrage an WolframAlpha und gibt die Antwort zurück."""
    try:
        res = wolfram_client.query(frage)
        if res['@success'] == 'true':
            # Antwort aus den Ergebnissen extrahieren
            antwort = next(res.results).text
            print(antwort)
            sprich(antwort)
        else:
            sprich("Entschuldigung, ich konnte keine Antwort finden.")
    except StopIteration:
        sprich("Ich konnte keine Antwort finden.")
    except Exception as e:
        print(f"Fehler bei der WolframAlpha-Anfrage: {e}")
        sprich("Es gab ein Problem bei der Verarbeitung deiner Anfrage.")

def gesichtserkennung():
    """Startet die Gesichtserkennung."""
    import cv2
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Kamera konnte nicht geöffnet werden.")
        sprich("Kamera konnte nicht geöffnet werden.")
        return

    while True:
        ret, img = cap.read()
        if not ret:
            print("Frame konnte nicht gelesen werden.")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow('Gesichtserkennung', img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:  # Drücke 'ESC' zum Beenden
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    sprich("Willkommen. Wie kann ich dir helfen?")
    aktuelle_sprache = 'de-DE'  # Standardmäßig Deutsch
    while True:
        befehl = hoere()
        if befehl == "":
            continue
        if 'beenden' in befehl:
            sprich("Auf Wiedersehen!")
            sys.exit()
        elif 'suche nach' in befehl:
            begriff = befehl.replace('suche nach', '').strip()
            wiki_suche(begriff)
        elif 'berechne' in befehl:
            frage = befehl.replace('berechne', '').strip()
            wolfram_suche(frage)
        elif 'starte gesichtserkennung' in befehl:
            sprich("Starte die Gesichtserkennung.")
            gesichtserkennung()
        elif 'wechsel sprache zu englisch' in befehl:
            sprich("Wechsle die Sprache zu Englisch.")
            aktuelle_sprache = 'en-US'
        elif 'wechsel sprache zu deutsch' in befehl:
            sprich("Wechsle die Sprache zu Deutsch.")
            aktuelle_sprache = 'de-DE'
            
        else:
            sprich("Entschuldigung, das habe ich nicht verstanden.")
            elif 'starte gesichtserkennung' in befehl:
    sprich("Starte die Gesichtserkennung.")
    gesichtserkennung()
else:
    antwort = chatbot.get_response(befehl)
    sprich(str(antwort))


import cv2

import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def gesichtserkennung():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow('img', img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:  # Drücke 'ESC' zum Beenden
            break

    cap.release()
    cv2.destroyAllWindows()

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot('Assistent')
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.german')
