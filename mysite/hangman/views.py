
import random

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Scoreboard



# Create your views here.
def index(request):
    global username
    if(request.method == "POST"):
        data = request.POST
        if(data.get('inputName') == ""):
            return
        username = data.get('inputName')
    if(request.method == 'GET'):
        username = "noUser"
    context = {}
    template = loader.get_template('index/index.html')
    return HttpResponse(template.render(context, request))


userWord = ""
currWord = ""
usedLetters = "a"
count = 0
username = "noName"
def hangman(request):
    dictionaryLen = 349900;  # Static value will never change unless new words are added
    global userWord
    global currWord
    global usedLetters
    global count
    wordLen = 0;
    newLetter = ""
    isActive = 'true'
    message = ""
    i = 0;
    template = loader.get_template('gamePage/gamePage.html')
    if(request.method == 'GET'):
        count = 0
        message = ""
    if (request.method == 'POST'):
        data = request.POST
        newLetter = data.get("inputChar")
        print(currWord)
        j = 0
        if usedLetters.__contains__(newLetter):
            message = "Letter already used..."
        else:
            message = ""
            usedLetters += newLetter + " "
        # CHECKS IF DATA MATCHES
        if currWord.__contains__(newLetter):
            tempWord = list(userWord)
            userWord = ""

            while j < len(currWord):
                if(currWord[j] == newLetter):
                    tempWord[j*2] = newLetter
                j += 1

            userWord = userWord.join(tempWord)
            print(userWord)

        else:
            #TODO add a counter to update image
            count = int(count) + 1
            print(count)

    else:
        userWord = ""
        usedLetters = ""
        wordNum = random.randint(0, dictionaryLen)
        with open("hangman/static/dictionary.txt") as f:
            lines = f.readlines()
        currWord = lines[wordNum]  # or whatever you want to do with this line
        wordLen = len(lines[wordNum])-1
        while i < wordLen: #print the llength of the word in underscores
            userWord = userWord + "_ "
            i = i + 1

    isMatching = userWord.replace(" ", "")
    currWord = currWord.strip()
    img = 'img/hm'+str(count)+'.PNG'
    print(img)

    if currWord.__eq__(isMatching):
        message = "You Win!!!"
        print("WORDS MATCH SUBMIT TO DB")
        newEntry = Scoreboard(username=username, wordSize=len(currWord), score=count, word=currWord)
        newEntry.save()
        isActive = 'false'

    elif count == 6:
        message = "You Lose..."
        isActive = 'false'
    context = {
        "word": userWord,
        "message": message,
        "usedLetters": usedLetters,
        "img": img,
        'isActive': isActive
    }


    return HttpResponse(template.render(context, request))


def displayScore(request):
    score_list = Scoreboard.objects.all().order_by('-id')
    context = {
        'score_list': score_list,
    }
    template = loader.get_template('displayScore/displayScore.html')
    return HttpResponse(template.render(context, request))

#TODO CREATE SCOREBOARD MODEL