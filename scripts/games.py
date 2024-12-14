import pandas as pd
import numpy as np

def selectRandomlyWeighted(df: pd.DataFrame):
    weights = df['frequency'] / df['frequency'].sum()

    selected_index = np.random.choice(df.index, p=weights)

    selected_row = df.loc[selected_index]

    return selected_row


def nextWord(df: pd.DataFrame, name: str):
    dfMasked = df[df['firstNoun'] == name]
    if dfMasked.shape[0] == 0:
        return None
    
    print(dfMasked)
    return selectRandomlyWeighted(dfMasked)

def generatePuzzle(seed: str, df: pd.DataFrame, n):
    dfMasked = df[df['firstNoun'] == seed]

    puzzles = [seed, []]

    for index, row in dfMasked.iterrows():
        if n != 0:
           puzzles[1].append(generatePuzzle(row['secondNoun'], df, n - 1))

    return puzzles
    
def printPuzzles(puzzles, n, string = ""):
    if puzzles[1] == []:
        if string.count('-') == n:
            pass
            print(string[1:])


    for puzzle in puzzles[1]:
        new_string =  string + '-' + puzzles[0]
        if puzzle[1] == []:
            if new_string.count('-') == n:
                print(new_string[1:])
        else:
            printPuzzles(puzzle, n, new_string)


def main():
    df = pd.read_csv('data/compoundNounsWithoutFaultyAndUnwantedWithFrequencies.csv')
    dfShortendFirstNoun = df[df['firstNoun'].str.len() <= 10]
    dfShortendSecondNoun = dfShortendFirstNoun[dfShortendFirstNoun['secondNoun'].str.len() <= 10]
    dfCapped = dfShortendSecondNoun[dfShortendSecondNoun['frequency'] > 1000]
    dfWithoutConnectors = dfCapped[dfCapped['connectorParticle'].isna()]
    dfSorted = dfWithoutConnectors.sort_values('frequency', ascending=False)

    n = 3

    puzzles = generatePuzzle('MARKT', dfSorted, n)
    printPuzzles(puzzles, n)









if __name__ == '__main__':
    main()
