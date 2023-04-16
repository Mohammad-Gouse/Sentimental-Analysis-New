from django.http import HttpResponse
from django.shortcuts import render, redirect
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

from review.models import Review

from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.db.models import Q
from django.db import connection
from django.core.paginator import Paginator

def signupPage(request):
    if request.method=='POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1 != pass2:
            return HttpResponse("Your password and confirm passoword are not Equal!!")
        else:  
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')
    return render(request, "signup.html")

def loginPage(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            name = user.username
            request.session['username'] = name
            return render(request, "home.html", {'name':name})
        else:
            return HttpResponse("username or password is incorrect!!")
    return render(request, "login.html")

@login_required(login_url="login")
def home(request):
    return render(request, "home.html")

def review_input(request):
    name = request.session.get('username')
    queryData = Review.objects.raw("SELECT * FROM review_review where user_name = %s order by id desc", [name])

    text = ''
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
        checkEmoji = ""
        score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
        if score['neg'] > score['pos']:
            print("Negative Sentiment")
            checkEmoji = "sad"
        elif score['neg'] < score['pos']:
            print("Positive Sentiment")
            checkEmoji = "happy"
        else:
            print("Neutral Sentiment")
            checkEmoji = "smile"
        return checkEmoji

    checkEmoji = sentiment_analyse(cleaned_text)
    # Plotting the emotions on the graph

    fig, ax1 = plt.subplots()
    ax1.bar(w.keys(), w.values())
    fig.autofmt_xdate()
    plt.savefig('graph.png')
    # plt.show()

    if checkEmoji == "happy":
        result = "Positve"
    elif checkEmoji == "smile":
        result = "Neutral"
    elif checkEmoji == "sad":
        result = "Negative"

    paginator = Paginator(queryData, 3)
    page_number = request.GET.get('page')
    pageDataFinal=paginator.get_page(page_number)
    totalPage = pageDataFinal.paginator.num_pages
    data = {
        'result': result,
        'checkEmoji': checkEmoji,
        'name': name,
        # 'q': queryData
        'q': pageDataFinal,
        'lastpage':totalPage,
        'totalPageList':[n+1 for n in range(totalPage)]
    }
    if request.method=="POST":
        user_name = request.session.get('username')
        description = request.POST.get('review')
        response = result
        r = Review(user_name=user_name, description = description, response=response)
        r.save()
    return render(request, "sentimental.html", data)
    # return render(request, "review_collection.html", data)

def logoutPage(request):
    logout(request)
    return redirect('login')

def Delete_record(request,id):
    a=Review.objects.get(pk=id)
    a.delete()
    return redirect('sentiment')

def reviewCollection(request):
    return render(request, 'review_collection.html')