## By Kasper Brandt
## Last updated on 01-05-2013

from rdflib import RDF, RDFS, Literal, URIRef, Namespace, OWL
from rdflib.graph import Graph
import xml.etree.ElementTree as ET
import os, sys, httplib2, urllib, datetime, AddProvenance

# Settings
turtle_folder = "/media/Acer/School/IATI-data/mappings/Geonames/"
country_codelist = "/media/Acer/School/IATI-data/xml/codelists/Country.xml"
webservice = "http://api.geonames.org/search?"
username = "KasperBrandt"

Iati = Namespace("http://purl.org/collections/iati/")
GN = Namespace("http://sws.geonames.org/")


if not os.path.isdir(turtle_folder):
    os.makedirs(turtle_folder)

start_time = datetime.datetime.now()

countries = Graph()
countries.bind('iati', "http://purl.org/collections/iati/")
countries.bind('gn', "http://sws.geonames.org/")
countries.bind('owl', "http://www.w3.org/2002/07/owl#")

feature_codes = dict([('PCLI', 0),
                      ('PCLD', 0),
                      ('TERR', 0),
                      ('PCL', 0),
                      ('PCLF', 0),
                      ('PCLIX', 0),
                      ('PCLS', 0),
                      ('PCLH', 0)])

found_count = 0
not_found_count = 0
not_found = []
total = 0

# Look up list of countries from codelists.
xml = ET.parse(country_codelist)
root = xml.getroot()

for country in root.findall('Country'):
    code = country.find('code').text
    name = country.find('name').text
    
    print "Processing: " + code + "..."
    total += 1
    
    url = webservice + "username=" + username + "&country=" + str(code)
    
    for feature_code in feature_codes.keys():
        url = url + "&featureCode=" + feature_code
    
    try:
        response, content = httplib2.Http().request(url, "GET")
        
    except httplib2.ServerNotFoundError as e:
        print e
        sys.exit(0)
        
    geonames_xml = ET.fromstring(content)
    
    count = geonames_xml.find('totalResultsCount').text
    
    if count == '0':
        print "Code " + code + " not found..."
        not_found.append((code, name))
        not_found_count += 1
        
    elif count == '1':
        geoname = geonames_xml.find('geoname')
        geonames_code = geoname.find('geonameId').text
        geonames_fcode = geoname.find('fcode').text
        
        countries.add((Iati['codelist/Country/' + code],
                       OWL.sameAs,
                       GN[geonames_code]))
        
        feature_codes[geonames_fcode] += 1
        found_count += 1
        
    else:
        found = False
        
        if geoname.findall('geoname') == []:
            print "Code " + code + " not found..."
            not_found.append((code, name))
            not_found_count += 1
        
        else:
            for element in geoname.findall('geoname'):
                if element.find('fcode') == 'PCLI':
                    geonames_code = element.find('geonameId').text
                    
                    countries.add((Iati['codelist/Country/' + code],
                                   OWL.sameAs,
                                   GN[geonames_code]))
                    
                    feature_codes['PCLI'] += 1
                    found = True
                    found_count += 1
        
                if (element.find('fcode') == 'PCLD') and (not found == True):
                    geonames_code = element.find('geonameId').text
                    
                    countries.add((Iati['codelist/Country/' + code],
                                   OWL.sameAs,
                                   GN[geonames_code]))
                    
                    feature_codes['PCLD'] += 1
                    Found = True
                    found_count += 1
                    
                if (element.find('fcode') == 'Terr') and (not found == True):
                    geonames_code = element.find('geonameId').text
                    
                    countries.add((Iati['codelist/Country/' + code],
                                   OWL.sameAs,
                                   GN[geonames_code]))
                    
                    feature_codes['Terr'] += 1
                    Found = True
                    found_count += 1
                    
                if (element.find('fcode') == 'PCL') and (not found == True):
                    geonames_code = element.find('geonameId').text
                    
                    countries.add((Iati['codelist/Country/' + code],
                                   OWL.sameAs,
                                   GN[geonames_code]))
                    
                    feature_codes['PCL'] += 1
                    Found = True
                    found_count += 1
                    
                if (element.find('fcode') == 'PCLF') and (not found == True):
                    geonames_code = element.find('geonameId').text
                    
                    countries.add((Iati['codelist/Country/' + code],
                                   OWL.sameAs,
                                   GN[geonames_code]))
                    
                    feature_codes['PCLF'] += 1
                    Found = True
                    found_count += 1
                    
                if (element.find('fcode') == 'PCLIX') and (not found == True):
                    geonames_code = element.find('geonameId').text
                    
                    countries.add((Iati['codelist/Country/' + code],
                                   OWL.sameAs,
                                   GN[geonames_code]))
                    
                    feature_codes['PCLIX'] += 1
                    Found = True
                    found_count += 1
                    
                if (element.find('fcode') == 'PCLS') and (not found == True):
                    geonames_code = element.find('geonameId').text
                    
                    countries.add((Iati['codelist/Country/' + code],
                                   OWL.sameAs,
                                   GN[geonames_code]))
                    
                    feature_codes['PCLS'] += 1
                    Found = True
                    found_count += 1
                    
                if (element.find('fcode') == 'PCLH') and (not found == True):
                    geonames_code = element.find('geonameId').text
                    
                    countries.add((Iati['codelist/Country/' + code],
                                   OWL.sameAs,
                                   GN[geonames_code]))
                    
                    feature_codes['PCLH'] += 1
                    Found = True
                    found_count += 1
                    
                else:
                    print "Scenario not possible, something went wrong..."
                    not_found_count += 1
                
print "Searching for codes not found..."

not_found_again = []

for not_found_country in not_found:
    
    print "Looking for: " + not_found_country[1] + "..."

    params = dict([('username', username),
                   ('q', not_found_country[1])])
    
    params_encoded = urllib.urlencode(params)
    
    url = webservice + params_encoded
    
    try:
        response, content = httplib2.Http().request(url, "GET")
        
    except httplib2.ServerNotFoundError as e:
        print e
        sys.exit(0)
     
    if not content == None:
        
        geonames_xml = ET.fromstring(content)
        results = geonames_xml.find('totalResultsCount')
        
        if (not results.text == '0') and (not results.text == None):
            geoname = geonames_xml.find('geoname')
            geonames_code = geoname.find('geonameId').text
            
            countries.add((Iati['codelist/Country/' + not_found_country[0]],
                           OWL.sameAs,
                           GN[geonames_code]))
            
            found_count += 1
            not_found_count -= 1
            
        else:
            not_found_again.append((not_found_country[0], not_found_country[1]))
    else:
        not_found_again.append((not_found_country[0], not_found_country[1]))

print "Adding to file..."
countries_turtle = countries.serialize(format='turtle')

with open(turtle_folder + 'geonames-countries.ttl', 'w') as turtle_file:
    turtle_file.write(countries_turtle)

# Add provenance
provenance = Graph()

provenance = AddProvenance.addProv(Iati,
                                   provenance,
                                   'Geonames',
                                   start_time,
                                   "http://sws.geonames.org/",
                                   ['Geonames'],
                                   "mapping%20scripts/GeonamesCountries.py")

provenance_turtle = provenance.serialize(format='turtle')

with open(turtle_folder + 'provenance-geonames-countries.ttl', 'w') as turtle_file:
    turtle_file.write(provenance_turtle)

print
print "Total countries: " + str(total)
print "Done, found: " + str(found_count) + ", not found: " + str(not_found_count) + "."

print
print "Could not find:"
for item in not_found_again:
    print item[0], item[1]

print
print "Summary:"
for key in feature_codes.keys():
    print key, feature_codes[key]

print
print "Done!"