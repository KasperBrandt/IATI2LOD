## By Kasper Brandt
## Last updated on 26-05-2013

import os, sys, datetime, urllib2, AddProvenance
from rdflib import Namespace, Graph

# Settings
dbpedia_folder = "/media/Acer/School/IATI-data/dataset/DBPedia/"
dbpedia_files = ["/media/Acer/School/IATI-data/mappings/DBPedia/dbpedia-countries-via-factbook.ttl",
                 "/media/Acer/School/IATI-data/mappings/DBPedia/dbpedia-organisations.ttl"]

if not os.path.isdir(dbpedia_folder):
    os.makedirs(dbpedia_folder)
    
# Provenance settings
Iati = Namespace("http://purl.org/collections/iati/")    
start_time = datetime.datetime.now()
source_ttls = []

for dbpedia_file in dbpedia_files:
    
    with open(dbpedia_file, 'r') as f:
        for line in f:
            
            if "owl:sameAs" in line:
                line_list = line.split()
                
                if "<" in line_list[2]:
                    dbpedia_item = line_list[2].replace("<http://dbpedia.org/resource/","").replace(">","")
                else:
                    dbpedia_item = line_list[2].replace("dbpedia:", "")
                    
                dbpedia_url = "http://dbpedia.org/data/" + dbpedia_item + ".ttl"
                source_ttls.append(dbpedia_url)
                
                turtle_response = urllib2.urlopen(dbpedia_url)
                turtle_data = turtle_response.read()
                
                print "Retrieved data from " + dbpedia_url + ", writing to file..."
                
                with open(dbpedia_folder + dbpedia_item + ".ttl", 'w') as turtle_f:
                    turtle_f.write(turtle_data)

# Add provenance
print "Adding provenance..."

provenance = Graph()

provenance = AddProvenance.addProv(Iati,
                                   provenance,
                                   'DBPedia',
                                   start_time,
                                   source_ttls,
                                   ['DBPedia'],
                                   "gather%20data%20scripts/DbpediaData.py")

provenance_turtle = provenance.serialize(format='turtle')

with open(dbpedia_folder + 'provenance-dbpedia.ttl', 'w') as turtle_file_prov:
    turtle_file_prov.write(provenance_turtle)
    
print "Done!"
                
                