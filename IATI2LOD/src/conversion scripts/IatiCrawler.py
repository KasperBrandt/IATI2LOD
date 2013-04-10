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
        return None

def save_to_folder(folder, xml_url, name):
    '''Check connection to IATI API and retrieve all document names.
    Retrieve all document names and the last time the server has checked for updates.
    
    Parameters
    @folder: The location of the folder.
    @xml_url: The URL of the XML containing activities.
    @name: The document name.'''
    
    xml = get_request(xml_url, False)
    
    if not xml == None:
        
        with open(folder + name + '.xml', 'w') as file:
            file.write(xml)
    
def check_connection(iati_url, limit):
    '''Check connection to IATI API and retrieve all document names.
    
    Parameters
    @iati_url: The URL of the IATI datasets.
    @limit: The max limit of the IATI server.
    
    Returns
    @all_documents: A list of a all document names.'''
    
    iati_url = iati_url + "search/dataset?filetype=activity"
    
    data = get_request(iati_url, True)
    
    if not data == None:
        print "Connection to IATI API established..."
        
        document_count = data['count']
        offset = 0
        
        all_documents = []
        
        while document_count > 0:
        
            document_count_url = iati_url + "&limit=" + str(document_count) + "&offset=" + str(offset)
            
            documents = get_request(document_count_url, True)
            
            for document in documents['results']:
                all_documents.append(document)
            
            offset += limit
            document_count -= limit
            
        print "Document list retrieved..."
        
        return all_documents
    
    else:
        sys.exit(0)

def update_documents(folder, iati_url, all_documents, server_update):
    '''Checking documents with the last time the server has been updated.
    Updates the triple store with new or updated activities.
    
    Parameters
    @folder: Location of folder in which XML files are to be saved.
    @iati_url: The URL of the IATI API.
    @all_documents: A list of a all document names.
    @server_update: A DateTime of the last time the XMLs were checked.'''
    
    # Settings
    iati_url = iati_url + "rest/dataset/"
    counter = 1
    
    # Check the last update for each document.
    for document in all_documents:
        
        data = get_request(iati_url + str(document), True)
        
        # Check if the data is open and if updating is needed.
        if (data['isopen']) and (server_update < data['metadata_modified']):
            
                save_to_folder(folder, data['download_url'].replace(' ','%20'), document)
                
        else:
            print "Skipping " + str(document) + "..."
        
        print "Progress: " + str(counter) + " out of " + str(len(all_documents)) + "..."
        
        counter += 1

def main():
    '''Crawls the IATI registry for XMLs and stores the XMLs locally.'''
    
    # Initial settings
    iati_url = "http://www.iatiregistry.org/api/"
    max_limit = 1000
    folder = "/media/Acer/School/IATI2LOD/IATI2LOD/xml/"
    
    # Last time the script was run: "2013-10-04"
    last_time_updated = "1990"
    
    print "Checking connection to IATI API..."
    # Check whether the IATI API is working and retrieve all document names
    all_documents = check_connection(iati_url, max_limit)
    
    print "Storing XML files to local folder..."
    # Checking documents with the last time they have been checked.
    # Adds XMLs to local folder.
    update_documents(folder, iati_url, all_documents, last_time_updated)
    
    print "Done!"
    
if __name__ == "__main__":
    main()