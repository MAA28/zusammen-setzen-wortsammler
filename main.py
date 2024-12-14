import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import threading
import queue
import re







def main():
    getFrequencies()
    print(getFrequency("Arbeit"))


if __name__ == '__main__':
    main()
