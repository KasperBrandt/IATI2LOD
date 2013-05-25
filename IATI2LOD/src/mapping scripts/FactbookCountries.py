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

countries_db = Graph()
countries_db.bind('iati-country', "http://purl.org/collections/iati/codelist/Country/")
countries_db.bind('dbpedia', "http://dbpedia.org/resource/")
countries_db.bind('owl', "http://www.w3.org/2002/07/owl#")

# Retrieve CIA Factbook information
print "Connecting to CIA Factbook..."

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

# Retrieve DBPedia information
print "Connecting to DBPedia..."

sparql_db = SPARQLWrapper("http://dbpedia.org/sparql")

sparql_db.setQuery("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    
    SELECT ?country ?same
    WHERE { ?country rdf:type dbpedia-owl:Country .
    ?country owl:sameAs ?same . }
    """)

sparql_db.setReturnFormat(JSON)
results_db = sparql_db.query().convert()

# Look up list of countries from codelists.
xml = ET.parse(country_codelist)
root = xml.getroot()

total_countries = 0
found_countries = 0
found_countries_db = 0
not_found = []
not_found_db = []

for country in root.findall('Country'):
    found = False
    found_db = False
    
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
    
    if found:
        link_resource = link.rsplit('/', 1)[1]

        link_db = "http://www4.wiwiss.fu-berlin.de/factbook/resource/" + str(link_resource)
        
        for result in results_db["results"]["bindings"]:
            
            if link_db == result["same"]["value"]:
                link_db_country = str(result["country"]["value"])
                
                countries_db.add((Iati['codelist/Country/' + code],
                                  OWL.sameAs,
                                  URIRef(link_db_country)))
                
                print "Found on DBPedia: " + str(link_db_country)
                
                found_countries_db += 1
                found_db = True
    
    if not found:
        not_found.append((name, code))
        
    if not found_db:
        not_found_db.append((name, code))

# Retrieve DBPedia information
print
print "Connecting to DBPedia again..."

sparql_db2 = SPARQLWrapper("http://dbpedia.org/sparql")

sparql_db2.setQuery("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?country ?code
    WHERE { ?country rdf:type dbpedia-owl:Country .
    ?country <http://dbpedia.org/property/cctld> ?code }
    """)

sparql_db2.setReturnFormat(JSON)
results_db2 = sparql_db2.query().convert()

not_found_db2 = []

for not_found_in_db in not_found_db:
    found_db2 = False
    print "Looking for code " + str(not_found_in_db[1]) + "..."
    
    country_code = "." + not_found_in_db[1]
    
    for result in results_db2["results"]["bindings"]:
        if country_code in result["code"]["value"]:
            link = result["country"]["value"]
            
            print "Found code " + str(not_found_in_db[1]) + ", link: " + str(link)
            
            countries_db.add((Iati['codelist/Country/' + not_found_in_db[1]],
                              OWL.sameAs,
                              URIRef(link)))
            
            found_countries_db += 1
            found_db2 = True

            break
        
    if not found_db2:
        not_found_db2.append(not_found_in_db)
        
        

# Adding mappings to file
print
print "Adding to file..."
countries_turtle = countries.serialize(format='turtle')

with open(turtle_folder + 'factbook-countries.ttl', 'w') as turtle_file:
    turtle_file.write(countries_turtle)
    
countries_turtle_db = countries_db.serialize(format='turtle')

with open(turtle_folder + 'dbpedia-countries.ttl', 'w') as turtle_file_db:
    turtle_file_db.write(countries_turtle_db)

print
print "Total: " + str(total_countries)
print "Automatically found: " + str(found_countries)

print
print "Could not automatically find:"
for country in not_found:
    print country[1] + ": " + country[0]
    
print
print "Total: " + str(total_countries)
print "Automatically found: " + str(found_countries_db)

print
print "Could not automatically find:"
for country in not_found_db2:
    print country[1] + ": " + country[0]