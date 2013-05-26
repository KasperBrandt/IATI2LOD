## By Kasper Brandt
## Last updated on 26-05-2013

import os, sys, datetime, urllib2, AddProvenance
from rdflib import Namespace, Graph

# Settings
geonames_folder = "/media/Acer/School/IATI-data/dataset/Geonames/"
geonames_files = ["/media/Acer/School/IATI-data/mappings/Geonames/geonames-countries.ttl",
                 "/media/Acer/School/IATI-data/mappings/Geonames/geonames-locations.ttl"]

if not os.path.isdir(geonames_folder):
    os.makedirs(geonames_folder)
    
# Provenance settings
Iati = Namespace("http://purl.org/collections/iati/")    
start_time = datetime.datetime.now()
source_rdfs = []

# Count total number
total_from_file = 0

for geonames_file in geonames_files:
    
    with open(geonames_file, 'r') as f:
        for line in f:
            if "owl:sameAs" in line:
                total_from_file += 1

total_count = 0

for geonames_file in geonames_files:
    
    with open(geonames_file, 'r') as f:
        for line in f:
            
            if "owl:sameAs" in line:
                total_count += 1
                
                line_list = line.split()
                
                geonames_item = line_list[2].replace("<","").replace(">","")
                geonames_item_id = geonames_item.rsplit('/',1)[1]
                    
                geonames_about_url = geonames_item + "/about.rdf"
                geonames_contains_url = geonames_item + "/contains.rdf"
                
                # Check if RDF is already downloaded
                if not geonames_about_url in source_rdfs:
                
                    source_rdfs.append(geonames_about_url)
                    source_rdfs.append(geonames_contains_url)
                    
                    rdf_about_data = urllib2.urlopen(geonames_about_url).read()
                    rdf_contains_data = urllib2.urlopen(geonames_contains_url).read()
                    
                    print "Retrieved data from " + geonames_about_url + ", writing to file (" + str(total_count) + " of " + str(total_from_file) + ")..."
                    
                    with open(geonames_folder + str(geonames_item_id) + "-about.rdf", 'w') as turtle_f:
                        turtle_f.write(rdf_about_data)
                        
                    print "Retrieved data from " + geonames_contains_url + ", writing to file (" + str(total_count) + " of " + str(total_from_file) + ")..."
                    
                    with open(geonames_folder + str(geonames_item_id) + "-contains.rdf", 'w') as turtle_f:
                        turtle_f.write(rdf_contains_data)
                    
# Add provenance
print "Adding provenance..."

provenance = Graph()

provenance = AddProvenance.addProv(Iati,
                                   provenance,
                                   'Geonames',
                                   start_time,
                                   source_rdfs,
                                   ['Geonames'],
                                   "gather%20data%20scripts/GeonamesData.py")

provenance_turtle = provenance.serialize(format='turtle')

with open(geonames_folder + 'provenance-geonames.ttl', 'w') as turtle_file_prov:
    turtle_file_prov.write(provenance_turtle)
    
print "Done!"