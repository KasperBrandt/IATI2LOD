## By Kasper Brandt
## Last updated on 13-05-2013

from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import RDF, RDFS, Literal, URIRef, Namespace, OWL
from rdflib.graph import Graph
import xml.etree.ElementTree as ET
import os, sys

# Settings
turtle_folder = "/media/Acer/School/IATI-data/mappings/"
country_codelist = "/media/Acer/School/IATI2LOD/IATI2LOD/xml/codelists/Country.xml"

if not os.path.isdir(turtle_folder):
    os.makedirs(turtle_folder)

# Namespaces
Iati = Namespace("http://purl.org/collections/iati/")

countries = Graph()
countries.bind('iati-country', "http://purl.org/collections/iati/codelist/Country/")
countries.bind('cia', "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/")
countries.bind('owl', "http://www.w3.org/2002/07/owl#")
    
# Look up list of countries from codelists.
xml = ET.parse(country_codelist)
root = xml.getroot()

total_countries = 0
found_countries = 0
not_found = []

for country in root.findall('Country'):
    total_countries += 1
    code = country.find('code').text.lower()
    name = country.find('name').text
    
    cia_code = "." + code
    
    sparql = SPARQLWrapper("http://wifo5-03.informatik.uni-mannheim.de/factbook/sparql")
    
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?country
        WHERE { ?country <http://wifo5-04.informatik.uni-mannheim.de/factbook/ns#internetcountrycode> "%s" }
        """ % (cia_code))
    
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    link = ""

    for result in results["results"]["bindings"]:
        link = result["country"]["value"]
        found_countries += 1
        break
    
    print str(code) + ": " + str(link)
    
    if not link == "":
        countries.add((Iati['codelist/Country/' + code],
                       OWL.sameAs,
                       URIRef(link)))
    
    if link == "":
        not_found.append((name, code))
        
# Manually adding countries that could not be found
manual_add = [("ax", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/Finland"),
              ("bq", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/Netherlands"),
              ("cw", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/Netherlands"),
              ("fi", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/Finland"),
              ("fr", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/France"),
              ("gf", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/France"),
              ("gp", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/France"),
              ("mq", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/France"),
              ("mp", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/United_States"),
              ("ps", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/Israel"),
              ("re", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/France"),
              ("ru", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/Russia"),
              ("bl", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/France"),
              ("sh", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/Saint_Helena"),
              ("mf", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/France"),
              ("rs", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/Serbia"),
              ("sx", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/Netherlands"),
              ("ss", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/Sudan"),
              ("tl", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/East_Timor"),
              ("gb", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/United_Kingdom"),
              ("um", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/United_States")]

for country in manual_add:
    countries.add((Iati['codelist/Country/' + country[0]],
                   OWL.sameAs,
                   URIRef(country[1])))

# Adding mappings to file
print
print "Adding to file..."
countries_turtle = countries.serialize(format='turtle')

with open(turtle_folder + 'factbook-countries.ttl', 'w') as turtle_file:
    turtle_file.write(countries_turtle)

print
print "Total: " + str(total_countries)
print "Automatically found: " + str(found_countries)

print
print "Could not automatically find:"
for country in not_found:
    if (country[1] == 'cr') or (country[1] == 'so'):
        print country[1] + ": " + country[0] + ", could not be found at all..."
    else:
        print country[1] + ": " + country[0]