import csv
import re

from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import SymptomInputForm, SelectionForm
from .models import Conversation
from django.contrib.auth.decorators import login_required
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import pyttsx3
# from django.conf import settings
from CARETECH import settings

# Load and preprocess data
training = settings.training_data
testing = settings.testing_data
cols = training.columns[:-1]
x = training[cols]
y = training['prognosis']

le = preprocessing.LabelEncoder()
le.fit(y)
y = le.transform(y)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
testx = testing[cols]
testy = testing['prognosis']
testy = le.transform(testy)
clf = DecisionTreeClassifier().fit(x_train, y_train)

severityDictionary = dict()
description_list = dict()
precautionDictionary = dict()
symptoms_dict = {}

for index, symptom in enumerate(x):
    symptoms_dict[symptom] = index


def calc_condition(exp, days):
    sum = 0
    for item in exp:
        sum = sum + severityDictionary[item]
    if ((sum * days) / (len(exp) + 1) > 13):
        sentence = "You should take the consultation from doctor. "
        print(sentence)
        readn(sentence)
        return sentence

    else:
        sentence = "It might not be that bad but you should take precautions."
        print(sentence)
        readn(sentence)
        return sentence


def getSeverityDict():
    global severityDictionary
    with open(settings.SYMPTOM_SEVERITY_FILE) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            print("^^^^^^^^^^^^\n\nRow:", row)
            if len(row) >= 2:
                _diction = {row[0]: int(row[1])}
                severityDictionary.update(_diction)
            else:
                print(f"Skipping invalid row: {row}")


def getDescription():
    global description_list
    with open(settings.SYMPTOM_DESCRIPTION_FILE) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            _description = {row[0]: row[1]}
            description_list.update(_description)


def getprecautionDict():
    global precautionDictionary
    with open(settings.SYMPTOM_PRECAUTION_FILE) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            _prec = {row[0]: [row[1], row[2], row[3], row[4]]}
            precautionDictionary.update(_prec)


getSeverityDict()
getDescription()
getprecautionDict()


def readn(nstr):
    engine = pyttsx3.init()
    engine.setProperty('voice', "english+f5")
    engine.setProperty('rate', 130)
    engine.say(nstr)
    engine.runAndWait()
    engine.stop()


def extract_symptoms(message):
    symptoms = []
    for symptom in severityDictionary.keys():
        if re.search(symptom, message, re.IGNORECASE):
            symptoms.append(symptom)
    return symptoms


def get_response(symptoms_input, days):
    symptoms_present = []
    for symptom in symptoms_input:
        if symptom in symptoms_dict:
            symptoms_present.append(symptom)
        else:
            print(f"Symptom '{symptom}' not found in symptoms_dict")

    if not symptoms_present:
        return "No valid symptoms provided."

    def sec_predict(symptoms_exp):
        df = pd.read_csv(settings.TRAINING_FILE)
        X = df.iloc[:, :-1]
        y = df['prognosis']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=20)
        rf_clf = DecisionTreeClassifier()
        rf_clf.fit(X_train, y_train)

        symptoms_dict = {symptom: index for index, symptom in enumerate(X)}
        input_vector = np.zeros(len(symptoms_dict))
        for item in symptoms_exp:
            input_vector[symptoms_dict[item]] = 1

        return rf_clf.predict([input_vector])

    # Simulate decision tree traversal and prediction
    present_disease = sec_predict(symptoms_present)[0]

    if present_disease in description_list:
        description = description_list[present_disease]
    else:
        description = "Description not available."

    if present_disease in precautionDictionary:
        precautions = precautionDictionary[present_disease]
    else:
        precautions = ["Precautions not available."]

    response = {
        "disease": present_disease,
        "description": description,
        "precautions": precautions,
    }

    return response


@login_required(login_url='login')
def chat_view(request):
    if request.method == "POST":
        user_input = request.POST.get("message")
        symptoms_input = user_input.split()  # Simple split by space, adapt as needed
        days = int(request.POST.get("days", 1))

        response = get_response(symptoms_input, days)
        return JsonResponse(response, safe=False)
    conversations = Conversation.objects.filter(user=request.user)
    context = {
        "conversations": conversations
    }
    return render(request, "chatbot/chat.html", context)
