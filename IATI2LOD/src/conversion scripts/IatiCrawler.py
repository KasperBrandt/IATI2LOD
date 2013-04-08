import xml.etree.ElementTree as ET
from SPARQLWrapper import SPARQLWrapper, JSON
from IatiConverter import iati_activity
import sys, httplib2, json

def get_request(url, json_format):
    '''Connect to url and return content.
    
    Parameters
    @url: The URL to connect to.
    @json_format: True for json and False for other formats.
    
    Returns
    @data: Dictionary of response.'''
    
    try:
        response, content = httplib2.Http().request(url, "GET")
        
    except httplib2.ServerNotFoundError as e:
        print e
        sys.exit(0)
    
    if response['status'] == '200':
        
        if json_format:
            data = json.loads(content)
        else:
            data = content
        
        return data
    
    else:
        print "Something went wrong while connecting to " + url
        sys.exit(0)

def check_triple_store(triple_store):
    '''Check connection to triple store and retrieve the last server update.
    Program quits when no connection could be established.
    '0' is returned when no date is known.
    
    Parameters
    @triple_store: The URL of the triple store.
    
    Returns
    @last_updated: A DateTime of the last update.'''
    
    context = triple_store + "/context/provenance"
    
    query = """
    SELECT ?date
    FROM NAMED <""" + context + """>
    WHERE {
        GRAPH <""" + context + """>
            { <""" + triple_store + """/context/iati> 
              <""" + triple_store + """/last-updated>
              ?date . }
    }
    """
    
    wrapper = SPARQLWrapper(triple_store)
    wrapper.setQuery(query)
    wrapper.setReturnFormat(JSON)
    
    try:
        content = wrapper.query().convert()
        print "Connection to triple store established..."
        
        last_updated = content['results']['bindings'][0]['date']['value']
    except AttributeError:
        last_updated = '0'
    except:
        print "Something went wrong while connecting to the triple store."
        sys.exit(0)
    
    return last_updated

def check_iati(iati_url):
    '''Check whether the triple store and IATI API are working.
    Retrieve all document names and the last time the server has checked for updates.
    
    Parameters
    @iati_url: The URL of the IATI datasets.
    
    Returns
    @all_documents: A list of a all document names.'''
    
    data = get_request(iati_url, True)
    print "Connection to IATI API established..."
    
    document_count = data['count']
    document_count_url = iati_url + "&limit=" + str(document_count)
    
    documents = get_request(document_count_url, True)
    print "Document list retrieved..."
    
    all_documents = documents['results']
    
    return all_documents

def update_document(triple_store, xml_url, activities_in_document):
    '''Check connection to IATI API and retrieve all document names.
    Retrieve all document names and the last time the server has checked for updates.
    
    Parameters
    @triple_store: The URL of the triple store.
    @xml_url: The URL of the XML containing activities.
    @activities_in_document: Total number of activities in the document.
    
    Returns
    @Updated activities: An integer of updated activities.'''
    
    xml = get_request(xml_url, False)
    parsed_xml = ET.fromstring(xml)
    
    count = 0
    
    for activity in parsed_xml.findall('iati-activity'):
        
        activity_parser = iati_activity(activity)
        
        last_activity_update = activity_parser.get_last_update()
        activity_id = activity_parser.get_id()
        
        print str(last_activity_update) +" en ID is: "+ str(activity_id)
        
        #### HIER GEBLEVEN ####
        
        sys.exit(0)
        
        count += 1
    
    return count
    
def check_connections(triple_store, iati_url):
    '''Check connection to IATI API and retrieve all document names.
    Retrieve all document names and the last time the server has checked for updates.
    
    Parameters
    @triple_store: The URL of the triple store.
    @iati_url: The URL of the IATI datasets.
    
    Returns
    @all_documents: A list of a all document names.
    @server_update: A DateTime of the last server update.'''
    
    iati_url = iati_url + "search/dataset?filetype=activity"
    
    # Check connection to triple store and retrieve the last server update.
    server_update = check_triple_store(triple_store)
    
    # Check connection to IATI API and retrieve all document names.
    all_documents = check_iati(iati_url)
    
    return all_documents, server_update

def update_documents(triple_store, iati_url, all_documents, server_update):
    '''Checking documents with the last time the server has been updated.
    Updates the triple store with new or updated activities.
    
    Parameters
    @triple_store: The URL of the triple store.
    @iati_url: The URL of the IATI API.
    @all_documents: A list of a all document names.
    @server_update: A DateTime of the last server update.'''
    
    # Settings
    iati_url = iati_url + "rest/dataset/"
    counter = 1
    activities_updated_count = 0
    
    # Check the last update for each document.
    for document in all_documents:
        
        data = get_request(iati_url + str(document), True)
        
        # Check if the data is open and if updating is needed.
        if (data['isopen']) and (server_update < data['metadata_modified']):
                print str(document) + " needs updating..."
                
                activity_count = data['extras']['activity_count']
                
                activities_updated = update_document(triple_store, data['download_url'], activity_count)
                activities_updated_count += activities_updated
        
        # DEBUG: take only first document.
        if counter == 1:
            print "Number of activities updated: " + str(activities_updated_count)
            
            sys.exit(0)
            break
        
        counter += 1

def main():
    '''Updates the Triple Store based on IATI data'''
    
    # Initial settings
    triple_store = "http://localhost:8080/openrdf-sesame/repositories/iati"
    iati_url = "http://www.iatiregistry.org/api/"
    
    print "Checking connections..."
    # Check whether the triple store and IATI API are working.
    # Retrieve all document names and the last time the server has checked for updates.
    all_documents, server_update = check_connections(triple_store, iati_url)
    
    print "Checking which documents have been updated..."
    # Checking documents with the last time the server has been updated.
    # Updates the triple store with new or updated activities.
    update_documents(triple_store, iati_url, all_documents, server_update)
    
    print "Updating the server update time..."
    # Update the provenance named graph
    update_provenance(triple_store)
    
    print "Done!"
    
if __name__ == "__main__":
    main()