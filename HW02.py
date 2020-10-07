import csv
from bs4 import BeautifulSoup
import requests
import json
import re
import pprint 

def csv_parser(filename):

    list = []
    country = ""
    region = ""
    population = ""
    density = ""
    gdp = ""
    literacy = ""

    with open(filename + '.csv', 'r', encoding = "utf8") as csv_file:

        csv_reader = csv.DictReader(csv_file)

        if (filename == 'countries'):
            # find fieldnames

            for row in csv_reader:

                try:

                    country = str(row['Country'].strip())    #removed outer spaces
                    region = str(row['Region'].strip())
                    population = int(row['Population'])
                    density = float(row['Pop. Density (per sq. mi.)'].replace(",", "."))

                    gdp = int(row['GDP ($ per capita)'])
                    if (gdp == ""): gdp = "Unknown"

                    literacy = float(row['Literacy (%)'].replace(",", "."))
                    if literacy == "": literacy = "Unknown"

                except Exception as e:
                    gdp = "Unknown"
                    literacy = "Unknown"
                    pass
                
                print(gdp)

csv_parser('countries')