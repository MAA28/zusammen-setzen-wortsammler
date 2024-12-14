from pprint import pprint
import os
from supabased import supabase

with open('../data/puzzles.txt', 'r') as file:
    puzzles = [puzzle.split('-') for puzzle in file.read().split('\n')[:-1]]

unique_words = set(word for puzzle in puzzles for word in puzzle)

supabase.table("Words").delete().execute()

supabase.table("Words").insert([
    {'word': word}
    for word in unique_words
]).execute()
