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
countries.bind('wbld-country', "http://worldbank.270a.info/classification/country/")
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
    code = country.find('code').text
    name = country.find('name').text
    
    sparql = SPARQLWrapper("http://worldbank.270a.info/sparql")
    
    sparql.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        
        SELECT ?country ?same
        WHERE { ?country rdf:type <http://dbpedia.org/ontology/Country> .
        ?country skos:notation "%s" .
        ?country owl:sameAs ?same . }
        """ % (code))
    
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    for result in results["results"]["bindings"]:
        
        countries.add((Iati['codelist/Country/' + code],
                       OWL.sameAs,
                       URIRef(result["country"]["value"])))
        
        if not "geonames" in result["same"]["value"]:
            
            countries.add((Iati['codelist/Country/' + code],
                           OWL.sameAs,
                           URIRef(result["same"]["value"])))
            
        found = True
    
    if found:
        found_countries += 1
        print "Found code " + code
    
    else:
        not_found.append((name, code))
        print "Did not find code " + code
        
# Adding mappings to file
print
print "Adding to file..."
countries_turtle = countries.serialize(format='turtle')

with open(turtle_folder + 'worldbank-countries.ttl', 'w') as turtle_file:
    turtle_file.write(countries_turtle)
    
print
print "Total: " + str(total_countries)
print "Automatically found: " + str(found_countries)

print
print "Could not automatically find:"
for country in not_found:
    print country[1] + ": " + country[0]
