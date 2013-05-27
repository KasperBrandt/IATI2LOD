## By Kasper Brandt
## Last updated on 25-05-2013

from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import RDF, RDFS, Literal, URIRef, Namespace, OWL
from rdflib.graph import Graph
import xml.etree.ElementTree as ET
import os, sys, datetime, AddProvenance

# Settings
turtle_folder = "/media/Acer/School/IATI-data/mappings/Transparency/"
country_codelist = "/media/Acer/School/IATI-data/xml/codelists/Country.xml"

if not os.path.isdir(turtle_folder):
    os.makedirs(turtle_folder)
    
start_time = datetime.datetime.now()

# Namespaces
Iati = Namespace("http://purl.org/collections/iati/")

countries = Graph()
countries.bind('iati-country', "http://purl.org/collections/iati/codelist/Country/")
countries.bind('transparency-country', "http://transparency.270a.info/classification/country/")
countries.bind('owl', "http://www.w3.org/2002/07/owl#")

# Get all countries
print "Retrieving country list..."

sparql = SPARQLWrapper("http://transparency.270a.info/sparql")

sparql.setQuery("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX transparency: <http://transparency.270a.info/classification/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    
    SELECT ?country ?code
    WHERE { ?country skos:topConceptOf transparency:country .
    ?country skos:notation ?code . }
    """)

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

#print results
#sys.exit(0)

total_countries = 0
found_countries = 0
not_found_countries = 0
not_found = []

# Look up list of countries from codelists.
xml = ET.parse(country_codelist)
root = xml.getroot()

for country in root.findall('Country'):
    found = False
    
    total_countries += 1
    code = country.find('code').text
    name = country.find('name').text.title()
    
    print "Looking for code " + str(code) + ", " + str(name) + "..."
    
    for result in results["results"]["bindings"]:
        if code in result["code"]["value"]:
            found = True
            
            link = result["country"]["value"]
            
            print "Found code: " + str(link)
            
            countries.add((Iati['codelist/Country/' + code],
                           OWL.sameAs,
                           URIRef(link)))
            
            found_countries += 1
            
    if not found:
        not_found.append((name, code))
        not_found_countries += 1
            

# Adding mappings to file
print
print "Adding to file..."
countries_turtle = countries.serialize(format='turtle')

with open(turtle_folder + 'transparency-countries.ttl', 'w') as turtle_file:
    turtle_file.write(countries_turtle)
    
# Add provenance
provenance = Graph()

provenance = AddProvenance.addProv(Iati,
                                   provenance,
                                   'Transparency',
                                   start_time,
                                   "",
                                   ['Transparency'],
                                   "mapping%20scripts/TransparencyCountries.py")

provenance_turtle = provenance.serialize(format='turtle')

with open(turtle_folder + 'provenance-transparency.ttl', 'w') as turtle_file:
    turtle_file.write(provenance_turtle)
    
print
print "Added provenance..."

print
print "Total: " + str(total_countries)
print "Done, found: " + str(found_countries) + ", not found: " + str(not_found_countries) + "."

print
print "Could not automatically find:"
for country in not_found:
    print country[1] + ": " + country[0]