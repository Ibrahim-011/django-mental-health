import random
import pickle
import json
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import tensorflow as tf
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate , login
from .forms import SignupForm
from django.contrib import messages

lemmatizer = WordNetLemmatizer()
intents = json.loads(open("chatbot/intents.json", encoding="utf8").read())
words = pickle.load(open('chatbot/words.pkl', 'rb'))
classes = pickle.load(open('chatbot/classes.pkl', 'rb'))
model = tf.keras.models.load_model('chatbot/model1.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence.lower())
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    error_threshold = 0.25  # 25%
    result = [[i, r] for i, r in enumerate(res) if r > error_threshold]
    result.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in result:
        return_list.append({'intents': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_responses(intents_list, intent_json):
    try:
        tag = intents_list[0]['intents']
        list_of_intents = intent_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
        return result
    except:
        return "Sorry I didn't really understand what you meant"

def get_bot_response(request):
    user_message = request.GET.get('user_message', '')
    if user_message:
        intent_list = predict_class(user_message)
        bot_response = get_responses(intent_list, intents)
    else:
        bot_response = "Please enter a valid message."
    return JsonResponse({'bot_response': bot_response})

def signupview(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to home page after signup
    else:
        form = SignupForm()
    return render(request, 'chatbot/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect ('home')  # Redirect back to login page with error message
    else:
        return render(request, 'chatbot/login.html')

def home(request):
    return render(request, 'chatbot/home.html')
