import requests
from tqdm import tqdm
from bs4 import BeautifulSoup


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

    def toCSVLine(self):
        return f'{self.firstNoun},{self.connectorParticle},{self.secondNoun}\n'


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

    for word in tqdm(words[start:], desc='Bisecting all words'):
        compoundNoun = bisect_word(word)
        if compoundNoun is not None:
            with open('compoundNouns.csv', 'a') as file:
                file.write(compoundNoun.toCSVLine())


def main():
    bisectAllWords()


if __name__ == '__main__':
    main()
