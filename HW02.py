import csv
from bs4 import BeautifulSoup
import requests
import json
import re
import pprint 

def csv_parser(filename):

    lines = []
    # countries = []
    # regions = []
    # populations = []
    # densities = []
    # gdps = []
    # literacies = []

    with open(filename + '.csv', 'r', encoding = "utf8") as csv_file:

        csv_reader = csv.DictReader(csv_file)

        if (filename == 'countries'):
            # find fieldnames

            for row in csv_reader:      #Read

                try:

                    country = str(row['Country'].strip())   #removed outer spaces
                    region = str(row['Region'].strip())
                    population = int(row['Population'])
                    density = float(row['Pop. Density (per sq. mi.)'].replace(",", "."))
                    gdp = int(row['GDP ($ per capita)'])
                    
                    literacy = float(row['Literacy (%)'].replace(",", ".")) 
                    

                    # countries.append(country)
                    # regions.append(region)
                    # populations.append(population)
                    # densities.append(density)
                    # gdps.append(gdp)
                    # literacies.append(literacy)

                    lines.append([country, region, population, density, gdp, literacy])
            
                except Exception as e:
                    if gdp == "": gdp = "Unknown"
                    if literacy == "": literacy = "Unknown"
                    # return e
        
    # lines = [countries, regions, populations, densities, gdps, literacies]

    # pprint.pprint(lines, indent=2)
    # print(lines)
    csv_file.close()

    return lines
    
      #check if right
def json_parser(filename, data): 

    details = {}

    lines = []

    with open(filename + '.json', 'r') as json_file:

        json_data = json.load(json_file)

        for i in data[0]:

            country = i

            # json_country = re.search(country, json_data)
            for item in json_data:

                if country == item:
                    print('yes')            #WRITE

                    try:

                        languages = (item['languages']).split() 
                        dish = item['national_dish'] 
                        religion = item['religion'] 
                        government = item['government'] 
                        currency = item['currency'] 
                        if languages == "": languages = "Unknown"
                        if dish == "": dish = "Unknown"
                        if religion == "": religion = "Unknown"
                        if government == "": government = "Unknown"
                        if currency == "": currency = "Unknown"

                        # languages.append(language)
                        # dishes.append(dish)
                        # religions.append(religion)
                        # governments.append(government)
                        # currencies.append(currency)

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

                    except Exception as e:

                        # return e
                        pass


    # pprint.pprint(details, indent=2)
    return details


data = csv_parser('countries')    
# pprint.pprint(data, indent=2)     #testing
b = json_parser('additional_stats', data)
print(b)