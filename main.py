from PIL import Image
import pytesseract
import nltk
from deep_translator import GoogleTranslator
from gtts import gTTS
from nltk.sentiment import SentimentIntensityAnalyzer
import re
import pyttsx3
nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    sentiment = sia.polarity_scores(text)
    return sentiment

def preprocess_text(text, remove_tone_marks=True, remove_punctuation=True):
    if remove_tone_marks:
        text = remove_tone_marks_func(text)
    if remove_punctuation:
        text = remove_punctuation_func(text)
    return text

def remove_tone_marks_func(text):
    # Replace tone marks with empty string
    text = re.sub(r'[\u0300-\u036f]', '', text)
    return text

def remove_punctuation_func(text):
    # Remove punctuation marks
    text = re.sub(r'[^\w\s]', '', text)
    return text

def text_to_speech(text, lang, save_path, sentiment_score, voice_gender):
    # Create a pyttsx3 engine instance
    engine = pyttsx3.init()

    # Set the voice gender
    voices = engine.getProperty('voices')
    if voice_gender == 'female':
        engine.setProperty('voice', voices[1].id)  # Use a female voice
    elif voice_gender == 'male':
        engine.setProperty('voice', voices[0].id)  # Use a male voice

    # Set the speech speed based on sentiment score
    if sentiment_score >= 0.5:
        # Positive sentiment - increase speech speed
        speed = 1.5
    elif sentiment_score <= -0.5:
        # Negative sentiment - decrease speech speed
        speed = 0.5
    else:
        # Neutral sentiment - standard speech speed
        speed = 1.0
    engine.setProperty('rate', speed * 175)  # Adjust the rate as needed
    # Set the volume based on sentiment score
    volume = 0.8 + (sentiment_score - 0.5) * 0.4  # Adjust the volume range as needed
    engine.setProperty('volume', volume)  # Adjust the volume as needed

    # Save the speech as an audio file
    engine.save_to_file(text, save_path)
    engine.runAndWait()

def translate_text(text, target_language):
    translated_text = GoogleTranslator(source='auto', target=target_language).translate(text)
    return translated_text

# Set the path to Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\obezkoro\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='ukr')
    return text

image_path = r"C:\Users\obezkoro\Desktop\РМ\b9a5b48aaf075ada5469c6f89d466c8a.jpg"
extracted_text = extract_text_from_image(image_path)

print(extracted_text)

english_text = translate_text(extracted_text, 'english')
print(english_text)

german_text = translate_text(extracted_text, 'german')
print(german_text)

sentiment_translated_german_text = analyze_sentiment(german_text)
print(sentiment_translated_german_text)

sentiment_translated_english_text = analyze_sentiment(english_text)
print(sentiment_translated_english_text)

audio_file_path_de = r"C:\Users\obezkoro\Desktop\РМ\output_de.mp3"
text_to_speech(german_text, 'de', audio_file_path_de, sentiment_translated_german_text['compound'], "male")

audio_file_path_en = r"C:\Users\obezkoro\Desktop\РМ\output_en.mp3"
text_to_speech(english_text, 'en', audio_file_path_en, sentiment_translated_english_text['compound'], "female")

