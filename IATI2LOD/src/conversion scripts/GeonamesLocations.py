## By Kasper Brandt
## Last updated on 01-05-2013

import urllib, urllib2, httplib2, sys, json

# Create a SPARQL query to retrieve all locations.
# Store the location URI, name and (if present) gazzetteer entry.

url = 'http://eculture.cs.vu.nl:1987/iati/servlets/login'   
body = {'user': 'admin', 'password': 'iatiadmin'}
headers = {'Content-type': 'application/x-www-form-urlencoded'}
response, content = httplib2.Http().request(url, 'POST', headers=headers, body=urllib.urlencode(body))

headers = {'Cookie': response['set-cookie']}

# QUERY

#query = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#
#SELECT ?location ?name WHERE {
#   ?location rdf:type <http://purl.org/collections/iati/location> .
#   ?location rdfs:label ?name .
#}
#LIMIT 100'''

query = """SELECT DISTINCT ?relation
WHERE {
?location rdf:type <http://purl.org/collections/iati/location> .
?location ?relation ?other .
}
"""

params = dict([('query', query),
               ('format', 'json')])

params_encoded = urllib.urlencode(params).replace('+', '%20').replace('%0A%0A','%20')

request_url = "http://eculture.cs.vu.nl:1987/iati/sparql/update?" + params_encoded

response, content = httplib2.Http().request(request_url, 'POST', headers=headers)

print response
# Need validation for correct response

content_json = json.loads(content)

for result in content_json['results']['bindings']:
    print result['relation']['value']    
#    print result['name']['value']

#for value in content_json["results"]["bindings"]["s"]["value"]:
#    print value