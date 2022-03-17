import urllib.request
import re
import os
import glob
import logging
from datetime import datetime

logging.basicConfig(filename='log.txt', encoding='utf-8', level=logging.DEBUG)
wordleJsUrl = 'https://www.nytimes.com/games/wordle/main.b84b7aa7.js'
now = datetime.now()
nowString = now.strftime('%Y-%m-%d_%H-%M-%S')
guessListDir = 'guesslists'
answerListDir = 'answerlists'

def setUpDirs():
    if not os.path.exists(guessListDir):
        logging.info('Creating answers directory')
        os.makedirs(guessListDir)
    if not os.path.exists(answerListDir):
        logging.info('Creating guesses directory')
        os.makedirs(answerListDir)

def getWordLists():
    wordleJsResponse = urllib.request.urlopen(wordleJsUrl)
    wordleJs = str(wordleJsResponse.read())

    answerListString = re.search("Ma=(.*),Oa=", wordleJs).group(1)
    guessListString = re.search("Oa=(.*),Ra=", wordleJs).group(1)
    answerList = answerListString.strip('[]').split(',')
    guessList = guessListString.strip('[]').split(',')
    answerList = list(map(lambda x: x.strip('"'), answerList))
    guessList = list(map(lambda x: x.strip('"'), guessList))
    
    logging.info('Answer list has ' + str(len(answerList)) + ' entries')
    logging.info('Guess list has ' + str(len(guessList)) + ' entries')
    
    return answerList, guessList
    
def saveWordLists(answerList, guessList):
    f = open(r'answerlists/answers_' + nowString, 'w')
    f.write('\n'.join(answerList))
    f.close()
    f = open(r'guesslists/guesses_' + nowString, 'w')
    f.write('\n'.join(guessList))
    f.close()
    
def saveDiffList(diffList, answers=True, added=True):
    type = 'answers' if answers else 'guesses'
    change = 'added' if added else 'removed'
    diffFileName = r'diff_' + type + '_' + change + '_' + nowString
    if answers:
        diffFileName = r'diff_answers_' + nowString
    f = open(diffFileName, 'w')
    f.write('\n'.join(diffList))
    f.close()

def readWordList(filePath):
    f = open(filePath, 'r')
    text = f.read()
    f.close()
    return text.split('\n')
    
def getMostRecentList(answers=True):
    dirPath = 'guesslists'
    if answers:
        dirPath = 'answerlists'
    fileList = glob.glob(dirPath + '/*')
    if len(fileList) > 0:
        latestFile = max(fileList, key=os.path.getctime)
        return readWordList(latestFile)
    return None
    
def diffLists(list1, list2):
    removedItems = list(set(list1) - set(list2))
    addedItems = list(set(list2) - set(list1))
    return removedItems, addedItems
    
logging.info('')
logging.info('Starting wordle check at ' + nowString)
setUpDirs()
answerList, guessList = getWordLists()

lastAnswers = getMostRecentList()
lastGuesses = getMostRecentList(False)

if lastAnswers:
    removedAnswers, addedAnswers = diffLists(lastAnswers, answerList)
    if len(removedAnswers) > 0:
        logging.warning('Found ' + str(len(removedAnswers)) + ' removed answers')
        saveDiffList(removedAnswers, answers=True, added=False)
    if len(addedAnswers) > 0:
        logging.warning('Found ' + str(len(addedAnswers)) + ' added answers')
        saveDiffList(addedAnswers, answers=True, added=True)
if lastGuesses:
    removedGuesses, addedGuesses = diffLists(lastGuesses, guessList)
    if len(removedGuesses) > 0:
        logging.warning('Found ' + str(len(removedGuesses)) + ' removed guesses')
        saveDiffList(removedGuesses, answers=False, added=False)
    if len(addedGuesses) > 0:
        logging.warning('Found ' + str(len(addedGuesses)) + ' added guesses')
        saveDiffList(addedGuesses, answers=False, added=True)
    
saveWordLists(answerList, guessList)

