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

def review_input(request):
    # file_path = os.path.join(
    #     settings.BASE_DIR, 'C:/django-projects/wscubetech/static/test.txt')
    # with open(file_path, 'r',  encoding='utf-8') as f:
    #     file_contents = f.read()
    text = 'good hotel'
    try:
        if request.method == "POST":
            text = request.POST.get('review')
    except:
        text = "awesome hotel"
    file_contents = text
    lower_case = file_contents.lower()
    cleaned_text = lower_case.translate(
        str.maketrans('', '', string.punctuation))

    tokenized_words = word_tokenize(cleaned_text, "english")

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
