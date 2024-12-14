import pandas as pd
from pprint import pprint
import numpy as np
from tqdm import tqdm, trange
from random import sample


def selectRandomlyWeighted(df: pd.DataFrame):
    weights = df['frequency'] / df['frequency'].sum()

    selected_index = np.random.choice(df.index, p=weights)

    selected_row = df.loc[selected_index]

    return selected_row


def selectRandomly(array: [], n):
    new_array = []
    for i in sample(range(len(array), n)):
        new_array.append(array[i])
    return new_array


def nextWord(df: pd.DataFrame, name: str):
    dfMasked = df[df['firstNoun'] == name]
    if dfMasked.shape[0] == 0:
        return None

    print(dfMasked)
    return selectRandomlyWeighted(dfMasked)


def generatePuzzle(df: pd.DataFrame, n):
    keyValuePairs = [(row['firstNoun'], set()) for i, row in df.iterrows()]
    puzzles = [dict(keyValuePairs)]

    for i in trange(n - 1):
        keyValuePairs = puzzles[-1].keys()
        puzzles.append({})
        for item in tqdm(keyValuePairs, desc=f'All words at depth {i}'):
            dfMasked = df[df['firstNoun'] == item]
            for i, row in dfMasked.iterrows():
                name = row['secondNoun']
                puzzles[-1][name] = set()
                puzzles[-2][item].add(name)

    return puzzles[:-1]


def generateStrings(puzzles, n, k):
    puzzle_strings = []

    for word in puzzles[0]:
        puzzle_strings.append(word)

    for puzzle in tqdm(puzzles, desc="Working through the iterations"):
        new_puzzle_strings = []
        for puzzle_string in tqdm(puzzle_strings):
            last = puzzle_string.split('-')[-1]
            if last in puzzle.keys():
                for next in puzzle[last]:
                    new_puzzle_strings.append(puzzle_string + '-' + next)
        puzzle_strings = new_puzzle_strings if len(
            new_puzzle_strings) < k else sample(new_puzzle_strings, k)

    return puzzle_strings


def main():
    df = pd.read_csv(
        '../data/compoundNounsWithoutFaultyAndUnwantedWithFrequencies.csv')
    dfShortendFirstNoun = df[df['firstNoun'].str.len() <= 10]
    dfShortendSecondNoun = dfShortendFirstNoun[dfShortendFirstNoun['secondNoun'].str.len(
    ) <= 10]
    dfCapped = dfShortendSecondNoun[dfShortendSecondNoun['frequency'] > 1000]
    dfWithoutConnectors = dfCapped[dfCapped['connectorParticle'].isna()]
    dfSorted = dfWithoutConnectors.sort_values('frequency', ascending=False)

    n = 10

    puzzles = generatePuzzle(dfSorted, n)

    strings = generateStrings(puzzles, len(puzzles), 100000)

    with open('../data/puzzles.txt', 'w') as file:
        for string in tqdm(strings, desc='Saving...'):
            file.write(string + '\n')





if __name__ == '__main__':
    main()
