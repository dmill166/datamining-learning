# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 23: Illustrates Language Detection

from langdetect import detect

if __name__ == "__main__":

    text = [
        "Hello, how are you doing?", 
        "Olá, como vai você?", 
        "¿Hola, cómo estás?", 
        "Hallo, wie geht's dir?",
        "Привет, как дела?",
        "Bonjour comment vas-tu?"
    ]

    # TODO: classify the sentences based on their language
    langs = [0 for _ in range(len(text))]
    i = 0
    for sentence in text:
        langs[i] = detect(sentence)
        i += 1
    print (langs)



