## By Kasper Brandt
## Last updated on 25-05-2013

from rdflib import RDF, RDFS, Literal, URIRef, Namespace, OWL
from rdflib.graph import Graph
import xml.etree.ElementTree as ET
import os, sys, httplib2, json, urllib, urllib2, AddProvenance, datetime

def connect(url):
    '''Connects to the given URL and returns response.
    
    Parameters
    @url: The URL.
    
    Returns
    @content: Content of the response or None in case of a fail.'''
    
    try:
        response, content = httplib2.Http().request(url, "GET")
    
    except httplib2.ServerNotFoundError as e:
        print e
        return None
    
    return content

def retrieve_locations(locations_file):
    '''Retrieves all locations from a local file.
    
    Parameters
    @file: Local file with location information.
    
    Returns
    @locations: List of dictionaries containing location information.'''
    
    all_locations = []
    file_done = False
    location_count = 0
    
    with open(locations_file, 'r') as file:
        while not file_done:
            line = file.readline()
            
            # Look for a location 
            if str(line[:4]) == "id: ":
                location = {}
                location_done = False
                
                location['link'] = str(line[4:]).replace("\n","")
                
                while not location_done:
                    next_line = file.readline()
                    
                    if not next_line == "\n":
                        if str(next_line[:10]) == "latitude: ":
                            location['latitude'] = str(next_line[10:]).replace("\n","")
                        elif str(next_line[:11]) == "longitude: ":
                            location['longitude'] = str(next_line[11:]).replace("\n","")
                        elif str(next_line[:11]) == "precision: ":
                            location['precision'] = str(next_line[11:]).replace("\n","")
                        elif str(next_line[:15]) == "country_label: ":
                            location['country_label'] = str(next_line[15:]).replace("\n","")
                        elif str(next_line[:7]) == "label: ":
                            location['label'] = str(next_line[7:]).replace("\n","")
                    else:
                        location_done = True
                        all_locations.append(location)
            
            else:
                file_done = True
                        
    return all_locations

def classify_locations(locations):
    '''Retrieves all locations from a local file.
    
    Parameters
    @locations: List of dictionaries containing location information.
    
    Returns
    @locations: List of dictionaries containing location information, added the classification.'''
    
    for location in locations:
        keys = location.keys()
        
        if ("latitude" in keys) and ("longitude" in keys) and ("precision" in keys):
            location['classification'] = 1
            
        elif ("latitude" in keys) and ("longitude" in keys):
            location['classification'] = 2
            
        elif ("country_label" in keys) and ("label" in keys):
            location['classification'] = 3
            
        elif ("label" in keys):
            location['classification'] = 4
            
        elif ("country_label" in keys):
            location['classification'] = 5 
        
        else:
            location['classification'] = 0
            
    return locations

def algorithm_one(location, geonames_uri, username, country_info):
    '''The algorithm for finding locations based on a precision smaller than 6, latitude 
    and longitude of a location.
    
    Parameters
    @location: A dictionary of location information.
    @geonames_uri: Base URI of Geonames.
    @username: Geonames username.
    @country_info: XML Etree containing information about countries.
    
    Returns
    @match: The matching Geonames URI.'''
    
    if location['precision'] < '3':
        service = "findNearbyPlaceName?"
        featureCode = ""
        print "Finding nearby place name..."
    elif location['precision'] == '3':
        service = "findNearby?"
        featureCode = "ADM2"
        print "Finding nearby place ADM2..."
    elif (location['precision'] == '4') or (location['precision'] == '5'):
        service = "findNearby?"
        featureCode = "ADM1"
        print "Finding nearby place ADM1..."
    elif location['precision'] > '5':
        service = "countryCode?"
        featureCode = ""
        print "Finding nearby country or capital..."
    else:
        print "Something went wrong with the precision..."
    
    webservice = geonames_uri + service
        
    params = dict([('username', username),
                   ('lat', str(location['latitude'])),
                   ('lng', str(location['longitude']))])
    
    if not featureCode == "":
        params['fcode'] = featureCode
    
    params_encoded = urllib.urlencode(params).replace('+', '%20').replace('%0A%0A','%20')
            
    url = webservice + params_encoded
    content = connect(url)
    
    if location['precision'] < '6':
        if not content == None:
            geonames_xml = ET.fromstring(content)
            geoname = geonames_xml.find('geoname')
            
            if not geoname == None:
                match = "http://sws.geonames.org/" + str(geoname.find('geonameId').text)
                return match
                
            else:
                status = geonames_xml.find('status')
                if not status == None:
                    print status.attrib['message']
                    if "timeout" in status.attrib['message']:
                        print "Trying again..."
                        return algorithm_one(location, geonames_uri, username, country_info)
                    return None
                else:
                    print "Trying again, broad search..."
                    
                    webservice = geonames_uri + "findNearby?"
                        
                    params = dict([('username', username),
                                   ('lat', str(location['latitude'])),
                                   ('lng', str(location['longitude']))])
                    
                    params_encoded = urllib.urlencode(params).replace('+', '%20').replace('%0A%0A','%20')       
                    url = webservice + params_encoded
                    
                    content = connect(url)
                    
                    if not content == None:
                        
                        geonames_xml = ET.fromstring(content)
                        geoname = geonames_xml.find('geoname')
                        
                        if not geoname == None:
                            match = "http://sws.geonames.org/" + str(geoname.find('geonameId').text)
                            return match
                            
                        else:
                            status = geonames_xml.find('status')
                            if not status == None:
                                print status.attrib['message']
                                if "timeout" in status.attrib['message']:
                                    print "Trying again..."
                                    return algorithm_one(location, geonames_uri, username, country_info)
                                return None
                            else:
                                return 0
                    
                    else:
                        return None
                    
        else:
            return None
        
    elif location['precision'] > '5':
        if len(content) > 5:
                print "Country code not found..."
                
                webservice = geonames_uri + "findNearby?"
                    
                params = dict([('username', username),
                               ('lat', str(location['latitude'])),
                               ('lng', str(location['longitude']))])
                
                params_encoded = urllib.urlencode(params).replace('+', '%20').replace('%0A%0A','%20')       
                url = webservice + params_encoded
                
                content = connect(url)
                
                if not content == None:
                    
                    geonames_xml = ET.fromstring(content)
                    geoname = geonames_xml.find('geoname')
                    
                    if not geoname == None:
                        match = "http://sws.geonames.org/" + str(geoname.find('geonameId').text)
                        return match
                        
                    else:
                        status = geonames_xml.find('status')
                        if not status == None:
                            print status.attrib['message']
                            if "timeout" in status.attrib['message']:
                                print "Trying again..."
                                return algorithm_one(location, geonames_uri, username, country_info)
                            return None
                        else:
                            return 0
                
                else:
                    return None
        
        country_code = content.rstrip()
            
        if (location['precision'] == '6') or (location['precision'] == '9'):
            print "Trying to find " + country_code + "..."
            for country in country_info:
                if country.find('countryCode').text == country_code:
                    match = "http://sws.geonames.org/" + str(country.find('geonameId').text)
                    return match
            
            return 0
                    
        elif (location['precision'] == '7') or (location['precision'] == '8'):
            for country in country_info:
                if country.find('countryCode').text == country_code:
                    capital = country.find('capital').text
                    break
            
            print "Looking for capital " + str(capital) + "..."
            
            webservice = geonames_uri + "search?"
            
            params = dict([('username', username),
                           ('countryCode', str(country_code)),
                           ('name_equals', str(capital))])
    
            params_encoded = urllib.urlencode(params).replace('+', '%20').replace('%0A%0A','%20')
                    
            url = webservice + params_encoded
            content = connect(url)
            
            if not content == None:
        
                geonames_xml = ET.fromstring(content)
                geoname = geonames_xml.find('geoname')
                
                if not geoname == None:
                    match = "http://sws.geonames.org/" + str(geoname.find('geonameId').text)
                    return match
                    
                else:
                    status = geonames_xml.find('status')
                    if not status == None:
                        print status.attrib['message']
                        if "timeout" in status.attrib['message']:
                            print "Trying again..."
                            return algorithm_one(location, geonames_uri, username, country_info)
                        return None            
                    else:
                        return 0
                    
            else:
                return None

def algorithm_two(location, geonames_uri, username):
    '''The algorithm for finding locations with a latitude and longitude of a location.
    
    Parameters
    @location: A dictionary of location information.
    @geonames_uri: Base URI of Geonames.
    @username: Geonames username.
    
    Returns
    @match: The matching Geonames URI.'''
    
    service = "findNearbyPlaceName?"
    print "Finding nearby place name..."
    
    webservice = geonames_uri + service
        
    params = dict([('username', username),
                   ('lat', str(location['latitude'])),
                   ('lng', str(location['longitude']))])
    
    params_encoded = urllib.urlencode(params).replace('+', '%20').replace('%0A%0A','%20')
            
    url = webservice + params_encoded
    content = connect(url)
    
    if not content == None:
        geonames_xml = ET.fromstring(content)
        geoname = geonames_xml.find('geoname')
        
        if not geoname == None:
            match = "http://sws.geonames.org/" + str(geoname.find('geonameId').text)
            return match
            
        else:
            status = geonames_xml.find('status')
            if not status == None:
                print status.attrib['message']
                if "timeout" in status.attrib['message']:
                    print "Trying again..."
                    return algorithm_two(location, geonames_uri, username)
                return None
            else:
                print "Trying again, broad search..."
                
                webservice = geonames_uri + "findNearby?"
                    
                params = dict([('username', username),
                               ('lat', str(latitude)),
                               ('lng', str(longitude))])
                
                params_encoded = urllib.urlencode(params).replace('+', '%20').replace('%0A%0A','%20')       
                url = webservice + params_encoded
                
                content = connect(url)
                
                if not content == None:
                    
                    geonames_xml = ET.fromstring(content)
                    geoname = geonames_xml.find('geoname')
                    
                    if not geoname == None:
                        match = "http://sws.geonames.org/" + str(geoname.find('geonameId').text)
                        return match
                        
                    else:
                        status = geonames_xml.find('status')
                        if not status == None:
                            print status.attrib['message']
                            if "timeout" in status.attrib['message']:
                                print "Trying again..."
                                return algorithm_two(location, geonames_uri, username)
                            return None
                        else:
                            return 0
                
                else:
                    return None
                
    else:
        return None
    
def algorithm_three(location, geonames_uri, username):
    '''The algorithm for finding locations with a label and a country label.
    
    Parameters
    @location: A dictionary of location information.
    @geonames_uri: Base URI of Geonames.
    @username: Geonames username.
    
    Returns
    @match: The matching Geonames URI.'''
    
    service = "search?"
    print "Searching for label..."
    
    webservice = geonames_uri + service
        
    params = dict([('username', username),
                   ('q', str(location['label']))])
    
    params_encoded = urllib.urlencode(params).replace('+', '%20').replace('%0A%0A','%20')
            
    url = webservice + params_encoded
    content = connect(url)
    
    if not content == None:
        
        geonames_xml = ET.fromstring(content)
        results = geonames_xml.find('totalResultsCount')

        if (not results.text == '0') and (not results.text == None):
            geoname = geonames_xml.find('geoname')
            
            match = "http://sws.geonames.org/" + str(geoname.find('geonameId').text)
            return match
             
        else:
            status = geonames_xml.find('status')
            if not status == None:
                print status.attrib['message']
                if "timeout" in status.attrib['message']:
                    print "Trying again..."
                    return algorithm_three(location, geonames_uri, username)
                return None
            else:
                
                service = "search?"
                print "Searching for country label..."
                
                webservice = geonames_uri + service
                    
                params = dict([('username', username),
                               ('q', str(location['country_label']))])
                
                params_encoded = urllib.urlencode(params).replace('+', '%20').replace('%0A%0A','%20')
                        
                url = webservice + params_encoded
                content = connect(url)
                
                if not content == None:
                    
                    geonames_xml = ET.fromstring(content)
                    results = geonames_xml.find('totalResultsCount')
                    
                    if (not results.text == '0') and (not results.text == None):
                        geoname = geonames_xml.find('geoname')
                        
                        match = "http://sws.geonames.org/" + str(geoname.find('geonameId').text)
                        return match
                         
                    else:
                        status = geonames_xml.find('status')
                        if not status == None:
                            print status.attrib['message']
                            if "timeout" in status.attrib['message']:
                                print "Trying again..."
                                return algorithm_three(location, geonames_uri, username)
                            return None
                        else:
                            return 0

def algorithm_four(location, geonames_uri, username):
    '''The algorithm for finding locations with a label.
    
    Parameters
    @location: A dictionary of location information.
    @geonames_uri: Base URI of Geonames.
    @username: Geonames username.
    
    Returns
    @match: The matching Geonames URI.'''
    
    service = "search?"
    print "Searching for label..."
    
    webservice = geonames_uri + service
        
    params = dict([('username', username),
                   ('q', str(location['label']))])
    
    params_encoded = urllib.urlencode(params).replace('+', '%20').replace('%0A%0A','%20')
            
    url = webservice + params_encoded
    content = connect(url)
    
    if not content == None:
        
        geonames_xml = ET.fromstring(content)
        results = geonames_xml.find('totalResultsCount')
        
        if (not results.text == '0') and (not results.text == None):
            geoname = geonames_xml.find('geoname')
            
            match = "http://sws.geonames.org/" + str(geoname.find('geonameId').text)
            return match
             
        else:
            status = geonames_xml.find('status')
            if not status == None:
                print status.attrib['message']
                if "timeout" in status.attrib['message']:
                    print "Trying again..."
                    return algorithm_three(location, geonames_uri, username)
                return None
            else:
                return 0

def algorithm_five(location, geonames_uri, username):
    '''The algorithm for finding locations with a country label.
    
    Parameters
    @location: A dictionary of location information.
    @geonames_uri: Base URI of Geonames.
    @username: Geonames username.
    
    Returns
    @match: The matching Geonames URI.'''
                
    service = "search?"
    print "Searching for country label..."
    
    webservice = geonames_uri + service
        
    params = dict([('username', username),
                   ('q', str(location['country_label']))])
    
    params_encoded = urllib.urlencode(params).replace('+', '%20').replace('%0A%0A','%20')
            
    url = webservice + params_encoded
    content = connect(url)
    
    if not content == None:
        
        geonames_xml = ET.fromstring(content)
        results = geonames_xml.find('totalResultsCount')
        
        if (not results.text == '0') and (not results.text == None):
            geoname = geonames_xml.find('geoname')
            
            match = "http://sws.geonames.org/" + str(geoname.find('geonameId').text)
            return match
             
        else:
            status = geonames_xml.find('status')
            if not status == None:
                print status.attrib['message']
                if "timeout" in status.attrib['message']:
                    print "Trying again..."
                    return algorithm_three(location, geonames_uri, username)
                return None
            else:
                return 0

def find_location(location, country_info):
    '''Retrieves location match from Geonames based on the information available.
    
    Parameters
    @location: A dictionary of location information.
     
    Returns
    @match: A Geonames URL.'''
    
    geonames_uri = "http://api.geonames.org/"
    username = "KasperBrandt"
    
    if location['classification'] == 1:
        match = algorithm_one(location, geonames_uri, username, country_info)
        return match
    elif location['classification'] == 2:
        match = algorithm_two(location, geonames_uri, username)
        return match
    elif location['classification'] == 3:
        match = algorithm_three(location, geonames_uri, username)
        return match
    elif location['classification'] == 4:
        match = algorithm_four(location, geonames_uri, username)
        return match
    elif location['classification'] == 5:
        match = algorithm_five(location, geonames_uri, username)
        return match
    

def main():
    '''Retrieves all locations from a local file and matches the labels, country labels and
    coordinates (if available) of a location to Geonames.'''
    
    # Settings
    turtle_folder = "/media/Acer/School/IATI-data/mappings/Geonames/"
    locations_file = "/media/Acer/School/IATI-data/mappings/locations.help"
    Iati = Namespace("http://purl.org/collections/iati/")
    start_time = datetime.datetime.now()
    
    found = 0
    not_found = 0
    
    # Read location file
    print "Retrieving locations from file..."
    all_locations = retrieve_locations(locations_file)
    
    # Classify locations
    print "Classifying locations..."
    all_locations = classify_locations(all_locations)
    
    # Initialize graph
    locations_graph = Graph()
    locations_graph.bind('iati', "http://purl.org/collections/iati/")
    locations_graph.bind('gn', "http://sws.geonames.org/")
    locations_graph.bind('owl', "http://www.w3.org/2002/07/owl#")
    
    # Retrieve all general country information
    country_info = connect("http://api.geonames.org/countryInfo?username=kasperbrandt")
    country_info = ET.fromstring(country_info)
    
    if country_info == None:
        print "Could not retrieve country information, exiting..."
        sys.exit(0)
    
    # Retrieve location match from Geonames
    for location in all_locations:
        
        if not location['classification'] == 0:
            print "Looking for " + location['link'] + "..."
            match = find_location(location, country_info)
            
            if (not match == None) and (not match == 0):
                locations_graph.add((URIRef(location['link']),
                                     OWL.sameAs,
                                     URIRef(match)))
                
                found += 1
                
            elif match == 0:
                # Did not find any results
                not_found += 1
            
            elif match == None:
                # No more credits
                print "Credits are gone.."
                locations_turtle = locations_graph.serialize(format='turtle')
    
                with open(turtle_folder + 'geonames-locations.ttl', 'w') as turtle_file:
                    turtle_file.write(locations_turtle)
                    
                sys.exit(0)
        
    # Write to file
    print "Done, writing " + str(found) + " mappings to file..."    
    locations_turtle = locations_graph.serialize(format='turtle')

    with open(turtle_folder + 'geonames-locations.ttl', 'w') as turtle_file:
        turtle_file.write(locations_turtle)
    
    print "Did not find " + str(not_found) + " mappings..."
    
    # Add provenance
    provenance = Graph()
    
    provenance = AddProvenance.addProv(Iati,
                                       provenance,
                                       'Geonames',
                                       start_time,
                                       "http://sws.geonames.org/",
                                       ['Geonames'],
                                       "mapping%20scripts/GeonamesLocations.py")
    
    provenance_turtle = provenance.serialize(format='turtle')

    with open(turtle_folder + 'provenance-geonames-locations.ttl', 'w') as turtle_file:
        turtle_file.write(provenance_turtle)
    
    print    
    print "Done, added provenance."
    
if __name__ == "__main__":
    main()