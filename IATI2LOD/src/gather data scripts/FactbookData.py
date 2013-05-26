## By Kasper Brandt
## Last updated on 26-05-2013

import os, sys, datetime, urllib2, AddProvenance
from rdflib import Namespace, Graph

# Settings
factbook_folder = "/media/Acer/School/IATI-data/dataset/Factbook/"
factbook_file = "/media/Acer/School/IATI-data/mappings/Factbook/factbook-countries.ttl"

if not os.path.isdir(factbook_folder):
    os.makedirs(factbook_folder)
    
# Provenance settings
Iati = Namespace("http://purl.org/collections/iati/")    
start_time = datetime.datetime.now()
sources = []
    
with open(factbook_file, 'r') as f:
    for line in f:
        
        if "owl:sameAs" in line:
            line_list = line.split()
            
            if "<" in line_list[2]:
                factbook_item = line_list[2].replace("<http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/","").replace(">","")
            else:
                factbook_item = line_list[2].replace("cia:", "")
                
            factbook_url = "http://wifo5-04.informatik.uni-mannheim.de/factbook/data/" + factbook_item
            sources.append(factbook_url)
            
            turtle_data = urllib2.urlopen(factbook_url).read()
            
            print "Retrieved data from " + factbook_url + ", writing to file..."
            
            with open(factbook_folder + factbook_item + ".ttl", 'w') as turtle_f:
                turtle_f.write(turtle_data)

# Add provenance
print "Adding provenance..."

provenance = Graph()

provenance = AddProvenance.addProv(Iati,
                                   provenance,
                                   'Factbook',
                                   start_time,
                                   sources,
                                   ['Factbook'],
                                   "gather%20data%20scripts/FactbookData.py")

provenance_turtle = provenance.serialize(format='turtle')

with open(factbook_folder + 'provenance-factbook.ttl', 'w') as turtle_file_prov:
    turtle_file_prov.write(provenance_turtle)
    
print "Done!"
                
                