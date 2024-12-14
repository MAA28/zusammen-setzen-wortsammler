from compoundNoun import CompoundNoun

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

def bisectAllWords(start=0):

    with open('data/compoundNouns.csv', 'w') as file:
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
                with open('data/compoundNouns.csv', 'a') as file:
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

if __name__ == '__main__':
    bisectAllWords()
