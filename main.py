import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import threading
import queue
import re


class CompoundNoun:
    def __init__(self, firstNoun, connectorParticle, secondNoun):
        self.firstNoun = firstNoun
        self.connectorParticle = connectorParticle
        self.secondNoun = secondNoun

    def __format__(self, spec):
        if self.connectorParticle == '':
            return f'{self.firstNoun} + {self.secondNoun}'
        else:
            return f'{self.firstNoun} + {self.connectorParticle} + {self.secondNoun}'

    def reconstruct(self):
        return f'{self.firstNoun}{self.connectorParticle}{self.secondNoun}'

    def toCSVLine(self):
        return f'{self.firstNoun},{self.connectorParticle},{self.secondNoun}'

    def fromCSVLine(line):
        values = line.split(',')
        return CompoundNoun(values[0], values[1], values[2])


def bisect_word(compound_noun):

    url = f'https://www.dwds.de/wb/{compound_noun}'

    response = requests.request('GET', url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, features='html.parser')
        selector = 'div.dwdswb-ft-block:nth-child(4) > span:nth-child(2) > a'
        selection = soup.select(selector)
        words = [word.string.upper()
                 for word in selection if word.string is not None]

        if len(words) == 2:
            connectorParticle = compound_noun.strip(words[0]).rstrip(words[1])
            if words[0] + connectorParticle + words[1] == compound_noun:
                return CompoundNoun(words[0], connectorParticle, words[1])

    return None


def getWordsFromLetter(letter):
    url = f'https://www.dwds.de/sitemap/{letter}'

    response = requests.request('GET', url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, features='html.parser')
        selector = '.lemmalist > li'
        selection = soup.select(selector)
        words = []
        for listItem in tqdm(selection, desc=f'Processing all {letter}-words'):
            aString = listItem.find('a').string
            if aString is not None:
                words.append(aString.upper())

        return words


def getAllWords():
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    words = []

    for letter in tqdm(letters, desc='Collecting words'):
        words += getWordsFromLetter(letter)

    return words


def saveAllWords():
    words = getAllWords()

    with open('words.txt', 'w') as file:
        file.write('\n'.join(words))


def bisectAllWords(start=0):

    with open('compoundNouns.csv', 'w') as file:
        file.write("firstNoun,connectorParticle,secondNoun\n")

    with open('words.txt', 'r') as file:
        words = file.read().split('\n')

    q = queue.Queue()

    bar = tqdm(total=len(words[start:]))

    def worker():
        while True:
            word = q.get()

            compoundNoun = bisect_word(word)

            if compoundNoun is not None:
                tqdm.write(f'Saving word: {compoundNoun}')
                with open('compoundNouns.csv', 'a') as file:
                    file.write(compoundNoun.toCSVLine())

            q.task_done()

    for i in range(50):
        threading.Thread(target=worker, daemon=True).start()

    for word in words[start:]:
        q.put(word)

    while q.qsize() != 0:
        bar.n = len(words) - q.qsize()
        bar.refresh()

    q.join()


def removeFaultyAndUnwantedCompoundNouns():
    with open('compoundNouns.csv', 'r') as file:
        compoundNouns = []
        text = file.read()
        lines = text.split('\n')
        compoundNouns = [CompoundNoun.fromCSVLine(
            line) for line in lines[1:-1]]

    with open('words.txt', 'r') as file:
        words = file.read().split('\n')

    keepers = []

    for compoundNoun in tqdm(compoundNouns):
        reconstruction = compoundNoun.reconstruct()
        if reconstruction in words and re.match(r'^[A-Z]+$', reconstruction):
            keepers.append(compoundNoun)

    print(f'Keeping {len(keepers)} / {len(compoundNouns)
                                      } ({len(keepers) / len(compoundNouns):.2%})')

    with open('compoundNounsWithoutFaultyAndUnwanted.csv', 'w') as file:
        file.write("firstNoun,connectorParticle,secondNoun\n")
        file.write('\n'.join([keeper.toCSVLine() for keeper in keepers]))


def getFrequency(word):
    url = f'https://www.dwds.de/frequency/?corpus=dwdsxl&q={word}'
    response = requests.request('GET', url)

    if response.status_code == 200:
        return int(response.text[1:-1])


def getFrequencies():
    with open('compoundNounsWithoutFaultyAndUnwanted.csv', 'r') as file:
        compoundNouns = []
        text = file.read()
        lines = text.split('\n')
        compoundNouns = [CompoundNoun.fromCSVLine(
            line) for line in lines[1:-1]]

    q = queue.Queue()

    bar = tqdm(total=len(compoundNouns[start:]))

    def worker():
        while True:
            compoundNoun = q.get()
            word = compoundNoun.reconstruct()

            frequency = getFrequency(word)
            if frequency is not None:
                tqdm.write(f'Saving word: {
                           compoundNoun} with frequncy of {frequency}')
                with open('compoundNounsWithoutFaultyAndUnwantedWithFrequencies.csv', 'a') as file:
                    file.write(compoundNoun.toCSVLine() + f',{frequency}')

            q.task_done()

    for i in range(50):
        threading.Thread(target=worker, daemon=True).start()

    for compoundNoun in compoundNouns:
        q.put(compoundNoun)

    while q.qsize() != 0:
        bar.n = len(compoundNouns) - q.qsize()
        bar.refresh()

    q.join()


def main():
    getFrequencies()


if __name__ == '__main__':
    main()
