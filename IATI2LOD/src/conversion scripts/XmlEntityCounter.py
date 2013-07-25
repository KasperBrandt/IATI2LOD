import xml.etree.ElementTree as ET
import glob, os, sys, re

# Settings
activities_folder = "/media/Acer/School/IATI-data/xml/activities/"

total_count = 0


for file in glob.glob(activities_folder + '*.xml'):
    file_count = 0
    
    with open(file, 'r') as activities_file:
        
        
        for line in activities_file:
            count = line.count('</transaction>')
            file_count += count
            
        print "Found " + str(file_count) + " in " + str(file)
        
        total_count += file_count
        
print "Total number: " + str(total_count)