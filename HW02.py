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
    #
    # data = csv_parser('countries') 

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

    gdp = 0

    with open(filename + '.csv', 'r', encoding = "utf8") as csv_file:

        csv_reader = csv.DictReader(csv_file)

        if (filename == 'companies'):
            
            # parsed_data['Unknown'] = {'GDP ($ per capita)': 0}

            for row in csv_reader:
                
                country = str(row['country'].strip())   #removed outer spaces
                country =" ".join([word.capitalize() for word in country.split()])  #capitalise each word
                
                business = str(row['name'])
                business = " ".join([word.capitalize() for word in business.split()])
                industry = str(row['industry'])
                total_employee = int(row['total employee estimate'])

                if country == "":
                    country = "Unknown"
                    gdp = 0
                elif country != "":

                    length = len(data)

                    for i in range(length):
                        
                    #FORMAT OF DATA FROM CSV FILE
                    # {'Country': 'Nepal',
                    # 'Currency Name': 'Nepalese Rupee',
                    # 'GDP ($ percapita)': 1400,
                    # 'Government': 'Federal parliamentary republic',
                    # 'Languages': ['Bhojpuri',
                    #                 'Hindi',
                    #                 'Maithili',
                    #                 'Nepali',
                    #                 'Newari',
                    #                 'Tamang',
                    #                 'Tharu'],
                    # 'Literacy (%)': 45.2,
                    # 'National Dish': 'Dal bhat',
                    # 'Pop. Density(per sq. mi.)': 192.2,
                    # 'Population': 28287147,
                    # 'Region': 'ASIA (EX. NEAR EAST)',
                    # 'Religion': 'Hinduism'},

                        list_country_key = data[i]['Country']
                        # print(list_country_key)
                        if country == list_country_key:
                            # gdp = int(data[i][4])
                            gdp = int(data[i]['GDP ($ percapita)'])

                
                # parsed_data[country] = {'GDP ($ per capita)': gdp, 'businesses': [], 'industries': []}

                parsed_data.setdefault(country, {})
                parsed_data[country].setdefault('GDP ($ per capita)', gdp)
                parsed_data[country].setdefault('businesses', [])
                parsed_data[country].setdefault('industries', [])
                parsed_data[country].setdefault('estimated_employees', 0)

                if country in parsed_data:
                                        
                    parsed_data[country]['businesses'].append(business)

                    
                    parsed_data[country]['industries'].append(industry)

                    
                    parsed_data[country]['estimated_employees'] = total_employee

                else:
                    # create a new array in this slot
                    parsed_data[country]['businesses'] = [business]
                    parsed_data[country]['industries']= [industry]
                    parsed_data[country]['estimated_employees'] += total_employee
                    
                    # break

                    # if re.search(r'\[Data\]', line):
                    # if re.match(list_country_key.lower(), line):
                    # # elif "united states" in line:

    csv_file.close()

    return parsed_data

def country_stats(json_filename, txt_filename, data):

    try:
        #write to json file
        with open(json_filename + '.json', 'w') as json_file:
            json.dump(data, json_file)
            json_file.close()

    except Exception as e:
        
        return e

    try:
        #write to text file
        with open(txt_filename + '.txt', 'w') as txt_file:
            
            for country, values in sorted(data.items()):

                for value_key, value in values.items():

                    gdp = value_key['GDP ($ per capita'].items()
                    businesses = value_key['businesses'].count()
                    industries = value_key['indstries'].count()
                    employees = value_key['estimated_employees'].items()

                    txt_file.write(country + ' has a total of ' + businesses + ' businesses ,an estimated ' + employees + 'employees, a total of ' + industries + 'industries , and total GDP of ' + gdp + '.')
            
            txt_file.close()

    except Exception as e:

        return e
    
    return 'Data successfully exported.'

data = csv_parser('countries')  

# pprint.pprint(data, indent=2)     #testing

a = json_parser('additional_stats', data)

# print(b)                          #execute testing

b = company_parser('companies', a)

c = country_stats('country_stats','summary', b)

# pprint.pprint(A, indent=3)
# company_parser('companies', data)
# c = 
pprint.pprint(c)