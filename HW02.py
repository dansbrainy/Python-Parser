import csv
from bs4 import BeautifulSoup
import requests
import json
import re
import pprint 

def csv_parser(filename):

    lines = []
    countries = []
    regions = []
    populations = []
    densities = []
    gdps = []
    literacies = []

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
                    gdp = int(row['GDP ($ per capita)']) if (gdp == ""): gdp = "Unknown"
                    literacy = float(row['Literacy (%)'].replace(",", ".")) if literacy == "": literacy = "Unknown"

                    countries.append(country)
                    regions.append(region)
                    populations.append(population)
                    densities.append(density)
                    gdps.append(gdp)
                    literacies.append(literacy)

                    # lines.append(country, region, population, density, gdp, literacy)
                    pprint.pprint(lines, indent=2)

                except Exception as e:
                    return e
        
    lines = countries, regions, populations, densities, gdps, literatures
    csv_file.close()

    return lines
    
      #check if right
def json_parser(filename, data): 

    languages = []
    dishes = []
    religions = []
    governments = []
    currencies = []

    # pprint(data)

    with open(filename + '.json', 'r') as json_file:

        details = {}

        json_data = json.load(json_file)

        for country in data[0]:

            # json_country = re.search(country, json_data)
            for item in json_data:

                if country == item:
                    print('yes')            #WRITE

                    try:

                        language = (item['languages']).split() if language == "": language = "Unknown"
                        dish = item['national_dish'] if dish == "": dish = "Unknown"
                        religion = item['religion'] if religion == "": religion = "Unknown"
                        government = item['government'] if government == "": government = "Unknown"
                        currency = item['currency'] if currency == "": currency = "Unknown"
                        
                        languages.append(langauge)
                        dishes.append(dish)
                        religions.append(religion)
                        governments.append(government)
                        currencies.append(currency)

                    except Exception as e:
                        return e
        
    
        details["Country"] = data[0]
        details["Region"] = data[1]
        details["Population"] = data[2]
        details["Pop. Density(per sq. mi.)"] = data[3]
        details["GDP ($ percapita)"] = data[4]
        details["Literacy (%)"] = data[5]
        
        details["Languages"] = languages
        details["National Dish"] = dish
        details["Religion"] = religion
        details["Government"] = government
        details["Currency Name"] = currency

        return details
        pprint.pprint(details, indent=2)

data = csv_parser('countries')    
json_parser('additional_stats', data)