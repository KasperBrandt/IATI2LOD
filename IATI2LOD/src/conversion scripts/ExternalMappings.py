## By Kasper Brandt
## Last updated on 29-04-2013

from rdflib import RDF, RDFS, Literal, URIRef, Namespace, OWL
from rdflib.graph import Graph
import os

graph = Graph()
graph.bind('iati', "http://purl.org/collections/iati/")
graph.bind('skos', "http://www.w3.org/2008/05/skos#")
graph.bind('dct', "http://purl.org/dc/terms/")
graph.bind('foaf', "http://xmlns.com/foaf/0.1/")
graph.bind('org', "http://www.w3.org/ns/org#")
graph.bind('geo', "http://www.w3.org/2003/01/geo/wgs84_pos#")
graph.bind('cc', "http://creativecommons.org/ns#")

Iati = Namespace("http://purl.org/collections/iati/")
SKOS = Namespace("http://www.w3.org/2008/05/skos#")
DC = Namespace("http://purl.org/dc/terms/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
ORG = Namespace("http://www.w3.org/ns/org#")
GEO = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
CC = Namespace ("http://creativecommons.org/ns#")

turtle_folder = "/media/Acer/School/IATI-data/mappings/"

if not os.path.isdir(turtle_folder):
    os.makedirs(turtle_folder)

#########     SKOS    #########

print "Add SKOS mappings..."

# Classes
graph.add((Iati['codelist'],
           RDFS.subClassOf,
           SKOS['ConceptScheme']))

graph.add((Iati['codelist-code'],
           RDFS.subClassOf,
           SKOS['Concept']))

graph.add((Iati['codelist-category'],
           RDFS.subClassOf,
           SKOS['Concept']))

# Properties
graph.add((Iati['member-codelist'],
           RDFS.subPropertyOf,
           SKOS['inScheme']))

graph.add((Iati['codelist-member-category'],
           RDFS.subPropertyOf,
           SKOS['broader']))


#########     DC    #########

print "Add DC mappings..."

# Classes
graph.add((Iati['period'],
           RDFS.subClassOf,
           DC['PeriodOfTime']))

# Properties
graph.add((Iati['activity-id'],
           RDFS.subPropertyOf,
           DC['identifier']))

graph.add((Iati['source-document-id'],
           RDFS.subPropertyOf,
           DC['identifier']))

graph.add((Iati['language'],
           RDFS.subPropertyOf,
           DC['language']))

graph.add((Iati['format'],
           RDFS.subPropertyOf,
           DC['hasFormat']))

graph.add((Iati['resources-mimetype'],
           RDFS.subPropertyOf,
           DC['format']))

graph.add((Iati['description-text'],
           RDFS.subPropertyOf,
           DC['description']))

graph.add((Iati['resources-description'],
           RDFS.subPropertyOf,
           DC['description']))

graph.add((Iati['date'],
           RDFS.subPropertyOf,
           DC['date']))

graph.add((Iati['iso-date'],
           RDFS.subPropertyOf,
           DC['date']))

graph.add((Iati['value-date'],
           RDFS.subPropertyOf,
           DC['date']))

graph.add((Iati['last-updated'],
           RDFS.subPropertyOf,
           DC['modified']))

graph.add((Iati['version'],
           RDFS.subPropertyOf,
           DC['hasVersion']))

graph.add((Iati['source-document-version'],
           RDFS.subPropertyOf,
           DC['hasVersion']))

graph.add((Iati['source-document-download-url'],
           RDFS.subPropertyOf,
           DC['source']))


#########     FOAF    #########

print "Add FOAF mappings..."

# Classes
graph.add((Iati['contact-info'],
           RDFS.subClassOf,
           FOAF['Agent']))

graph.add((Iati['author'],
           RDFS.subClassOf,
           FOAF['Agent']))

graph.add((Iati['maintainer'],
           RDFS.subClassOf,
           FOAF['Agent']))

# Properties
graph.add((Iati['contact-info-person-name'],
           RDFS.subPropertyOf,
           FOAF['name']))

graph.add((Iati['author-name'],
           RDFS.subPropertyOf,
           FOAF['name']))

graph.add((Iati['maintainer-name'],
           RDFS.subPropertyOf,
           FOAF['name']))

graph.add((Iati['contact-info-telephone'],
           RDFS.subPropertyOf,
           FOAF['phone']))

graph.add((Iati['contact-info-email'],
           RDFS.subPropertyOf,
           FOAF['mbox']))

graph.add((Iati['author-email'],
           RDFS.subPropertyOf,
           FOAF['mbox']))

graph.add((Iati['maintainer-email'],
           RDFS.subPropertyOf,
           FOAF['mbox']))

graph.add((Iati['source-document-author'],
           RDFS.subPropertyOf,
           FOAF['creator']))


#########     ORG    #########

print "Add ORG mappings..."

# Classes
graph.add((Iati['organisation'],
           RDFS.subClassOf,
           ORG['Organization']))

# Properties
graph.add((Iati['contact-info-organisation'],
           RDFS.subPropertyOf,
           ORG['memberOf']))

graph.add((Iati['organisation-id'],
           RDFS.subPropertyOf,
           ORG['identifier']))


#########     GEO    #########

print "Add GEO mappings..."

# Classes
graph.add((Iati['region'],
           RDFS.subClassOf,
           GEO['location']))

graph.add((Iati['country'],
           RDFS.subClassOf,
           GEO['location']))

graph.add((Iati['location'],
           RDFS.subClassOf,
           GEO['location']))

# Properties
graph.add((Iati['latitude'],
           RDFS.subPropertyOf,
           GEO['lat']))

graph.add((Iati['longitude'],
           RDFS.subPropertyOf,
           GEO['long']))


#########     CC    #########

print "Add CC mappings..."

# Properties
graph.add((Iati['source-document-license'],
           RDFS.subPropertyOf,
           CC['license']))


#########     Finalize    #########

graph_turtle = graph.serialize(format='turtle')

print "Writing to file..."

with open(turtle_folder + 'mappings.ttl', 'w') as turtle_file:
    turtle_file.write(graph_turtle)
    
print "Done!"