## By Kasper Brandt
## Last updated on 15-04-2013

import glob, sys, os, IatiConverter
import xml.etree.ElementTree as ET
from rdflib import Namespace, Graph, Literal, URIRef

def main():
    '''Converts Codelist XMLs to Turtle files and stores these to local folder.'''
    
    # Settings
    xml_folder = "/media/Acer/School/IATI2LOD/IATI2LOD/xml/codelists/"
    turtle_folder = "/media/Acer/School/IATI-data/codelists/"
    Iati = Namespace("http://purl.org/collections/iati/")
    
    provenance = Graph()
    provenance.bind('iati', Iati)

    if not os.path.isdir(turtle_folder):
        os.makedirs(turtle_folder)
    
    document_count = 1
    
    total_elapsed_time = 0
    
    # Retrieve XML files from the XML folder
    for document in glob.glob(xml_folder + '*.xml'):
        
        xml = ET.parse(document)
        root = xml.getroot()
        
        try:
            # Convert each codelist in XML file to RDFLib Graph    
            converter = IatiConverter.ConvertCodelist(root)
            graph, id, last_updated = converter.convert(Iati)
        except TypeError as e:
            print "Error in " + document + ":" + str(e)
        
        if not graph == None:
            # Write codelist to Turtle and store in local folder
            graph_turtle = graph.serialize(format='turtle')
            
            with open(turtle_folder + 'codelist-' + id.replace('/','-') + '.ttl', 'w') as turtle_file:
                turtle_file.write(graph_turtle)
            
            # Add provenance
            provenance.add((URIRef(Iati + 'codelist-' + id.replace('/','-')),
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