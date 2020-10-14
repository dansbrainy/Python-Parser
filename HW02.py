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

        json_file.close()
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

                    
                    parsed_data[country]['estimated_employees'] += total_employee

                else:
                    # create a new array in this slot
                    parsed_data[country]['businesses'] = [business]
                    parsed_data[country]['industries']= [industry]
                    parsed_data[country]['estimated_employees'] = total_employee
                    
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
            json.dump(data, json_file, sort_keys=True, indent=3)
            json_file.close()

    except Exception as e:
        
        return e

    try:
        #write to text file
        with open(txt_filename + '.txt', 'w') as txt_file:
            
            # FORMAT OF DATA PARSED
            # 'Zimbabwe': {'GDP ($ per capita)': 1900,
            #   'businesses': ['Econet Wireless Zimbabwe',
            #                  'Jewson',
            #                  'Delta Beverages Pvt Ltd',
            #                  'University Of Zimbabwe',
            #                  'Telone Zimbabwe (pvt) Ltd',
            #                  'Midlands State University',
            #                  'Cbz Bank Ltd',
            #                  'Skills Funding Agency',
            #                  'Voyage Care Ltd',
            #                  'Telecel Zimbabwe',
            #                  'Cabs',
            #                  'Orbit Group',
            #                  'National University Of Science & Technology',
            #                  'Ishida Europe Ltd',
            #                  'Barhale Plc',
            #                  'Steward Bank',
            #                  'Edgars Stores Zimbabwe',
            #                  'Harare Institute Of Technology',
            #                  "Loughborough Students' Union",
            #                  'Dudley College',
            #                  'Schweppes Zimbabwe Ltd',
            #                  'Riozim Ltd',
            #                  'Pertemps People Development Group',
            #                  'Zb Financial Holdings Limited',
            #                  'Cimas Medical Aid Society',
            #                  'Netone Cellular Private Limited',
            #                  'Kingdom Financial Holdings Ltd',
            #                  'Ttcs Global'],
            #   'estimated_employees': 245,
            #   'industries': ['telecommunications',
            #                  'building materials',
            #                  'food & beverages',
            #                  'higher education',
            #                  'telecommunications',
            #                  'education management',
            #                  'banking',
            #                  'government relations',
            #                  'hospital & health care',
            #                  'telecommunications',
            #                  'financial services',
            #                  'non-profit organization management',
            #                  'higher education',
            #                  'machinery',
            #                  'civil engineering',
            #                  'banking',
            #                  'retail',
            #                  'education management',
            #                  'education management',
            #                  'food & beverages',
            #                  'mining & metals',
            #                  'staffing and recruiting',
            #                  'financial services',
            #                  'telecommunications',
            #                  'banking',
            #                  'information technology and services']}

            for country in sorted(data.keys()):

                businesses = len(data[country]['businesses'])
                industries = len(data[country]['industries'])
                gdp = data[country]['GDP ($ per capita)']
                employees = data[country]['estimated_employees']

                txt_file.write(country + ' has a total of ' + str(businesses) + ' businesses, an estimated ' + str(employees) + ' employees, a total of ' + str(industries) +' industries, and total GDP of ' + str(gdp) + '. \n')

            txt_file.close()

    except Exception as e:

        return e
    
    return 'Data successfully exported.'


def inequality(region, gini_val):

    result = {}
    string = 'The given region was not found.'

    # try:
    response = requests.get('https://restcountries.eu/rest/v2/region/' + region)

    if response.status_code != 200:
        return string
    else:
        
        data = json.loads(response.text)  # parse json to dict

        for country in data:

            gini = country['gini']
            name = country['name']
            
            if gini != None and gini > gini_val:

                # result[name] = gini

                result.setdefault(name, gini)

                return result

            # else:

            #     string = "The gini provided is higher than all " + region + "'s ginis"
    
            #     return string


        # FORMAT OF DATA
        #     'latlng': [49.75, 6.16666666],
        #     'name': 'Luxembourg',
        #     'nativeName': 'Luxembourg',
        #     'numericCode': '442',
        #     'population': 576200,
        #     'region': 'Europe',
        #     'regionalBlocs': [ { 'acronym': 'EU',
        #                         'name': 'European Union',
        #                         'otherAcronyms': [],
        #                         'otherNames': []}],
        #     'subregion': 'Western Europe',
        #     'timezones': ['UTC+01:00'],
        #     'topLevelDomain': ['.lu'],
        #     'translations': { 'br': 'Luxemburgo',
        #                     'de': 'Luxemburg',
        #                     'es': 'Luxemburgo',
        #                     'fa': 'لوکزامبورگ',
        #                     'fr': 'Luxembourg',
        #                     'hr': 'Luksemburg',
        #                     'it': 'Lussemburgo',
        #                     'ja': 'ルクセンブルク',
        #                     'nl': 'Luxemburg',
        #                     'pt': 'Luxemburgo'}},
        # { 'alpha2Code': 'MK',
        #     'alpha3Code': 'MKD',
        #     'altSpellings': ['MK', 'Republic of Macedonia', 'Република Македонија'],
        #     'area': 25713.0,
        #     'borders': ['ALB', 'BGR', 'GRC', 'KOS', 'SRB'],
        #     'callingCodes': ['389'],
        #     'capital': 'Skopje',
        #     'cioc': 'MKD',
        #     'currencies': [ { 'code': 'MKD',
        #                     'name': 'Macedonian denar',
        #                     'symbol': 'ден'}],
        #     'demonym': 'Macedonian',
        #     'flag': 'https://restcountries.eu/data/mkd.svg',
        #     'gini': 43.2,
        #     'languages': [ { 'iso639_1': 'mk',
        #                     'iso639_2': 'mkd',
        #                     'name': 'Macedonian',
        #                     'nativeName': 'македонски јазик'}],

            # print(data)
            # return data
    # except Exception as e:
    #     return e
    

    # print(response)

    # return result


# --------------------------
# EXECUSION AND RUNNING
# --------------------------

# data = csv_parser('countries')  

# pprint.pprint(data, indent=2)     #testing

# data = json_parser('additional_stats', data)

# print(b)                          #execute testing

# data = company_parser('companies', data)

# data = country_stats('country_stats','summary', data)

# pprint.pprint(data)

# inequality('Africa', 63.9)
s = inequality('Europe', 40.9)

pprint.pprint(s)