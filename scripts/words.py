from compoundNoun import CompoundNoun

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

    with open('../data/words.txt', 'w') as file:
        file.write('\n'.join(words))


if __name__ == '__main__':
    saveAllWords()
