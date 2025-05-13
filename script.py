import nltk
nltk.download ('punkt')
nltk.download ('punkt_tab')
nltk.download('advanced_perceptron_tagger')
nltk.download ('stopwords')
nltk.download ('wordnet')
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import streamlit as st
import speech_recognition as sr

with open('eifel_tower_elevator.txt', 'r', encoding='utf-8') as f:
    data = f.read().replace('\n', ' ')

sentences = sent_tokenize(data)

def preprocess (sentences):
    words= word_tokenize(sentences)
    words= [word.lower() for word in words if word.lower() not in stopwords.words('english') and word not in string.punctuation]
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return words

corpus = [preprocess (sentence) for sentence in sentences]


def get_most_relevant_sentences(query):
    query = preprocess(query)
    max_similarity = 0
    most_relevant_sentence = ""

    for sentence in corpus:
        similarity = float(len(set(query).intersection(sentence))) / float(len(set(query).union(sentence)))
        if similarity > max_similarity:
            max_similarity = similarity
            most_relevant_sentence = " ".join(sentence)
    
    return most_relevant_sentence

def chatbot(question):
    most_relevant_sentence = get_most_relevant_sentences(question)
    return most_relevant_sentence

def transcribe_speech():

    r= sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Speak now ...")

        audio_text = r.listen(source)
        
        st.error("Could not hear you!... Maybe an issue with the microphone ?")

        st.info("Transcribing...")

        try:
            text = r.recognize_google(audio_text)
            return text
        except:
            return "Sorry, I did not get that."


def main():
    st.title('Chatbot Checkpoint')
    st.write("Hello! Am a chatbot, Ask me anything about the Elevator in the Eifel Tower.")

    st.write("The checkpoint trained based on this text file: https://gutenberg.org/ebooks/32282 ")

    

    st.write("Write your question or speak to the microphone ...")

    if st.button("Ask your question through the mic"):
        text = transcribe_speech()
        st.write("Your question ", text)
        response = chatbot(text)
        st.write("Chatbot: " + response)

    question = st.text_input("You:")

    if st.button("Submit written question"):
        response = chatbot(question)
        st.write("Chatbot: " + response)

if __name__ == "__main__":
    main()




