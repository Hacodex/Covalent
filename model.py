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
    def setUniqueWords(self):
        self.uniqueWords = [word.strip(string.punctuation) for word in self.uniqueWords]
        self.uniqueWords = [word for word in self.uniqueWords if word not in ["", " ", "\n", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]]
    def setTFIDF(self):
        for word in self.uniqueWords:
            tf = 0
            for sentence in self.sentences:
                tf += UserData.helperTermFrequency(word, sentence)
            idf = UserData.helperInverseDocumentFrequency(word, self.sentences)
            self.tfidf.append(tf * idf)
    def setVecs(self, wordList, embeddings):
        for word in self.uniqueWords:
            tmpbool = True
            try:
                index = wordList.index(word)
            except:
                print("Word not in dataset:", word)
                self.uniqueWords.remove(word)
                print(len(self.uniqueWords))
                tmpbool = False
                continue
            if tmpbool:
                self.ivecs.append(embeddings[index])
                if embeddings[index] == ['NA'] * 50:
                    del self.ivecs[len(self.ivecs)-1]
                    self.uniqueWords.remove(word)
                    print("Vector is NA:", word)
        traits = ["openness", "conscientiousness", "neuroticism", "extraversion", "agreeableness"]
        for trait in traits:
            index = wordList.index(trait)
            self.rvecs.append(embeddings[index])
    def toString(self):
        print(self.name)
        print(self.email)
        print(self.city)
        print(self.state)
        print(self.school)
        print(self.classes)
    @staticmethod
    def helperTermFrequency(word, sentence):
        if len(sentence) == 0:
            return 0
        count = 0
        for currWord in sentence.split(" "):
            if word == currWord:
                count += 1
        return count/len(sentence)
    @staticmethod
    def helperInverseDocumentFrequency(word, sentences):
        count = 0
        for sentence in sentences:
            if word in sentence:
                count += 1
        return math.log(count/len(sentences))

class Model:
    def __init__(self, thisData):
        self.data = thisData
        self.finalscores = []
    def trainModel(self):
        for referenceVector in self.data.rvecs:
            allBetas = []
            for iVector in self.data.ivecs:
                gpr = GaussianProcessRegressor(random_state=0).fit(np.array(iVector).reshape(-1, 1), np.array(referenceVector))
                allBetas.append(gpr.score(np.array(iVector).reshape(-1, 1), np.array(referenceVector)))
            print("Betas:", len(allBetas), "TFIDF", len(self.data.tfidf))
            if len(allBetas) == len(self.data.tfidf):
                self.finalscores.append(np.dot(allBetas, self.data.tfidf))
            else:
                if len(allBetas) > len(self.data.tfidf):
                    self.finalscores.append(np.dot(allBetas[0:len(self.data.tfidf)], self.data.tfidf))
                else:
                    self.finalscores.append(np.dot(allBetas, self.data.tfidf[0:len(allBetas)]))
    def performDropOut(self, dropoutRate, nFeatures):
        random.seed(time.time())
        nKeep = round(nFeatures*dropoutRate)
        indReplace = random.sample(range(nFeatures), (nFeatures - nKeep))
        for i in range(len(self.data.ivecs)):
            self.data.ivecs[i] = list(map(float, self.data.ivecs[i]))
            vecMean = sum(self.data.ivecs[i])/len(self.data.ivecs[i])
            self.data.ivecs[i] = [vecMean if ind in indReplace else self.data.ivecs[i][ind] for ind in range(len(self.data.ivecs[i]))]
        for i in range(len(self.data.rvecs)):
            self.data.rvecs[i] = list(map(float, self.data.rvecs[i]))
            vecMean = sum(self.data.rvecs[i])/len(self.data.rvecs[i])
            self.data.rvecs[i] = [vecMean if ind in indReplace else self.data.rvecs[i][ind] for ind in range(len(self.data.rvecs[i]))]

class Results:
    def __init__(self, email, users, info, scores):
        self.email = email
        self.users = users
        self.indUsers = Results.getIndexOfUser(email, self.users) 
        self.info = info
        self.indInfo = Results.getIndexOfUser(email, self.info)
        self.scores = scores
        self.indScores = Results.getIndexOfUser(email, self.scores)
    def main(self):
        ##Make Friends Results
        currUser = UserData({"description": self.info[self.indInfo]["description"], "name": self.users[self.indUsers]["name"], "email": self.info[self.indInfo]["email"], "city": self.info[self.indInfo]["city"], "state": self.info[self.indInfo]["state"], "school": self.info[self.indInfo]["school"], "classes": self.info[self.indInfo]["classes"]})
        friendsLocation, friendsSchool, friendsClasses = [], [], []
        
        for i in range(len(self.info)):
            email = self.info[i]["email"]
            indUsers = Results.getIndexOfUser(email, self.users) 
            indInfo = Results.getIndexOfUser(email, self.info)
            tmpUser = UserData({"description": self.info[indInfo]["description"], "name": self.users[indUsers]["name"], "email": self.info[indInfo]["email"], "city": self.info[indInfo]["city"], "state": self.info[indInfo]["state"], "school": self.info[indInfo]["school"], "classes": self.info[indInfo]["classes"]})
            if tmpUser.email == currUser.email:
                continue
            if len(friendsLocation) <= 5:
                if tmpUser.state == currUser.state:
                    friendsLocation.append(tmpUser)
            if len(friendsSchool) <= 5:
                if tmpUser.school == currUser.school:
                    friendsSchool.append(tmpUser)
            for word in tmpUser.classes:
                if len(friendsClasses) == 5:
                    break
                if word in currUser.classes:
                    friendsClasses.append(tmpUser)

        teamMembers = [UserData(), UserData(), UserData(), UserData(), UserData()]
        currUserScores = list(self.scores[self.indScores].values())[2:]
        userBestAttribute = currUserScores.index(max(currUserScores))
        teamMembers[userBestAttribute] = currUser
        bestScores = [-10000,-10000,-10000,-10000,-10000]

        ##Make Team Build Results
        for i in range(len(self.scores)):
            email = self.info[i]["email"]
            indUsers = Results.getIndexOfUser(email, self.users) 
            indInfo = Results.getIndexOfUser(email, self.info)
            tmpUser = UserData({"description": self.info[indInfo]["description"], "name": self.users[indUsers]["name"], "email": self.info[indInfo]["email"], "city": self.info[indInfo]["city"], "state": self.info[indInfo]["state"], "school": self.info[indInfo]["school"], "classes": self.info[indInfo]["classes"]})
            indScores = Results.getIndexOfUser(email, self.scores)
            tmpUserScores = list(self.scores[indScores].values())[2:]
            tmpBestAttribute = tmpUserScores.index(max(tmpUserScores))
            print(tmpBestAttribute)
            if tmpBestAttribute != userBestAttribute and (teamMembers[tmpBestAttribute].name != "" or tmpUserScores[tmpBestAttribute] > bestScores[tmpBestAttribute]):
                teamMembers[tmpBestAttribute] = tmpUser
                bestScores[tmpBestAttribute] = tmpUserScores[tmpBestAttribute]
        del teamMembers[userBestAttribute]
        return teamMembers, friendsLocation, friendsSchool, friendsClasses
    @staticmethod
    def makeAll(inputDict, wordList, embeddings):
            ##Initialize User
            currUser = UserData(inputDict)
            currUser.setUniqueWords()
            currUser.setVecs(wordList, embeddings)
            currUser.setTFIDF()

            ##Model
            userModel = Model(currUser)
            userModel.performDropOut(0.7, 50)
            userModel.trainModel()
            return currUser, userModel
    @staticmethod
    def getIndexOfUser(email, inputDict):
        for i in range(len(inputDict)):
            if inputDict[i]["email"] == email:
                return i
        return ":/"