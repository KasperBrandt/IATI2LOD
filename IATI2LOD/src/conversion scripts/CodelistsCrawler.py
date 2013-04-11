## CodelistsCrawler.py
## By Kasper Brandt
## Last updated on 27-03-2013

import xml.etree.ElementTree as ET
import httplib2, urllib, sys
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Namespace, Literal, XSD, URIRef, Graph
from SparqlContext import context
from CodelistsConverter import codelist
from datetime import datetime

def connect_to_server(request):
    '''Connects to the server and returns contents if the status is OK.
    
    Parameters
    @request: The location of the codelists API, an XML file.
    
    Returns
    @content: The contents returned by the request.'''
    
    try:
        response, content = httplib2.Http().request(request, "GET")
    except httplib2.ServerNotFoundError as e:
        print e
        sys.exit(0)
    
    if response['status'] == '200':
        return content
    else:
        print "Something went wrong while retrieving the XML, status: " + str(response['status'])
        sys.exit(0)

def query_last_server_update(triple_store):
    '''Retrieves the last time the codelists were checked for updates.
    
    Parameters
    @triple_store: The URL of the triple store.
    
    Returns
    @update_date: The datetime of the last update.
    @provenance_graph: A RDFLib Graph containing provenance information.'''
    
    iati_context = Namespace(triple_store + "/context/")
    
    sparql = SPARQLWrapper(triple_store)

    sparql.setQuery("""
    SELECT ?date
    FROM NAMED <""" + iati_context['provenance'] + """>
    WHERE {
        GRAPH <""" + iati_context['provenance'] + """> {
            <""" + iati_context['codelists']  + """>
            <""" + iati_context['last-updated'] + """>
            ?date .
        }
    }
    """)
    
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    provenance_graph = Graph()
    
    try:
        provenance_graph.add((iati_context['codelists'],
                              iati_context['last-updated'],
                              Literal(results['results']['bindings'][0]['date']['value'], datatype = XSD.dateTime)))
        
        return results['results']['bindings'][0]['date']['value'], provenance_graph
    except:
        return '0', Graph()
        
def get_codelists(xml, last_server_update, xml_base_url):
    '''Retrieves all codelists from the XML file.
    
    Parameters
    @xml: The XML containing all codelists.
    @last_server_update: Datetime of the last server check for codelists.
    @xml_base_url: The base URL of the XMLs.
    
    Returns
    @codelists: A nested dictionary containing all codelists.'''
    
    codelists = {}
    
    parsed_xml = ET.fromstring(xml)

    for codelist in parsed_xml.findall('codelist'):
        codelists[codelist.find('name').text] = {}
    
    for codelist in codelists.keys():
        this_codelist = {}
        
        xml_location = xml_base_url + "codelist/" + codelist + ".xml"
        codelist_xml = connect_to_server(xml_location)
        
        parsed_codelist_xml = ET.fromstring(codelist_xml)
        
        this_codelist['date-last-modified'] = parsed_codelist_xml.attrib['date-last-modified']
        
        if str(last_server_update) < str(parsed_codelist_xml.attrib['date-last-modified']):
            code_iter = 0
            
            for attribute in parsed_codelist_xml:
                this_codelist_code = {}
                code_iter += 1
                
                for code in attribute:
                    this_codelist_code[code.tag] = code.text
                    
                this_codelist[code_iter] = this_codelist_code
                
            codelists[codelist] = this_codelist
        
        else:
            codelists.pop(codelist)
    
    return codelists

def empty_dict(dictionary):
    '''Checks whether a dictionary is filled or not.
    
    Parameters
    @dictionary: A dictionary.
    
    Returns
    @status: True in case the dictionary is empty and False otherwise.'''
    
    for something in dictionary:
        return False
    
    return True

def query_codelist_graph(triple_store, context_uri):
    '''Queries the triple store for all codelists.
    
    Parameters
    @triple_store: The URL of the triple store.
    
    Returns
    @graph: A RDFLib graph containing all codelists.'''
    
    conversion = context(triple_store, context_uri)
    graph = conversion.convert()
    
    return graph

def update_codelist_graph(codelists, codelist_graph, triple_store):
    '''Updates the codelist graph with codelists to be updated.
    
    Parameters
    @codelists: A nested dictionary of the codelists to be updated.
    @codelist_graph: A RDFLib graph of the codelist context.
    @triple_store: The URL of the triple store.
    
    Returns
    @updated_graph: A RDFLib graph including the updated codelists.'''
    
    convert = codelist(codelists, codelist_graph, triple_store)
    
    updated_graph = convert.update()
    
    return updated_graph

def push_to_triple_store(graph, triple_store, context):
    '''Updates the triple stores
    
    Parameters
    @graph: The graph which is to be committed.
    @triple_store: The URL of the triple store.
    @context: The context to which the graph is to be committed. None for no context.
    
    Returns
    @status: Returned status from HTTP PUT request'''
    
    graph_data = graph.serialize()
    
    if not context == None:
        params = { 'context': '<' + context + '>' }
        
        endpoint = triple_store + "/statements?%s" % (urllib.urlencode(params))
    
    else:
        endpoint = triple_store + "/statements"
    
    (response, _content) = httplib2.Http().request(endpoint, 'PUT', 
                                                  body=graph_data, 
                                                  headers={ 'content-type': 'application/rdf+xml' })
    
    return response['status']

def update_codelists(codelists, triple_store):
    '''Updates the codelists which are to be updated.
    
    Parameters
    @codelists: A nested dictionary containing all codelists to be updated.
    @triple_store: The URL of the triple store.
    
    Returns
    @status: The HTTP PUT status of the update.'''
    
    context_uri = triple_store + "/context/codelists"
    
    empty = empty_dict(codelists)
    
    if empty == False:
        print "Updating triple store..."
        status = update_triple_store(codelists, triple_store, context_uri)
        print "Status of update: " + str(status)
    else:
        print "No update needed..."
        status = '204'
    
    return status

def update_triple_store(codelists, triple_store, context_uri):
    '''Updates the codelists which are to be updated.
    
    Parameters
    @codelists: A nested dictionary containing all codelists to be updated.
    @triple_store: The URL of the triple store.
    @context_uri: The URI of the context.
    
    Returns
    @status: The HTTP PUT status of the update.'''
    
    codelist_graph = query_codelist_graph(triple_store, context_uri)
    
    updated_graph = update_codelist_graph(codelists, codelist_graph, triple_store)
    
    status = push_to_triple_store(updated_graph, triple_store, context_uri)
    
    return status
    
def update_provenance(status, triple_store, provenance_graph):
    '''Updates the updated server time in the triple store.
    
    Parameters
    @status: Status of the codelist HTTP PUT request.
    @triple_store: The URL of the triple store.
    @provenance_graph: The RDFLib Graph containing provenance information.
    
    Returns
    @status: The HTTP PUT status of the update.'''
    
    context_uri = triple_store + "/context/codelists"
    
    if status > '199' and status < '300':
        now = datetime.now()
    
        iati_context = Namespace(triple_store + "/context/")
        
        provenance_graph.set((URIRef(context_uri),
                              iati_context['last-updated'],
                              Literal(str(now), datatype = XSD.dateTime)))
        
        status = push_to_triple_store(provenance_graph, triple_store, iati_context['provenance'])
    
        print "Status of provenance update: " + str(status)
     

def main():
    '''Checks for updates of the IATI codelists using their codelists API.
    Updates are pushed to a triple store.'''
    
    # Settings
    triple_store = "http://localhost:3020/"
    xml_base_url = "http://datadev.aidinfolabs.org/data/"
    
    print "Retrieving last server update..."
    # Retrieve the last time the server checked for updates
    last_server_update, provenance_graph = query_last_server_update(triple_store)
    
    print "Connecting to IATI server for codelists..."
    # Connect to the IATI server and retrieve contents of codelists
    xml = connect_to_server(xml_base_url + "codelist.xml")
    
    print "Calculating codelists that need updating..."
    # Retrieve all codelists which need updating
    codelists = get_codelists(xml, last_server_update, xml_base_url)
    
    # Update triple store if needed
    status = update_codelists(codelists, triple_store)
    
    # Update provenance
    provenance_status = update_provenance(status, triple_store, provenance_graph)
    
    print "Done!"
    
if __name__ == "__main__":
    main()