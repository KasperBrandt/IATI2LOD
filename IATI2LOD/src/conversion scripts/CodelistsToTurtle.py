## CodelistsToTurtle.py
## By Kasper Brandt
## Last updated on 13-04-2013

import glob, sys, IatiConverter
import xml.etree.ElementTree as ET
from rdflib import Namespace, Graph, Literal, URIRef

def main():
    '''Converts Codelist XMLs to Turtle files and stores these to local folder.'''
    
    # Settings
    xml_folder = "/media/Acer/School/IATI2LOD/IATI2LOD/xml/codelists/"
    turtle_folder = "/media/Acer/School/IATI2LOD/IATI2LOD/Data/"
    Iati = Namespace("http://purl.org/collections/iati/")
    
    provenance = Graph()
    provenance.bind('iati', Iati)
    provenance.bind('graph', Iati['graph/'])
    
    document_count = 1
    
    total_elapsed_time = 0
    
    # Retrieve XML files from the XML folder
    for document in glob.glob(xml_folder + '*.xml'):
        
        xml = ET.parse(document)
        root = xml.getroot()
        
        # Convert each codelist in XML file to RDFLib Graph    
        converter = IatiConverter.ConvertCodelist(root)
        graph, id, last_updated = converter.convert(Iati)
        
        # Write codelist to Turtle and store in local folder
        graph_turtle = graph.serialize(format='turtle')
        
        with open(turtle_folder + 'codelist-' + id + '.ttl', 'w') as turtle_file:
            turtle_file.write(graph_turtle)
        
        # Add provenance
        provenance.add((URIRef(Iati + 'graph/' + id),
                        URIRef(Iati + 'last-updated'),
                        Literal(last_updated)))
        
        print "Progress: Document #" + str(document_count)
                   
        document_count += 1
    
    # Write provenance graph to Turtle and store in local folder
    provenance_turtle = provenance.serialize(format='turtle')
    
    with open(turtle_folder + 'codelist-provenance.ttl', 'w') as turtle_file:
        turtle_file.write(provenance_turtle)
        
    print "Done!"

if __name__ == "__main__":
    main()