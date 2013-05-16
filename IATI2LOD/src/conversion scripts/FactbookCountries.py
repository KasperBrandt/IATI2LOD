## By Kasper Brandt
## Last updated on 16-05-2013

from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import RDF, RDFS, Literal, URIRef, Namespace, OWL
from rdflib.graph import Graph
import xml.etree.ElementTree as ET
import os, sys

# Settings
turtle_folder = "/media/Acer/School/IATI-data/mappings/"
country_codelist = "/media/Acer/School/IATI-data/xml/codelists/Country.xml"

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
    found = False
    
    total_countries += 1
    code = country.find('code').text.lower()
    name = country.find('name').text
    
    cia_code = "." + code
    
    print "Looking for code " + code + "..."
    
    # Municipalities of The Netherlands:
    if cia_code == ".bq" or cia_code == ".cw" or cia_code == ".sx":
        cia_code = ".nl"
        
    # Municipalities of France:
    elif cia_code == ".bl" or cia_code == ".mf":
        cia_code = ".fr"
        
    # United Kingdom exception:
    elif cia_code == ".gb":
        cia_code = ".uk"
    
    sparql = SPARQLWrapper("http://wifo5-03.informatik.uni-mannheim.de/factbook/sparql")
    
    sparql.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?country ?code
        WHERE { ?country rdf:type <http://wifo5-04.informatik.uni-mannheim.de/factbook/ns#Country> .
        ?country <http://wifo5-04.informatik.uni-mannheim.de/factbook/ns#internetcountrycode> ?code . }
        """)
    
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    link = ""

    for result in results["results"]["bindings"]:
        if cia_code in result["code"]["value"]:
            link = result["country"]["value"]
            
            print "Found code " + code + ", link: " + str(link)
            
            countries.add((Iati['codelist/Country/' + code],
                           OWL.sameAs,
                           URIRef(link)))
            
            found_countries += 1
            found = True
            break
    
    if not found:
        not_found.append((name, code))
        
# Manually adding countries that could not be found
#manual_add = [("ax", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/Finland"),
#              ("bq", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/Netherlands"),
#              ("cw", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/Netherlands"),
#              ("fi", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/Finland"),
#              ("fr", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/France"),
#              ("gf", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/France"),
#              ("gp", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/France"),
#              ("mq", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/France"),
#              ("mp", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/United_States"),
#              ("ps", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/Israel"),
#              ("re", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/France"),
#              ("ru", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/Russia"),
#              ("bl", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/France"),
#              ("sh", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/Saint_Helena"),
#              ("mf", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/France"),
#              ("rs", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/Serbia"),
#              ("sx", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/Netherlands"),
#              ("ss", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/Sudan"),
#              ("tl", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/East_Timor"),
#              ("gb", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/United_Kingdom"),
#              ("um", "http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/United_States")]
#
#for country in manual_add:
#    countries.add((Iati['codelist/Country/' + country[0]],
#                   OWL.sameAs,
#                   URIRef(country[1])))

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
#    if (country[1] == 'cr') or (country[1] == 'so'):
#        print country[1] + ": " + country[0] + ", could not be found at all..."
#    else:
    print country[1] + ": " + country[0]