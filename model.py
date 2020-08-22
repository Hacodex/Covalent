import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
import csv
import random
import time
import timeit
import math
import string

class UserData:
    def __init__(self, inputDict = {"description": "", "name": "", "email": "", "city": "", "state": "", "school": "", "classes": ""}):
        self.origText = inputDict['description']
        self.uniqueWords = []
        self.sentences = self.origText.split(".")
        for i in range(len(self.sentences)):
            tmp = self.sentences[i].split(" ")
            tmp = [word.strip(string.punctuation).lower() for word in tmp if word not in ["", " ", "\n", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]]
            self.uniqueWords = list(set(self.uniqueWords + tmp))
            self.sentences[i] = " ".join(tmp)
        self.sentences = [sentence for sentence in self.sentences if sentence != ""]
        self.tfidf = []
        self.ivecs = []
        self.rvecs = []
        self.name = inputDict['name']
        self.email = inputDict['email']
        self.city = inputDict['city']
        self.state = inputDict['state']
        self.school = inputDict['school']
        self.classes = inputDict['classes'].split(",")
        self.classes = [word.strip(string.punctuation).lower() for word in self.classes]