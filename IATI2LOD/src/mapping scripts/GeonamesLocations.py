## By Kasper Brandt
## Last updated on 02-05-2013

from rdflib import RDF, RDFS, Literal, URIRef, Namespace, OWL
from rdflib.graph import Graph
import xml.etree.ElementTree as ET
import os, sys, httplib2, json, urllib, urllib2

def find_location(latitude, longitude, precision, country_info):
    '''Finds a location based on the lat/long and the precision.
    Returns the Geonames ID of the location.
    
    Parameters
    @latitude: A string of the latitude.
    @longitude: A string of the longitude.
    @precision: A string of the precision, ranging from 1 to 9.
    @country_info: An XML ETree containing all country information.
    
    Returns
    @GeonamesID: The ID of the Geonames location.'''
    
    geonames_uri = "http://api.geonames.org/"
    username = "KasperBrandt"
    
    if precision < '3':
        service = "findNearbyPlaceName?"
        featureCode = ""
        print "Finding nearby place name..."
    elif precision == '3':
        service = "findNearby?"
        featureCode = "ADM2"
        print "Finding nearby place ADM2..."
    elif (precision == '4') or (precision == '5'):
        service = "findNearby?"
        featureCode = "ADM1"
        print "Finding nearby place ADM1..."
    elif precision > '5':
        service = "countryCode?"
        featureCode = ""
        print "Finding nearby country or capital..."
    else:
        print "Something went wrong with the precision..."
    
    webservice = geonames_uri + service
        
    params = dict([('username', username),
                   ('lat', str(latitude)),
                   ('lng', str(longitude))])
    
    if not featureCode == "":
        params['fcode'] = featureCode
    
    params_encoded = urllib.urlencode(params).replace('+', '%20').replace('%0A%0A','%20')
            
    url = webservice + params_encoded
    
    try:
        response, content = httplib2.Http().request(url, "GET")
    
    except httplib2.ServerNotFoundError as e:
        print e
        return "Niets"
    
    if precision < '6':
        geonames_xml = ET.fromstring(content)
        geoname = geonames_xml.find('geoname')
        
        if not geoname == None:
            return geoname.find('geonameId').text
            
        else:
            status = geonames_xml.find('status')
            if not status == None:
                print status.attrib['message']
                if "timeout" in status.attrib['message']:
                    print "Trying again..."
                    return find_location(latitude, longitude, precision, country_info)
                return None
            else:
                print "Trying again, broad search..."
                
                webservice = geonames_uri + "findNearby?"
                    
                params = dict([('username', username),
                               ('lat', str(latitude)),
                               ('lng', str(longitude))])
                
                params_encoded = urllib.urlencode(params).replace('+', '%20').replace('%0A%0A','%20')       
                url = webservice + params_encoded
                
                try:
                    response, content = httplib2.Http().request(url, "GET")
                
                except httplib2.ServerNotFoundError as e:
                    print e
                    return "Niets"
                    
                geonames_xml = ET.fromstring(content)
                geoname = geonames_xml.find('geoname')
                
                if not geoname == None:
                    return geoname.find('geonameId').text
                    
                else:
                    status = geonames_xml.find('status')
                    if not status == None:
                        print status.attrib['message']
                        if "timeout" in status.attrib['message']:
                            print "Trying again..."
                            return find_location(latitude, longitude, precision, country_info)
                        return None
                    else:
                        return "Niets"
                        
    
    elif precision > '5':
        if len(content) > 5:
                print "Trying again, broad search..."
                
                webservice = geonames_uri + "findNearby?"
                    
                params = dict([('username', username),
                               ('lat', str(latitude)),
                               ('lng', str(longitude))])
                
                params_encoded = urllib.urlencode(params).replace('+', '%20').replace('%0A%0A','%20')       
                url = webservice + params_encoded
                
                try:
                    response, content = httplib2.Http().request(url, "GET")
                
                except httplib2.ServerNotFoundError as e:
                    print e
                    return "Niets"
                    
                geonames_xml = ET.fromstring(content)
                geoname = geonames_xml.find('geoname')
                
                if not geoname == None:
                    return geoname.find('geonameId').text
                    
                else:
                    status = geonames_xml.find('status')
                    if not status == None:
                        print status.attrib['message']
                        if "timeout" in status.attrib['message']:
                            print "Trying again..."
                            return find_location(latitude, longitude, precision, country_info)
                        return None
                    else:
                        return "Niets"
        
        country_code = content.rstrip()
            
        if (precision == '6') or (precision == '9'):
            print "Trying to find " + country_code + "..."
            for country in country_info:
                if country.find('countryCode').text == country_code:
                    return country.find('geonameId').text
            
            return "Niets"
                    
        elif (precision == '7') or (precision == '8'):
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
            
            try:
                response, content = httplib2.Http().request(url, "GET")
            
            except httplib2.ServerNotFoundError as e:
                print e
                return "Niets"
        
            geonames_xml = ET.fromstring(content)
            geoname = geonames_xml.find('geoname')
            
            if not geoname == None:
                return geoname.find('geonameId').text
                
            else:
                status = geonames_xml.find('status')
                if not status == None:
                    print status.attrib['message']
                    if "timeout" in status.attrib['message']:
                        print "Trying again..."
                        return find_location(latitude, longitude, precision, country_info)
                    return None            
                else:
                    return "Niets"

                    
def retrieve_countries():
    '''Looks up all country info.
    
    Returns
    @country_info: An XML ETree containing all country info.'''
    
    geonames_uri = "http://api.geonames.org/"
    username = "KasperBrandt"
    
    webservice = geonames_uri + "countryInfo?"
    
    params = dict([('username', username)])

    params_encoded = urllib.urlencode(params).replace('+', '%20').replace('%0A%0A','%20')
            
    url = webservice + params_encoded
    
    try:
        response, content = httplib2.Http().request(url, "GET")
    
    except httplib2.ServerNotFoundError as e:
        print e
        return None
        
    geonames_xml = ET.fromstring(content)
    
    status = geonames_xml.find('status')
    
    if status == None:
        return geonames_xml
    
    else:
        print status.attrib['message']
        return None
                                
        
def main():
    '''Looks up the geonames IDs of locations with coordinates and a precision.'''
    
    # Settings
    turtle_folder = "/media/Acer/School/IATI-data/mappings/"
    
    # Cache login information
    url = 'http://eculture.cs.vu.nl:1987/iati/servlets/login'   
    body = {'user': 'admin', 'password': 'iatiadmin'}
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    response, content = httplib2.Http().request(url, 'POST', headers=headers, body=urllib.urlencode(body))
    
    headers = {'Cookie': response['set-cookie']}
    
    # Initialize graph
    locations = Graph()
    locations.bind('iati', "http://purl.org/collections/iati/")
    locations.bind('gn', "http://sws.geonames.org/")
    locations.bind('owl', "http://www.w3.org/2002/07/owl#")
    
    Iati = Namespace("http://purl.org/collections/iati/")
    GN = Namespace("http://sws.geonames.org/")
    
    if not os.path.isdir(turtle_folder):
        os.makedirs(turtle_folder)
    
    print "Retrieving all country information..."
    # Retrieve all country information
    country_info = retrieve_countries()
    
    if country_info == None:
        sys.exit(0)
    
    # QUERY
    
    query = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX iati: <http://purl.org/collections/iati/>
    
    SELECT ?location ?type ?lat ?long ?preccode WHERE {
       ?location rdf:type iati:location .
       ?location iati:location-coordinates ?coordinates .
       ?coordinates iati:precision ?precision .
       ?precision iati:code ?preccode . 
       ?coordinates iati:latitude ?lat .
       ?coordinates iati:longitude ?long .
    }'''
    
    params = dict([('query', query),
                   ('format', 'json')])
    
    params_encoded = urllib.urlencode(params).replace('+', '%20').replace('%0A%0A','%20')
    
    request_url = "http://eculture.cs.vu.nl:1987/iati/sparql/update?" + params_encoded
    
    print "Retrieving all locations from triple store..."
    # Request all location with coordinates and precision
    response, content = httplib2.Http().request(request_url, 'POST', headers=headers)
    
    if response['status'] == '200':
    
        content_json = json.loads(content)
        
        count = 0
        count_nothing = 0
    
        for result in content_json['results']['bindings']:
            location = result['location']['value']
            latitude = result['lat']['value']
            longitude = result['long']['value']
            precision = result['preccode']['value']
            
            print "Lat/ long with precision " + str(precision) + " found for " + str(location) + "..."
            
            geonames_id = find_location(latitude, longitude, precision, country_info)
            
            if (not geonames_id == None) and (not geonames_id == "Niets"):
                
                print "Adding location " + str(geonames_id) + " to Graph..."
                locations.add((URIRef(location),
                               OWL.sameAs,
                               GN[str(geonames_id)]))
                
                count += 1
            
            elif geonames_id == "Niets":
                print "No match found..."
                
                count_nothing += 1
            
            elif geonames_id == None:
                print "Writing to file since credits are gone..."
                
                locations_turtle = locations.serialize(format='turtle')
    
                with open(turtle_folder + 'locations-mapping.ttl', 'w') as turtle_file:
                    turtle_file.write(locations_turtle)
                            
                print "Done, " + str(count) + " locations written to file..."
                
                sys.exit(0)
            
            else:
                print "Impossible scenario..."
                
    print "Writing to file..."
    
    locations_turtle = locations.serialize(format='turtle')
    
    with open(turtle_folder + 'geonames-locations.ttl', 'w') as turtle_file:
        turtle_file.write(locations_turtle)
                
    print "Done:"
    print str(count) + " locations written to file."
    print str(count_nothing) + " locations could not be found."

if __name__ == "__main__":
    main()