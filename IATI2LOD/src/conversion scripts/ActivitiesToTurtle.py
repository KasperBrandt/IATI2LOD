## ActivitiesToTurtle.py
## By Kasper Brandt
## Last updated on 15-04-2013

import glob, sys, os, IatiConverter
import xml.etree.ElementTree as ET
from rdflib import Namespace, Graph, Literal, URIRef

def main():
    '''Converts Activity XMLs to Turtle files and stores these to local folder.'''
    
    # Settings
    xml_folder = "/media/Acer/School/IATI2LOD/IATI2LOD/xml/activities/"
    turtle_folder = "/media/Acer/School/IATI2LOD/IATI2LOD/Data/activities/"
    Iati = Namespace("http://purl.org/collections/iati/")
    
    if not os.path.isdir(turtle_folder):
        os.makedirs(turtle_folder)
    
    provenance = Graph()
    provenance.bind('iati', Iati)
    
    document_count = 1
    activity_count = 1
    
    total_elapsed_time = 0
    
    # Retrieve XML files from the XML folder
    for document in glob.glob(xml_folder + '*.xml'):
        
        try:
            xml = ET.parse(document)
        except ET.ParseError:
            print "Could not parse file " + document
        
        # Convert each activity in XML file to RDFLib Graph
        for activity in xml.findall('iati-activity'):
            
            try:
                converter = IatiConverter.ConvertActivity(activity)
                graph, id, last_updated = converter.convert(Iati)
            except TypeError as e:
                print "Error in " + document + ":" + str(e)            
            
            if not graph == None:
                # Write activity to Turtle and store in local folder
                graph_turtle = graph.serialize(format='turtle')
                
                with open(turtle_folder + 'activity-' + id.replace('/','-') + '.ttl', 'w') as turtle_file:
                    turtle_file.write(graph_turtle)
            
                # Add provenance
                provenance.add((URIRef(Iati + 'activity-' + id),
                                URIRef(Iati + 'last-updated'),
                                Literal(last_updated)))
            
            print "Progress: Activity #" + str(activity_count) + " in document #" + str(document_count)
            
            activity_count += 1
                   
        document_count += 1
    
    # Write provenance graph to Turtle and store in local folder
    provenance_turtle = provenance.serialize(format='turtle')
    
    with open(turtle_folder + 'activity-provenance.ttl', 'w') as turtle_file:
        turtle_file.write(provenance_turtle)
        
    print "Done!"
    
if __name__ == "__main__":
    main()