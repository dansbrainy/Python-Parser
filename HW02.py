import csv
from bs4 import BeautifulSoup
import requests
import json
import re
import pprint

# 2333.20 + 2422.68
# experience in marketing 

def csv_parser(filename):

    with open(filename + '.csv', 'r', encoding = "utf8") as csv_file:

        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            print(row)

csv_parser('countries')