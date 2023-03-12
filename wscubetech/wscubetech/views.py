from django.http import HttpResponse
from django.shortcuts import render
import string
from django.conf import settings
from django.core.files import File
import os
from collections import Counter
import matplotlib.pyplot as plt

from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


def homePage(request):
    data = {
        'title': 'Home Page',
        'heading': 'Welcome to Wscubetech'
    }
    return render(request, "index.html", data)


def calculator(request):
    c = ""
    try:
        if request.method == "POST":
            n1 = eval(request.POST.get('num1'))
            n2 = eval(request.POST.get('num2'))
            opr = request.POST.get('opr')
            if opr == "+":
                c = n1+n2
            elif opr == "-":
                c = n1-n2
            elif opr == "*":
                c = n1*n2
            elif opr == "/":
                c = n1/n2
    except:
        c = "invalid opr..."
    print(c)
    return render(request, "calculator.html", {'c': c})


def sentimental(request):
    file_path = os.path.join(
        settings.BASE_DIR, 'C:/django-projects/wscubetech/static/test.txt')
    with open(file_path, 'r',  encoding='utf-8') as f:
        file_contents = f.read()
        lower_case = file_contents.lower()
        cleaned_text = lower_case.translate(
            str.maketrans('', '', string.punctuation))

        # normal previos
        # tokenized_words = cleaned_text.split()

        tokenized_words = word_tokenize(cleaned_text, "english")

        # normal previos
        # stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
        #             "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
        #             "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these",
        #             "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
        #             "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
        #             "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
        #             "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
        #             "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
        #             "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
        #             "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

        final_words = []
        for word in tokenized_words:
            if word not in stopwords.words('english'):
                final_words.append(word)

        lemma_words = []
        for word in final_words:
            word = WordNetLemmatizer().lemmatize(word)
            lemma_words.append(word)

        emotion_list = []
        emotion_path = os.path.join(
            settings.BASE_DIR, 'C:/django-projects/wscubetech/static/emotions.txt')

        with open(emotion_path, 'r') as file:
            for line in file:
                clear_line = line.replace("\n", '').replace(
                    ",", '').replace("'", '').strip()
                word, emotion = clear_line.split(':')

                if word in lemma_words:
                    emotion_list.append(emotion)

        print(emotion_list)
        w = Counter(emotion_list)
        print(w)

        
        def sentiment_analyse(sentiment_text):
            result = ""
            score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
            if score['neg'] > score['pos']:
                print("Negative Sentiment")
                result = "Negative Sentiment"
            elif score['neg'] < score['pos']:
                print("Positive Sentiment")
                result = "Positive Sentiment"
            else:
                print("Neutral Sentiment")
                result = "Neutral Sentiment"
            return result

        result = sentiment_analyse(cleaned_text)
        # Plotting the emotions on the graph

        fig, ax1 = plt.subplots()
        ax1.bar(w.keys(), w.values())
        fig.autofmt_xdate()
        plt.savefig('graph.png')
        # plt.show()

        data = {
            'result': result
        }
    return render(request, "sentimental.html", data)
