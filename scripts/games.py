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

def generatePuzzle(df: pd.DataFrame, n, seed: str = ''):
    dfUsing = df[df['firstNoun'] == seed] if seed != '' else df

    puzzles = [seed, []]

    for index, row in dfUsing.iterrows():
        if n != 0:
           puzzles[1].append(generatePuzzle(df, n - 1, row['secondNoun']))

    all_empty = True

    for puzzle in puzzles[1]:
        if len(puzzle) != 0:
            all_empty = False

    if all_empty:
        return [seed, []]

    return puzzles
    
def printPuzzles(puzzles, n, string = ""):
    string = string + '-' + puzzles[0] 
    if puzzles[1] == []:
        if string[1:].count('-') == n:
           print(string[2:])

    for puzzle in puzzles[1]:
        printPuzzles(puzzle, n, string)


def main():
    df = pd.read_csv('data/compoundNounsWithoutFaultyAndUnwantedWithFrequencies.csv')
    dfShortendFirstNoun = df[df['firstNoun'].str.len() <= 10]
    dfShortendSecondNoun = dfShortendFirstNoun[dfShortendFirstNoun['secondNoun'].str.len() <= 10]
    dfCapped = dfShortendSecondNoun[dfShortendSecondNoun['frequency'] > 1000]
    dfWithoutConnectors = dfCapped[dfCapped['connectorParticle'].isna()]
    dfSorted = dfWithoutConnectors.sort_values('frequency', ascending=False)

    n = 3

    puzzles = generatePuzzle(dfSorted, n)
    print(puzzles)
    printPuzzles(puzzles, n)









if __name__ == '__main__':
    main()
