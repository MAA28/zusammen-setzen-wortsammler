from compoundNoun import CompoundNoun

def getFrequency(word):
    url = f'https://www.dwds.de/frequency/?corpus=dwdsxl&q={word}'
    response = requests.request('GET', url)

    if response.status_code == 200:
        return int(response.text[1:-1])


def getFrequencies():
    with open('../data/compoundNounsWithoutFaultyAndUnwantedWithFrequencies.csv', 'w') as file:
        file.write('firstNoun,connectorParticle,secondNoun,frequency\n')

    with open('../data/compoundNounsWithoutFaultyAndUnwanted.csv', 'r') as file:
        compoundNouns = []
        text = file.read()
        lines = text.split('\n')
        compoundNouns = [CompoundNoun.fromCSVLine(
            line) for line in lines[1:-1]]

    q = queue.Queue()

    bar = tqdm(total=len(compoundNouns))

    def worker():
        while True:
            compoundNoun = q.get()
            word = compoundNoun.reconstruct()

            frequency = getFrequency(word)
            if frequency is not None:
                tqdm.write(f'Saving word: {
                           compoundNoun} with frequncy of {frequency}')
                with open('../data/compoundNounsWithoutFaultyAndUnwantedWithFrequencies.csv', 'a') as file:
                    file.write(compoundNoun.toCSVLine() + f',{frequency}\n')

            q.task_done()

    for i in range(50):
        threading.Thread(target=worker, daemon=True).start()

    for compoundNoun in compoundNouns:
        q.put(compoundNoun)

    while q.qsize() != 0:
        bar.n = len(compoundNouns) - q.qsize()
        bar.refresh()

    q.join()

if __name__ == '__main__':
    getFrequencies()
