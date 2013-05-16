## IatiCrawler.py
## By Kasper Brandt
## Last updated on 11-04-2013

import xml.etree.ElementTree as ET
from SPARQLWrapper import SPARQLWrapper, JSON
from datetime import date
import sys, httplib2, json, os

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
        
    except KeyError as e:
        print "Something went wrong while connecting to " + url
        return None
    
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
        
        with open(folder + name, 'w') as file:
            file.write(xml)
    
def retrieve_document_names(iati_url, limit, type):
    '''Check connection to IATI API and retrieve all document names.
    
    Parameters
    @iati_url: The URL of the IATI datasets.
    @limit: The max limit of the IATI server.
    @type: The type of documents that should be retrieved.
    
    Returns
    @all_documents: A list of a all document names.'''

    # Set IATI url
    if type == 'activities':
        url = iati_url + "search/dataset?filetype=activity"
        json = True
    elif type == 'organisations':
        url = iati_url + "search/dataset?filetype=organisation"
        json = True
    elif type == 'codelists':
        url = "http://datadev.aidinfolabs.org/data/codelist.xml"
        json = False
    
    data = get_request(url, json)
    all_documents = []
    
    if (not data == None) and (json):
        # activity and organisation documents
        print "Connection to IATI API established..."
        
        document_count = data['count']
        offset = 0
        
        while document_count > 0:
        
            document_count_url = url + "&limit=" + str(document_count) + "&offset=" + str(offset)
            
            documents = get_request(document_count_url, True)
            
            for document in documents['results']:
                all_documents.append(document)
            
            offset += limit
            document_count -= limit
            
        print "Document list retrieved..."
    
    elif (not data == None) and (not json):
        # codelist XMLs
        print "Connection to IATI API established..."
                
        parsed_xml = ET.fromstring(data)
    
        for codelist in parsed_xml.findall('codelist'):
            all_documents.append(str(codelist.find('name').text) + '.xml')
        
        print "Document list retrieved..."
    
    else:
        print "Something went wrong while connecting to the IATI API..."
        sys.exit(0)
    
    return all_documents

def update_documents(folder, iati_url, all_documents, server_update, type):
    '''Checking documents with the last time the server has been updated.
    Updates the triple store with new or updated activities.
    
    Parameters
    @folder: Location of folder in which XML files are to be saved.
    @iati_url: The URL of the IATI API.
    @all_documents: A list of a all document names.
    @server_update: A DateTime of the last time the XMLs were checked.
    @type: The type of documents that should be retrieved.'''
    
    # Settings
    if type == 'activities' or type == 'organisations':
        url = iati_url + "rest/dataset/"
        json_bool = True
    elif type == 'codelists':
        url = "http://datadev.aidinfolabs.org/data/codelist/"
        json_bool = False
    
    #folder = str(folder) + str(type) + '/Update ' + str(date.today()) + '/'
    folder = str(folder) + str(type) + '/'
    counter = 1
    
    if not os.path.isdir(folder):
        os.makedirs(folder)
    
    # DEBUG: last 100 documents only
    if type == 'activities':
        all_documents = all_documents[-200:]
    
    # Check the last update for each document.
    for document in all_documents:
        
        data = get_request(url + str(document), json_bool)
        
        if json_bool:
            # Check if the activity or organisation data is open and if updating is needed.
            if (data['isopen']) and (server_update < data['metadata_modified']):
                
                # Save JSON metadata to folder
                with open(folder + document + '.json', 'w') as file:
                    file.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
                
                # Save XML to folder
                save_to_folder(folder, data['download_url'].replace(' ','%20'), document + '.xml')
                print "Progress: " + str(counter) + " out of " + str(len(all_documents)) + "..."
                    
            else:
                print "Skipping " + str(document) + "..."
        
        else:
            parsed_codelist_xml = ET.fromstring(data)
            
            if server_update < parsed_codelist_xml.attrib['date-last-modified']:
                
                save_to_folder(folder, url + str(document), document)
                print "Progress: " + str(counter) + " out of " + str(len(all_documents)) + "..."
                
            else:
                print "Skipping " + str(document) + "..."
        
        counter += 1

def main():
    '''Crawls the IATI registry for activity, organisation and codelist XMLs 
    and stores the XMLs locally.'''
    
    # Initial settings
    max_limit = 1000
    folder = "/media/Acer/School/IATI-data/xml/"
    iati_url = "http://www.iatiregistry.org/api/"
    retrieve = ['activities', 'organisations', 'codelists']
    
    # Last time the script was run: "2013-22-04"
    last_time_updated = "1990"
    
    for type in retrieve:
        print "Start retrieving " + str(type) + "..."
        
        # Check whether the IATI API is working and retrieve all document names
        all_documents = retrieve_document_names(iati_url, max_limit, type)
    
        print "Storing XML files to local folder..."
        # Adds XMLs to local folder.
        update_documents(folder, iati_url, all_documents, last_time_updated, type)
    
    print "Done!"
    
if __name__ == "__main__":
    main()