## By Kasper Brandt
## Last updated on 22-05-2013

from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import RDF, RDFS, Literal, URIRef, Namespace, OWL
from rdflib.graph import Graph
import xml.etree.ElementTree as ET
import glob, os, sys, re

# Settings
turtle_folder = "/media/Acer/School/IATI-data/mappings/"
activities_folder = "/media/Acer/School/IATI-data/activity/"

locations = {}
location_count = 0

# Retrieve TTL files from the activities folder
for folder in glob.glob(activities_folder + '*'):
    print "Checking out folder " + str(folder) + "..."
    
    for activity_file in glob.glob(folder + '/*.ttl'):
        
        with open(activity_file, 'r') as turtle_file:
            turtle_file_data = turtle_file.read()
            
            # Check whether the file has a location
            if "iati:location" in turtle_file_data:
                print "Found location in " + str(activity_file) + "..."
                location_count += 1
                
                location_information = {}
                done_location = False
                done_country = False
                
                # Look up the location information
                turtle_file.seek(0)
                while not done_location:
                    line = turtle_file.readline()

                    if "iati:location " in line:
                        location_id = line.split()[0].replace("<","").replace(">","")
                        
                        while not done_location:
                            line = turtle_file.readline()
                            
                            if ":" in line:
                                if "rdfs:label" in line:
                                    match = re.search(r'\"(.+?)\"', line)
                                    location_information['label'] = match.group(0).replace('"', '')
                                    
                                elif "iati:coordinates-precision" in line:
                                    location_information['precision'] = line.rsplit('/',1)[1][:1]
                                    
                                elif "iati:latitude" in line:
                                    match_lat = re.search(r'\"(.+?)\"', line)
                                    location_information['latitude'] = match_lat.group(0).replace('"', '')
                                    
                                elif "iati:longitude" in line:
                                    match_long = re.search(r'\"(.+?)\"', line)
                                    location_information['longitude'] = match_long.group(0).replace('"', '')
                                    
                            else:
                                done_location = True
                                
                # Look up recipient country information
                turtle_file.seek(0)
                if ("/recipient-country/" in turtle_file_data):
                    while not done_country:
                         line = turtle_file.readline()
                         
                         if ("/recipient-country/" in line) and ("> a iati:country ;" in line):
                             while not done_country:
                                line = turtle_file.readline()
                                 
                                if ":" in line:
                                    if "rdfs:label" in line:
                                        match_country = re.search(r'\"(.+?)\"', line)
                                        location_information['country_label'] = match_country.group(0).replace('"', '')
                                        
                                else:
                                    done_country = True
                                    
            locations[location_id] = location_information
            
print "Writing to file..."

with open(turtle_folder + 'locations.help', 'w') as locations_file:
    for key in locations.keys():
        locations_file.write("id: " + str(key) + "\n")
        for location_key in locations[key].keys():
            locations_file.write(str(location_key) + ": " + str(locations[key][location_key]) + "\n")
        locations_file.write("\n")
        
print "Done, total number of locations: " + str(location_count)