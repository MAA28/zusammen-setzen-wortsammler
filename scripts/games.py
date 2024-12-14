import pandas as pd
from pprint import pprint
import numpy as np
from tqdm import tqdm, trange

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

def generatePuzzle(df: pd.DataFrame, n):
    queue = [[row['firstNoun']] for i, row in df.iterrows()]


    for i in trange(n):
        new_queue = []
        for item in tqdm(queue, desc=f'All words at depth {i}'):
            name = item[-1]
            dfMasked = df[df['firstNoun'] == name]
            for i, row in dfMasked.iterrows():
                new_queue.append(item + [row['secondNoun']])
        queue = new_queue
            
    
    return queue

    
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

    n = 6

    puzzles = generatePuzzle(dfSorted, n)
    # pprint(puzzles)
    # printPuzzles(puzzles, n)




# Unviable (exponetial growth)
# 0	5334
# 1	90004
# 2	401605
# 3	1801881
# 4	8100692



if __name__ == '__main__':
    main()
