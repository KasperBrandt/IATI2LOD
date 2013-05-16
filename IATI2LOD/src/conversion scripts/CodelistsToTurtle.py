## By Kasper Brandt
## Last updated on 16-05-2013

import glob, sys, os, IatiConverter, AttributeHelper
import xml.etree.ElementTree as ET
from rdflib import Namespace, Graph, Literal, URIRef, RDF

def main():
    '''Converts Codelist XMLs to Turtle files and stores these to local folder.'''
    
    # Settings
    xml_folder = "/media/Acer/School/IATI-data/xml/codelists/"
    turtle_folder = "/media/Acer/School/IATI-data/codelist/"
    provenance_folder = "/media/Acer/School/IATI-data/provenance/"
    Iati = Namespace("http://purl.org/collections/iati/")
        
    if not os.path.isdir(provenance_folder):
        os.makedirs(provenance_folder)
    
    document_count = 1
    
    total_elapsed_time = 0
    
    # Retrieve XML files from the XML folder
    for document in glob.glob(xml_folder + '*.xml'):
        
        doc_id = str(document.rsplit('/',1)[1])[:-4]
        doc_folder = turtle_folder + doc_id + '/'
        
        if not os.path.isdir(doc_folder):
            os.makedirs(doc_folder)
        
        provenance = Graph()
        provenance.bind('iati', Iati)
        
        xml = ET.parse(document)
        root = xml.getroot()
        
        version = AttributeHelper.attribute_key(root, 'version')
        
        try:
            # Convert each codelist in XML file to RDFLib Graph    
            converter = IatiConverter.ConvertCodelist(root)
            graph, id, last_updated = converter.convert(Iati)
        except TypeError as e:
            print "Error in " + document + ":" + str(e)
            graph = None
        
        if not graph == None:
            # Write codelist to Turtle and store in local folder
            graph_turtle = graph.serialize(format='turtle')
            
            with open(doc_folder + id.replace('/','%2F') + '.ttl', 'w') as turtle_file:
                turtle_file.write(graph_turtle)
            
            # Add provenance of last-updated, version and source document
            provenance.add((URIRef(Iati + 'graph/codelist/' + str(id)),
                            URIRef(Iati + 'last-updated'),
                            Literal(last_updated)))
            
            provenance.add((URIRef(Iati + 'graph/codelist/' + str(id)),
                            URIRef(Iati + 'version'),
                            Literal(version)))
            
            provenance.add((URIRef(Iati + 'graph/codelist/' + str(id)),
                            URIRef(Iati + 'source-document-id'),
                            Literal(str(id))))
            
            provenance.add((URIRef(Iati + 'graph/codelist/' + str(id)),
                            URIRef(Iati + 'source-document-download-url'),
                            URIRef('http://datadev.aidinfolabs.org/data/codelist/' + str(id) + '.xml')))                        
        
        print "Progress: Document #" + str(document_count)
                   
        document_count += 1
    
        # Write provenance graph to Turtle and store in local folder
        provenance_turtle = provenance.serialize(format='turtle')
        
        with open(provenance_folder + 'provenance-codelist-' + str(id) + '.ttl', 'w') as turtle_file:
            turtle_file.write(provenance_turtle)
        
    print "Done!"

if __name__ == "__main__":
    main()