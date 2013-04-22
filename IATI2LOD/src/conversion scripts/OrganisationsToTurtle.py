## By Kasper Brandt
## Last updated on 15-04-2013

import glob, sys, os, IatiConverter
import xml.etree.ElementTree as ET
from rdflib import Namespace, Graph, Literal, URIRef

def main():
    '''Converts Activity XMLs to Turtle files and stores these to local folder.'''
    
    # Settings
    xml_folder = "/media/Acer/School/IATI2LOD/IATI2LOD/xml/organisations/"
    turtle_folder = "/media/Acer/School/IATI-data/organisations/"
    Iati = Namespace("http://purl.org/collections/iati/")
    
    provenance = Graph()
    provenance.bind('iati', Iati)

    if not os.path.isdir(turtle_folder):
        os.makedirs(turtle_folder)
    
    document_count = 1
    organisation_count = 1
    
    total_elapsed_time = 0
    
    # Retrieve XML files from the XML folder
    for document in glob.glob(xml_folder + '*.xml'):
        
        try:
            xml = ET.parse(document)
        except ET.ParseError:
            print "Could not parse file " + document
        
        if (xml.getroot().tag == 'iati-organisations') or (xml.getroot().tag == 'organisations'):
                        
            # Convert each organisation in XML file to RDFLib Graph
            for organisation in xml.findall('iati-organisation'):
                
                try:
                    converter = IatiConverter.ConvertOrganisation(organisation)
                    graph, id, last_updated = converter.convert(Iati)
                except TypeError as e:
                    print "Error in " + document + ":" + str(e)
                    graph = None
                
                if not graph == None:
                    # Write activity to Turtle and store in local folder
                    graph_turtle = graph.serialize(format='turtle')
                    
                    with open(turtle_folder + 'organisation-' + id.replace('/','-') + '.ttl', 'w') as turtle_file:
                        turtle_file.write(graph_turtle)
                    
                    # Add provenance
                    provenance.add((URIRef(Iati + 'organisation-' + id.replace('/','-')),
                                    URIRef(Iati + 'last-updated'),
                                    Literal(last_updated)))
                
                print "Progress: Organisation #" + str(organisation_count) + " in document #" + str(document_count)
                
                organisation_count += 1

            for organisation in xml.findall('organisation'):
                
                try:
                    converter = IatiConverter.ConvertOrganisation(organisation)
                    graph, id, last_updated = converter.convert(Iati)
                except TypeError as e:
                    print "Error in " + document + ":" + str(e)
                
                # Write activity to Turtle and store in local folder
                graph_turtle = graph.serialize(format='turtle')
                
                with open(turtle_folder + 'organisation-' + id + '.ttl', 'w') as turtle_file:
                    turtle_file.write(graph_turtle)
                
                # Add provenance
                provenance.add((URIRef(Iati + 'graph/' + id),
                                URIRef(Iati + 'last-updated'),
                                Literal(last_updated)))
                
                print "Progress: Organisation #" + str(organisation_count) + " in document #" + str(document_count)
                
                organisation_count += 1
            
        elif (xml.getroot().tag == 'iati-organisation') or (xml.getroot().tag == 'organisation'):
            
                try:
                    converter = IatiConverter.ConvertOrganisation(xml.getroot())
                    graph, id, last_updated = converter.convert(Iati)
                except TypeError as e:
                    print "Error in " + document + ":" + str(e)
                
                # Write activity to Turtle and store in local folder
                graph_turtle = graph.serialize(format='turtle')
                
                with open(turtle_folder + 'organisation-' + id + '.ttl', 'w') as turtle_file:
                    turtle_file.write(graph_turtle)
                
                # Add provenance
                provenance.add((URIRef(Iati + 'graph/' + id),
                                URIRef(Iati + 'last-updated'),
                                Literal(last_updated)))
                
                print "Progress: Organisation #" + str(organisation_count) + " in document #" + str(document_count)
                
                organisation_count += 1
                   
        document_count += 1
    
    # Write provenance graph to Turtle and store in local folder
    provenance_turtle = provenance.serialize(format='turtle')
    
    with open(turtle_folder + 'organisation-provenance.ttl', 'w') as turtle_file:
        turtle_file.write(provenance_turtle)
        
    print "Done!"
    
if __name__ == "__main__":
    main()