## IatiToTurtle.py
## By Kasper Brandt
## Last updated on 10-04-2013

import glob, sys
import xml.etree.ElementTree as ET
from rdflib import Namespace, Graph, Literal, URIRef
from IatiConverter import ConvertActivity

def main():
    '''Converts XML to Turtle files and stores these to local folder.'''
    
    # Settings
    xml_folder = "/media/Acer/School/IATI2LOD/IATI2LOD/xml/"
    turtle_folder = "/media/Acer/School/IATI2LOD/IATI2LOD/Data/"
    Iati = Namespace("http://purl.org/collections/iati/")
    
    provenance = Graph()
    provenance.bind('iati', Iati)
    
    document_count = 1
    activity_count = 1
    
    total_elapsed_time = 0
    
    # Retrieve XML files from the XML folder
    for document in glob.glob(xml_folder + '*.xml'):
        
        xml = ET.parse(document)
        
        # Convert each activity in XML file to RDFLib Graph
        for activity in xml.findall('iati-activity'):
            
            converter = ConvertActivity(activity)
            graph, id, last_updated = converter.convert(Iati)
            
            # Write activity to Turtle and store in local folder
            graph_turtle = graph.serialize(format='turtle')
            
            with open(turtle_folder + 'activity-' + id + '.ttl', 'w') as turtle_file:
                turtle_file.write(graph_turtle)
            
            # Add provenance
            provenance.add((URIRef(Iati + 'graph/' + id + '.ttl'),
                            URIRef(Iati + 'last-updated'),
                            Literal(last_updated)))
            
            print "Progress: Activity #" + str(activity_count) + " in document #" + str(document_count)
            
            activity_count += 1
                   
        document_count += 1
    
    # Write provenance graph to Turtle and store in local folder
    provenance_turtle = provenance.serialize(format='turtle')
    
    with open(turtle_folder + id + '.ttl', 'w') as turtle_file:
        turtle_file.write(provenance_turtle)
        
    print "Done!"
    
if __name__ == "__main__":
    main()