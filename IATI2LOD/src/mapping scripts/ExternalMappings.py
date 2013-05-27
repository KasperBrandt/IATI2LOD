## By Kasper Brandt
## Last updated on 29-04-2013

from rdflib import RDF, RDFS, Literal, URIRef, Namespace, OWL
from rdflib.graph import Graph
import os, datetime, AddProvenance

start_time = datetime.datetime.now()

graph_skos = Graph()
graph_skos.bind('iati', "http://purl.org/collections/iati/")
graph_skos.bind('skos', "http://www.w3.org/2008/05/skos#")

graph_dct = Graph()
graph_dct.bind('iati', "http://purl.org/collections/iati/")
graph_dct.bind('dct', "http://purl.org/dc/terms/")

graph_foaf = Graph()
graph_foaf.bind('iati', "http://purl.org/collections/iati/")
graph_foaf.bind('foaf', "http://xmlns.com/foaf/0.1/")

graph_org = Graph()
graph_org.bind('iati', "http://purl.org/collections/iati/")
graph_org.bind('org', "http://www.w3.org/ns/org#")

graph_geo = Graph()
graph_geo.bind('iati', "http://purl.org/collections/iati/")
graph_geo.bind('geo', "http://www.w3.org/2003/01/geo/wgs84_pos#")

graph_cc = Graph()
graph_cc.bind('iati', "http://purl.org/collections/iati/")
graph_cc.bind('cc', "http://creativecommons.org/ns#")

Iati = Namespace("http://purl.org/collections/iati/")
SKOS = Namespace("http://www.w3.org/2008/05/skos#")
DC = Namespace("http://purl.org/dc/terms/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
ORG = Namespace("http://www.w3.org/ns/org#")
GEO = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
CC = Namespace ("http://creativecommons.org/ns#")

turtle_folder = "/media/Acer/School/IATI-data/mappings/Schema/"

if not os.path.isdir(turtle_folder):
    os.makedirs(turtle_folder)

#########     SKOS    #########

print "Add SKOS mappings..."

# Classes
graph_skos.add((Iati['codelist'],
                RDFS.subClassOf,
                SKOS['ConceptScheme']))

graph_skos.add((Iati['codelist-code'],
                RDFS.subClassOf,
                SKOS['Concept']))

graph_skos.add((Iati['codelist-category'],
                RDFS.subClassOf,
                SKOS['Concept']))

# Properties
graph_skos.add((Iati['member-of-codelist'],
                RDFS.subPropertyOf,
                SKOS['inScheme']))

graph_skos.add((Iati['codelist-member-category'],
                RDFS.subPropertyOf,
                SKOS['broader']))

graph_skos.add((Iati['has-member'],
                RDFS.subPropertyOf,
                SKOS['narrower']))


#########     DC    #########

print "Add DC mappings..."

# Classes
graph_dct.add((Iati['period'],
               RDFS.subClassOf,
               DC['PeriodOfTime']))

# Properties
graph_dct.add((Iati['activity-id'],
               RDFS.subPropertyOf,
               DC['identifier']))

graph_dct.add((Iati['source-document-id'],
               RDFS.subPropertyOf,
               DC['identifier']))

graph_dct.add((Iati['language'],
               RDFS.subPropertyOf,
               DC['language']))

graph_dct.add((Iati['format'],
               RDFS.subPropertyOf,
               DC['hasFormat']))

graph_dct.add((Iati['resources-mimetype'],
               RDFS.subPropertyOf,
               DC['format']))

graph_dct.add((Iati['description-text'],
               RDFS.subPropertyOf,
               DC['description']))

graph_dct.add((Iati['resources-description'],
               RDFS.subPropertyOf,
               DC['description']))

graph_dct.add((Iati['date'],
               RDFS.subPropertyOf,
               DC['date']))

graph_dct.add((Iati['iso-date'],
               RDFS.subPropertyOf,
               DC['date']))

graph_dct.add((Iati['value-date'],
               RDFS.subPropertyOf,
               DC['date']))

graph_dct.add((Iati['baseline-year'],
               RDFS.subPropertyOf,
               DC['date']))

graph_dct.add((Iati['value-date'],
               RDFS.subPropertyOf,
               DC['date']))

graph_dct.add((Iati['start-actual-date'],
               RDFS.subPropertyOf,
               DC['date']))

graph_dct.add((Iati['end-actual-date'],
               RDFS.subPropertyOf,
               DC['date']))

graph_dct.add((Iati['start-planned-date'],
               RDFS.subPropertyOf,
               DC['date']))

graph_dct.add((Iati['end-planned-date'],
               RDFS.subPropertyOf,
               DC['date']))

graph_dct.add((Iati['start-date'],
               RDFS.subPropertyOf,
               DC['date']))

graph_dct.add((Iati['end-date'],
               RDFS.subPropertyOf,
               DC['date']))

graph_dct.add((Iati['last-updated'],
               RDFS.subPropertyOf,
               DC['modified']))

graph_dct.add((Iati['updated'],
               RDFS.subPropertyOf,
               DC['modified']))

graph_dct.add((Iati['version'],
               RDFS.subPropertyOf,
               DC['hasVersion']))

graph_dct.add((Iati['source-document-version'],
               RDFS.subPropertyOf,
               DC['hasVersion']))

graph_dct.add((Iati['source-document-download-url'],
               RDFS.subPropertyOf,
               DC['source']))

graph_dct.add((Iati['source-document-author'],
               RDFS.subPropertyOf,
               DC['creator']))

graph_dct.add((Iati['source-document-maintainer'],
               RDFS.subPropertyOf,
               DC['contributor']))

graph_dct.add((Iati['extras-iati-publisher-id'],
               RDFS.subPropertyOf,
               DC['publisher']))

graph_dct.add((Iati['extras-language'],
               RDFS.subPropertyOf,
               DC['language']))

#########     FOAF    #########

print "Add FOAF mappings..."

# Classes
graph_foaf.add((Iati['contact-info'],
                RDFS.subClassOf,
                FOAF['Agent']))

graph_foaf.add((Iati['author'],
                RDFS.subClassOf,
                FOAF['Agent']))

graph_foaf.add((Iati['maintainer'],
                RDFS.subClassOf,
                FOAF['Agent']))

# Properties
graph_foaf.add((Iati['contact-info-person-name'],
                RDFS.subPropertyOf,
                FOAF['name']))

graph_foaf.add((Iati['author-name'],
                RDFS.subPropertyOf,
                FOAF['name']))

graph_foaf.add((Iati['maintainer-name'],
                RDFS.subPropertyOf,
                FOAF['name']))

graph_foaf.add((Iati['contact-info-telephone'],
                RDFS.subPropertyOf,
                FOAF['phone']))

graph_foaf.add((Iati['contact-info-email'],
                RDFS.subPropertyOf,
                FOAF['mbox']))

graph_foaf.add((Iati['author-email'],
                RDFS.subPropertyOf,
                FOAF['mbox']))

graph_foaf.add((Iati['maintainer-email'],
                RDFS.subPropertyOf,
                FOAF['mbox']))


#########     ORG    #########

print "Add ORG mappings..."

# Classes
graph_org.add((Iati['organisation'],
               RDFS.subClassOf,
               ORG['Organization']))

# Properties
graph_org.add((Iati['contact-info-organisation'],
               RDFS.subPropertyOf,
               ORG['memberOf']))

graph_org.add((Iati['organisation-id'],
               RDFS.subPropertyOf,
               ORG['identifier']))


#########     GEO    #########

print "Add GEO mappings..."

# Classes
graph_geo.add((Iati['region'],
               RDFS.subClassOf,
               GEO['location']))

graph_geo.add((Iati['country'],
               RDFS.subClassOf,
               GEO['location']))

graph_geo.add((Iati['location'],
               RDFS.subClassOf,
               GEO['location']))

# Properties
graph_geo.add((Iati['latitude'],
               RDFS.subPropertyOf,
               GEO['lat']))

graph_geo.add((Iati['longitude'],
               RDFS.subPropertyOf,
               GEO['long']))


#########     CC    #########

print "Add CC mappings..."

# Properties
graph_cc.add((Iati['source-document-license'],
              RDFS.subPropertyOf,
              CC['license']))


#########     Finalize    #########

graph_turtle_skos = graph_skos.serialize(format='turtle')
graph_turtle_dct = graph_dct.serialize(format='turtle')
graph_turtle_foaf = graph_foaf.serialize(format='turtle')
graph_turtle_org = graph_org.serialize(format='turtle')
graph_turtle_geo = graph_geo.serialize(format='turtle')
graph_turtle_cc = graph_cc.serialize(format='turtle')

print "Writing to file..."

with open(turtle_folder + 'schema-skos.ttl', 'w') as turtle_file:
    turtle_file.write(graph_turtle_skos)

with open(turtle_folder + 'schema-dct.ttl', 'w') as turtle_file:
    turtle_file.write(graph_turtle_dct)
    
with open(turtle_folder + 'schema-foaf.ttl', 'w') as turtle_file:
    turtle_file.write(graph_turtle_foaf)
    
with open(turtle_folder + 'schema-org.ttl', 'w') as turtle_file:
    turtle_file.write(graph_turtle_org)
    
with open(turtle_folder + 'schema-geo.ttl', 'w') as turtle_file:
    turtle_file.write(graph_turtle_geo)
    
with open(turtle_folder + 'schema-cc.ttl', 'w') as turtle_file:
    turtle_file.write(graph_turtle_cc) 

print "Adding provenance..."

# Add provenance
provenance = Graph()

provenance = AddProvenance.addProv(Iati,
                                   provenance,
                                   'Schema',
                                   start_time,
                                   "",
                                   ['Schema'],
                                   "mapping%20scripts/ExternalMappings.py")

provenance_turtle = provenance.serialize(format='turtle')

with open(turtle_folder + 'provenance-schema.ttl', 'w') as turtle_file:
    turtle_file.write(provenance_turtle)

print "Done!"