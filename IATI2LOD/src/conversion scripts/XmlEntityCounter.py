import xml.etree.ElementTree as ET
import glob, os, sys, re

# Settings
turtle_folder = "/media/Acer/School/IATI-data/mappings/"
activities_folder = "/media/Acer/School/IATI-data/xml/activities/"

locations = {}
total_count = 0


for file in glob.glob(activities_folder + '*.xml'):
    file_count = 0
    
    with open(file, 'r') as activities_file:
        
        
        for line in activities_file:

            if "<indicator" in line:
                file_count += 1
            
        print "Found " + str(file_count) + " in " + str(file)
        
        total_count += file_count
        
print "Total number: " + str(total_count)