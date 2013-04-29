from rdflib import RDF, RDFS, Literal, URIRef, Namespace, OWL
from rdflib.graph import Graph

graph = Graph()
graph.bind('iati', "http://purl.org/collections/iati/")
graph.bind('skos', "http://www.w3.org/2008/05/skos#")

Iati = Namespace("http://purl.org/collections/iati/")
SKOS = Namespace("http://www.w3.org/2008/05/skos#")

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

print graph.serialize(format='turtle')