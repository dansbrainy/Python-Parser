import csv
from bs4 import BeautifulSoup
import requests
import json
import re
import pprint 

def csv_parser(filename):

    lines = []
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

            for row in csv_reader:      #Read

                try:

                    country = str(row['Country'].strip())    #removed outer spaces
                    region = str(row['Region'].strip())
                    population = int(row['Population'])
                    density = float(row['Pop. Density (per sq. mi.)'].replace(",", "."))

                    gdp = int(row['GDP ($ per capita)'])
                    if (gdp == ""): gdp = "Unknown"

                    literacy = float(row['Literacy (%)'].replace(",", "."))
                    if literacy == "": literacy = "Unknown"

                    values = [country, region, population, density, gdp, literacy]
                    
                    lines.append(values)

                    pprint.pprint(lines, indent=2)

                except Exception as e:
                    return e

                return lines

data = csv_parser('countries')

def json_parser(filename, data): 

    languages = ""
    dish = ""
    religion = ""
    government = ""
    currency = ""

    # pprint(data)

    with open(filename + '.json', 'r') as json_file:

        json_data = json.load(json_file)

        for country in data[0]:
            
            # json_country = re.search(country, json_data)
            for item in json_data:

                if country == item:
                    print('yes')            #WRITE

                try:
            
                    languages = (item['languages']).split() 
                    if languages == "": languages = "Unknown"
                    dish = item['national_dish']
                    if dish == "": dish = "Unknown"
                    religion = item['religion']
                    if religion == "": dish = "Unknown"
                    government = item['government']
                    if government == "": government = "Unknown"
                    currency = item['currency']
                    if currency == "": currency = "Unknown"

                except Exception as e:
                    return e

json_parser('additional_stats', data)