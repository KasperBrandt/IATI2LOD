## By Kasper Brandt
## Last updated on 21-05-2013

from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import RDF, RDFS, Literal, URIRef, Namespace, OWL
from rdflib.graph import Graph
import xml.etree.ElementTree as ET
import os, sys

# Settings
turtle_folder = "/media/Acer/School/IATI-data/mappings/"
dbpedia_file = "/media/Acer/School/IATI-data/mappings/dbpedia-countries.ttl"

if not os.path.isdir(turtle_folder):
    os.makedirs(turtle_folder)

# Namespaces
Iati = Namespace("http://purl.org/collections/iati/")

countries_oecd = Graph()
countries_oecd.bind('iati-country', "http://purl.org/collections/iati/codelist/Country/")
countries_oecd.bind('owl', "http://www.w3.org/2002/07/owl#")

countries_bfs = Graph()
countries_bfs.bind('iati-country', "http://purl.org/collections/iati/codelist/Country/")
countries_bfs.bind('bfs-country', "http://bfs.270a.info/code/1.0/CL_STATES_AND_TERRITORIES/")
countries_bfs.bind('owl', "http://www.w3.org/2002/07/owl#")

countries_ecb = Graph()
countries_ecb.bind('iati-country', "http://purl.org/collections/iati/codelist/Country/")
countries_ecb.bind('ecb-country', "http://ecb.270a.info/code/1.0/CL_AREA_EE/")
countries_ecb.bind('owl', "http://www.w3.org/2002/07/owl#")

countries_fao = Graph()
countries_fao.bind('iati-country', "http://purl.org/collections/iati/codelist/Country/")
countries_fao.bind('ecb-country', "http://fao.270a.info/code/0.1/CL_UN_COUNTRY/")
countries_fao.bind('owl', "http://www.w3.org/2002/07/owl#")

# Look up DBPedia entries from mapping file.
dbpedia_countries = []

with open(dbpedia_file, 'r') as f:
    for line in f:
        if "owl:sameAs" in line:
            line_list = line.split()
            dbpedia_countries.append((line_list[2].replace("dbpedia:", "http://dbpedia.org/resource/"),
                                      line_list[0].replace("iati-country:", "http://purl.org/collections/iati/codelist/Country/")))

total_countries = 0

found_countries_oecd = 0
not_found_oecd = []

found_countries_bfs = 0
not_found_bfs = []

found_countries_ecb = 0
not_found_ecb = []

found_countries_fao = 0
not_found_fao = []

for country in dbpedia_countries:
    found_oecd = False
    found_bfs = False
    found_ecb = False
    found_fao = False
    
    print "Looking for " + str(country[0])
    
    total_countries += 1
    
    sparql = SPARQLWrapper("http://oecd.270a.info/sparql")
    
    sparql.setQuery("""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        
        SELECT ?country ?country2
        WHERE { ?country skos:exactMatch <%s> .
        ?country skos:exactMatch ?country2 }
        """ % (country[0]))
    
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    for result in results["results"]["bindings"]:
        
        countries_oecd.add((URIRef(country[1]),
                            OWL.sameAs,
                            URIRef(result["country"]["value"])))
        
        found_oecd = True
        
        if "bfs.270a.info" in result["country2"]["value"]:
            countries_bfs.add((URIRef(country[1]),
                               OWL.sameAs,
                               URIRef(result["country2"]["value"])))
            
            found_bfs = True
            
        elif "ecb.270a.info" in result["country2"]["value"]:
            countries_ecb.add((URIRef(country[1]),
                               OWL.sameAs,
                               URIRef(result["country2"]["value"])))
            
            found_ecb = True
            
        elif "fao.270a.info" in result["country2"]["value"]:
            countries_fao.add((URIRef(country[1]),
                               OWL.sameAs,
                               URIRef(result["country2"]["value"])))
            
            found_fao = True
            
    if found_oecd:
        print "Found OECD mapping(s) for " + str(country[0])
        found_countries_oecd += 1
        
    else:
        not_found_oecd.append(country[0])
        
    if found_bfs:
        print "Found BFS mapping for " + str(country[0])
        found_countries_bfs += 1
        
    else:
        not_found_bfs.append(country[0])
        
    if found_ecb:
        print "Found ECB mapping for " + str(country[0])
        found_countries_ecb += 1
        
    else:
        not_found_ecb.append(country[0])
        
    if found_fao:
        print "Found FAO mapping for " + str(country[0])
        found_countries_fao += 1
        
    else:
        not_found_fao.append(country[0])
        
print
print "Adding to files..."

countries_turtle_oecd = countries_oecd.serialize(format='turtle')

with open(turtle_folder + 'oecd-countries.ttl', 'w') as turtle_file_oecd:
    turtle_file_oecd.write(countries_turtle_oecd)
    
countries_turtle_bfs = countries_bfs.serialize(format='turtle')

with open(turtle_folder + 'bfs-countries.ttl', 'w') as turtle_file_bfs:
    turtle_file_bfs.write(countries_turtle_bfs)
    
countries_turtle_ecb = countries_ecb.serialize(format='turtle')

with open(turtle_folder + 'ecb-countries.ttl', 'w') as turtle_file_ecb:
    turtle_file_ecb.write(countries_turtle_ecb)
    
countries_turtle_fao = countries_fao.serialize(format='turtle')

with open(turtle_folder + 'fao-countries.ttl', 'w') as turtle_file_fao:
    turtle_file_fao.write(countries_turtle_fao)

print
print "Total: " + str(total_countries)
print
print "Automatically found OECD: " + str(found_countries_oecd)

print
print "Could not automatically find OECD:"
for country in not_found_oecd:
    print str(country)
    
print
print "Automatically found BFS: " + str(found_countries_bfs)

print
print "Could not automatically find BFS:"
for country in not_found_bfs:
    print str(country)

print
print "Automatically found ECB: " + str(found_countries_ecb)

print
print "Could not automatically find ECB:"
for country in not_found_ecb:
    print str(country)
    
print
print "Automatically found FAO: " + str(found_countries_fao)

print
print "Could not automatically find FAO:"
for country in not_found_fao:
    print str(country)

