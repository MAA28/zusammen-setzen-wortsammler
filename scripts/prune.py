from compoundNoun import CompoundNoun

def removeFaultyAndUnwantedCompoundNouns():
    with open('data/compoundNouns.csv', 'r') as file:
        compoundNouns = []
        text = file.read()
        lines = text.split('\n')
        compoundNouns = [CompoundNoun.fromCSVLine(
            line) for line in lines[1:-1]]

    with open('data/words.txt', 'r') as file:
        words = file.read().split('\n')

    keepers = []

    for compoundNoun in tqdm(compoundNouns):
        reconstruction = compoundNoun.reconstruct()
        if reconstruction in words and re.match(r'^[A-Z]+$', reconstruction):
            keepers.append(compoundNoun)

    print(f'Keeping {len(keepers)} / {len(compoundNouns)
                                      } ({len(keepers) / len(compoundNouns):.2%})')

    with open('data/compoundNounsWithoutFaultyAndUnwanted.csv', 'w') as file:
        file.write("firstNoun,connectorParticle,secondNoun\n")
        file.write('\n'.join([keeper.toCSVLine() for keeper in keepers]))

if __name__ == '__main__':
    removeFaultyAndUnwantedCompoundNouns()
