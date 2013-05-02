## By Kasper Brandt
## Last updated on 02-05-2013

import xml.etree.ElementTree as ET
import os, sys, httplib2, httplib, json, urllib, urllib2

# Cache login information
url = 'http://eculture.cs.vu.nl:1987/iati/servlets/login'   
body = {'user': 'admin', 'password': 'iatiadmin'}
headers = {'Content-type': 'application/x-www-form-urlencoded'}
response, content = httplib2.Http().request(url, 'POST', headers=headers, body=urllib.urlencode(body))

headers = {'Cookie': response['set-cookie']}

folder = "/media/Acer/School/IATI-statistics/"


############## CLASSES #################

classes = ['activity',
           'location',
           'budget',
           'sector',
           'policy-marker',
           'planned-disbursement',
           'region',
           'country',
           'condition',
           'coordinates',
           'gazetteer-entry',
           'transaction',
           'result',
           'indicator']

class_dict = {}

for class_thing in classes:
    
    done = False
    
    classes_query = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX iati: <http://purl.org/collections/iati/>
    
    SELECT (count(?entity) as ?count) WHERE {
       ?entity rdf:type iati:%s .
    }''' % (class_thing)
    
    params = dict([('query', classes_query),
                   ('format', 'json')])
    
    params_encoded = urllib.urlencode(params).replace('+', '%20').replace('%0A%0A','%20')
    
    request_url = "http://eculture.cs.vu.nl:1987/iati/sparql/update?" + params_encoded
    
    print "Retrieving " + class_thing + " count from triple store..."
    # Request all location with coordinates and precision
    try:
        response, content = httplib2.Http().request(request_url, 'POST', headers=headers)
    except httplib.IncompleteRead:
        class_dict[class_thing] = 0
        done = True
    
    if (response['status'] == '200') and (not done == True):

        content_json = json.loads(content)
    
        for result in content_json['results']['bindings']:
            count = result['count']['value']
            
        class_dict[class_thing] = count
        
    elif done == True:
        print "Could not find class " + class_thing + "..."
        
    else:
        print "Failed to connect, response status: " + str(response['status'])


############## RELATIONS #################

relations = ['activity-id',
             'activity-participating-org',
             'activity-reporting-org',
             'activity-start-actual-date',
             'activity-start-planned-date',
             'activity-end-actual-date',
             'activity-end-planned-date',
             'activity-sector',
             'activity-policy-marker',
             'activity-budget',
             'activity-planned-disbursement',
             'activity-recipient-region',
             'activity-recipient-country',
             'activity-condition',
             'related-activity',
             'activity-linked-data-uri',
             'activity-location',
             'location-coordinates',
             'location-gazetteer-entry',
             'location-administrative',
             'activity-transaction',
             'activity-result',
             'result-indicator',
             'organisation-id',
             'organisation-total-budget',
             'organisation-recipient-org-budget',
             'organisation-recipient-country-budget']

relation_dict = {}

for relation in relations:
    
    done = False

    relations_query = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX iati: <http://purl.org/collections/iati/>
    
    SELECT (count(?entity) as ?count) WHERE {
       ?entity iati:%s ?object .
    }''' % (relation)
    
    params = dict([('query', relations_query),
                   ('format', 'json')])
    
    params_encoded = urllib.urlencode(params).replace('+', '%20').replace('%0A%0A','%20')
    
    request_url = "http://eculture.cs.vu.nl:1987/iati/sparql/update?" + params_encoded
    
    print "Retrieving " + relation + " count from triple store..."
    # Request all location with coordinates and precision
    try:
        response, content = httplib2.Http().request(request_url, 'POST', headers=headers)
    except httplib.IncompleteRead:
        relation_dict[relation] = 0
        done = True
    
    if (response['status'] == '200') and (not done == True):

        content_json = json.loads(content)
    
        for result in content_json['results']['bindings']:
            count = result['count']['value']
            
        relation_dict[relation] = count
        
    elif done == True:
        print "Could not find relation " + relation + "..."
        
    else:
        print "Failed to connect, response status: " + str(response['status'])


############## PRINTING #################

print
print "Classes"

for class_key in class_dict.keys():
    print str(class_key) + "\t" + str(class_dict[class_key])
    
print
print "Relations"

for relation_key in relation_dict.keys():
    print str(relation_key) + "\t" + str(relation_dict[relation_key])


