import csv
from bs4 import BeautifulSoup
import requests
import json
import re
import pprint 

def csv_parser(filename):

    lines = []

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

                    lines.append([country, region, population, density, gdp, literacy])
            
                except Exception:
                    if gdp == "": gdp = "Unknown"
                    if literacy == "": literacy = "Unknown"
                    # pass e

    # pprint.pprint(lines, indent=2)
    # print(lines)
    csv_file.close()

    return lines
    
      #check if right
def json_parser(filename, data): 

    new_data = []
    # print(data[0][0])

    with open(filename + '.json', 'r') as json_file:

        json_data = json.load(json_file)
        # print(json_data)

        length = len(data)
        i = 0

        for i in range(length):
        # while i < length:

            country = data[i][0]
            # print(country)

            if country in json_data:
                # print('yes') 
                # print(country)

                details = {}

                #WRITE
                json_country_key = json_data[country]
                # print(json_country_key)
            
                try:

                    languages = str(json_country_key['languages']).split(';') 
                    dish = json_country_key['national_dish'] 
                    religion = json_country_key['religion'] 
                    government = json_country_key['government'] 
                    currency = json_country_key['currency_name'] 

                    if languages == "": languages = "Unknown"
                    if dish == "": dish = "Unknown"
                    if religion == "": religion = "Unknown"
                    if government == "": government = "Unknown"
                    if currency == "": currency = "Unknown"

                    details['Country'] = data[i][0]
                    details['Region'] = data[i][1]
                    details['Population'] = data[i][2]
                    details['Pop. Density(per sq. mi.)'] = data[i][3]
                    details["GDP ($ percapita)"] = data[i][4]
                    details["Literacy (%)"] = data[i][5]
                    
                    details["Languages"] = languages
                    details["National Dish"] = dish
                    details["Religion"] = religion
                    details["Government"] = government
                    details["Currency Name"] = currency

                    new_data.append(details)
                    # i += 1
                except Exception as e:

                    return e
                    # pass

    # pprint.pprint(details, indent=2)
    return new_data

def company_parser(filename, data):
    
    parsed_data = {}

    with open(filename + '.csv', 'r', encoding = "utf8") as csv_file:

        csv_reader = csv.DictReader(csv_file)

        if (filename == 'companies'):

            parsed_data['Unknown']= {'GDP ($ per capita)': 0}, {'businesses': 'value'}, {'industries': 'value'}, {'estimated_employees': 'value'}

            for row in csv_reader:      #Read
                
                try:

                    country = str(row['country'].strip())   #removed outer spaces
                    country =" ".join([word.capitalize() for word in country.split()])  #capitalise each word
                    businesses = []
                    industries = []
                    estimated_employees = 0

                    length = len(data)
                    # i = 0

                    for i in range(length):

                        list_country_key = data[i][0]

                        # print(list_country_key)
                        
                        if country == list_country_key:
                            # print('yes') 
                            # print(list_country_key)
                            try:
                                gdp = int(data[i][5])
                                business = str(row['name'].strip())
                                business = " ".join([word.capitalize() for word in business.split()])
                                industry = str(row['industry'].strip())
                                total_employee = int(row['total employee estimate'])

                                businesses.append(business)
                                industries.append(industry)
                                estimated_employees += total_employee

                                print(estimated_employees)

                            except Exception as e:
                                return e
                                    
                        if country == None:
                            print('no') 
                            country = "Unknown"
                            gdp = 0
                        
                    
                    # {'Country': 'Zimbabwe', 'Region': 'SUB-SAHARAN AFRICA', 'Population': 12236805, 'Pop. Density(per sq.rcapita)': 1900, 'Litera mi.)': 31.3, 'GDP ($ percapita)': 1900, 'Literacy (%)': 90.7, 'Languages': ['English', 'Ndebele', 'Nyanja', 'Shona'], 'National Dish': 'Sadza', 'Religion': 'cy Name': 'Zimbabwe DollChristianity', 'Government': 'Republic', 'Currency Name': 'Zimbabwe Dollar'}

                    # gdp = int(row['GDP ($ per capita)'])
                    # region = str(row['Region'].strip())
                    # population = int(row['Population'])
                    # density = float(row['Pop. Density (per sq. mi.)'].replace(",", "."))

                    
                    # literacy = float(row['Literacy (%)'].replace(",", ".")) 

                    # lines.append([country, region, population, density, gdp, literacy])
                        

                    
                    # print(country)

                        
                except Exception as e:

                    return e

    return parsed_data
    
data = csv_parser('countries')  
# pprint.pprint(data, indent=2)     #testing
b = json_parser('additional_stats', data)
# print(b)                          #execute testing
company_parser('companies', data)