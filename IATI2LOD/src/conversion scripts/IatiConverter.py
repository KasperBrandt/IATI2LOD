## By Kasper Brandt
## Last updated on 24-04-2013

from rdflib import Namespace, Literal, XSD, URIRef, Graph, RDF, RDFS
import xml.etree.ElementTree as ET
import IatiElements, AttributeHelper


class ConvertActivity :
    '''Class for converting a IATI activity XML to a RDFLib Graph.'''
    
    def __init__(self, xml, version, linked_data_default):
        '''Initializes the activity class.
        
        Parameters
        @xml: An ElementTree of an activity.
        @version: The version of the activities.'''
        
        self.xml = xml
        
        self.id = self.get_id()
        self.last_updated = AttributeHelper.attribute_key(self.xml, 'last-updated-datetime')
        
        self.version = self.determine_version(version)
        self.linked_data_uri = self.determine_linked_data_uri(linked_data_default, self.id)
        
        self.hierarchy = AttributeHelper.attribute_key(self.xml, 'hierarchy')

    def determine_version(self, version):
        '''Determines the version of this activity.
        
        Parameters
        @version: The version of the iati-activities attribute.
        
        Returns
        @version: The iati-activity or iati-activities attribute version.'''
        
        activity_version = AttributeHelper.attribute_key(self.xml, 'version')
        
        if not activity_version == None:
            return activity_version
        
        else:
            return version
        
    def determine_linked_data_uri(self, linked_data_default, id):
        '''Determines the Linked Data URI of this activity.
        
        Parameters
        @linked_data_default: The version of the iati-activities attribute.
        @id: The ID of the activity.
        
        Returns
        @linked_data_uri: The Linked Data URI or None if not specified.'''
        
        linked_data_uri = AttributeHelper.attribute_key(self.xml, 'linked-data-uri')
        
        if not linked_data_uri == None:
            return linked_data_uri
        
        elif not linked_data_default == None:
            return str(linked_data_default) + str(id)
        
        else:
            return None
    
    def get_id(self):
        '''Returns the ID of the activity.
        
        Returns
        @activity_id: The ID of the activity.'''
        
        id = AttributeHelper.attribute_text(self.xml, 'iati-identifier')
        
        if not id == None:
            return str(id[0].split()[0])
        
        return id
    
    def get_default_type(self, type):
        '''Returns a default type of the activity.
        
        Parameters
        @type: The element that should be retrieved.
        
        Returns
        @default_type: The default finance type of the activity.'''
        
        default_type = self.xml.find(type)
        
        if default_type == None:
            return None
        
        return AttributeHelper.attribute_key(default_type, 'code') 
    
    def get_activity_defaults(self):
        '''Returns the defaults of the activity.
        
        Returns
        @defaults: A dictionary containing the defaults of the activity.'''
        
        defaults = dict([('id', self.id),
                         ('language', AttributeHelper.attribute_key(self.xml, '{http://www.w3.org/XML/1998/namespace}lang')),
                         ('currency', AttributeHelper.attribute_key(self.xml, 'default-currency')),
                         ('finance_type', self.get_default_type('default-finance-type')),
                         ('flow_type', self.get_default_type('default-flow-type')),
                         ('aid_type', self.get_default_type('default-aid-type')),
                         ('tied_status', self.get_default_type('default-tied-status')),
                         ('hierarchy', self.hierarchy),
                         ('linked_data_uri', self.linked_data_uri)])
        
        return defaults
    
    def convert(self, namespace):
        '''Converts the XML file into a RDFLib graph.
        
        Parameters
        @namespace: A RDFLib Namespace.
        
        Returns
        @graph: The RDFLib Graph of the activity.
        @id: The ID of the activity.
        @last_updated: The DateTime of the last update.
        @version: The version of the activity.'''
        
        if (self.id == None) or (self.id == ""):
            return None, None, None, None
        
        defaults = self.get_activity_defaults()
        defaults['namespace'] = namespace
        
        converter = IatiElements.ActivityElements(defaults)
        
        for attribute in self.xml:
            
            try:
                if ":" in attribute.tag:
                    funcname = attribute.tag.split(":")[1].replace("-","_").replace("default_", "")
                else:
                    funcname = attribute.tag.replace("-","_").replace("default_", "")
            
                update = getattr(converter, funcname)
                update(attribute)
                
            except AttributeError as e:
                try:
                    converter.convert_unknown(attribute)
                except:
                    print "Could not convert "+ funcname + " in file " + self.id + ": " + str(e)
        
        return converter.get_result(), self.id, self.last_updated, self.version
        
class ConvertCodelist :
    '''Class for converting a codelist dictionary to a RDFLib.'''
    
    def __init__(self, xml):
        '''Initializes the codelist class.
        
        Parameters
        @xml: The XML file of the codelist.'''
        
        self.graph = Graph()
        self.xml = xml
        
        self.id = AttributeHelper.attribute_key(self.xml, 'name')
        self.last_updated = AttributeHelper.attribute_key(self.xml, 'date-last-modified')

    def get_codelist_defaults(self):
        '''Retrieves the defaults for the codelist.
        
        Return
        @defaults: A dictionary of defaults.'''

        defaults = dict([('id', self.id),
                         ('language', AttributeHelper.attribute_key(self.xml, '{http://www.w3.org/XML/1998/namespace}lang'))])
        
        return defaults        
        
    def convert(self, namespace):
        '''Converts the XML file into a RDFLib graph.
        
        Parameters
        @namespace: A RDFLib Namespace.
        
        Returns
        @graph: The RDFLib Graph of the activity.
        @id: The ID of the activity.
        @last_updated: The DateTime of the last update.'''
        
        if (self.id == None) or (self.id == ""):
            return None, None, None

        defaults = self.get_codelist_defaults()
        defaults['namespace'] = namespace
        
        converter = IatiElements.CodelistElements(defaults)
        
        for entry in self.xml:
            
            # Get code, language and category code from entry
            code = AttributeHelper.attribute_text(entry, 'code')
            language = AttributeHelper.attribute_text(entry, 'language')
            category_code = AttributeHelper.attribute_text(entry, 'category')
            
            for attribute in entry:
                
                try:
                    funcname = attribute.tag.replace("-","_")
                
                    update = getattr(converter, funcname)
                    update(attribute, code, language, category_code)
                    
                except AttributeError as e:
                    print "Error in " + funcname + ", " + self.id + ": " + str(e)
        
        
        # Add 'is codelist type' statement 
        resulting_graph = converter.get_result()

        resulting_graph.add((namespace['codelist/' + self.id],
                             RDF.type,
                             namespace['codelist']))
        
        # Add label for codelist
        resulting_graph.add((namespace['codelist/' + self.id],
                             RDFS.label,
                             Literal(self.id, lang=defaults['language'])))    
        
                
        return resulting_graph, self.id, self.last_updated
    
class ConvertOrganisation :
    '''Class for converting a IATI organisation XML to a RDFLib Graph.'''
    
    def __init__(self, xml):
        '''Initializes the organisation class.
        
        Parameters
        @xml: An ElementTree of an activity.'''
        
        self.xml = xml
        
        self.id = self.get_id()
        self.last_updated = AttributeHelper.attribute_key(self.xml, 'last-updated-datetime')

        
    def get_id(self):
        '''Returns the ID of the organisation.
        
        Returns
        @activity_id: The ID of the organisation.'''
        
        id = AttributeHelper.attribute_text(self.xml, 'iati-identifier')
        
        if not id == None:
            return str("-".join(id[0].split()))
        
        elif id == None:
            id = AttributeHelper.attribute_text(self.xml, 'identifier')
            
            if not id == None:
                return str("-".join(id[0].split()))
        
#            if id == None:
#                try:
#                    id = self.xml.find('reporting-org').attrib['ref']
#                except:
#                    id = None
        
        return id

    def get_organisation_defaults(self):
        '''Returns the defaults of the organisation.
        
        Returns
        @defaults: A dictionary containing the defaults of the activity.'''
        
        defaults = dict([('id', self.id),
                         ('language', AttributeHelper.attribute_key(self.xml, '{http://www.w3.org/XML/1998/namespace}lang')),
                         ('currency', AttributeHelper.attribute_key(self.xml, 'default-currency'))])
        
        return defaults
    
    def convert(self, namespace):
        '''Converts the XML file into a RDFLib graph.
        
        Parameters
        @namespace: A RDFLib Namespace.
        
        Returns
        @graph: The RDFLib Graph of the activity.
        @id: The ID of the activity.
        @last_updated: The DateTime of the last update.'''
        
        if (self.id == None) or (self.id == ""):
            return None, None, None
        
        defaults = self.get_organisation_defaults()
        defaults['namespace'] = namespace
        
        converter = IatiElements.OrganisationElements(defaults)
        
        for attribute in self.xml:
            
            try:
                if ":" in attribute.tag:
                    funcname = attribute.tag.split(":")[1].replace("-","_").replace("default_", "")
                else:
                    funcname = attribute.tag.replace("-","_").replace("default_", "")
                
                funcname = attribute.tag.replace("-","_")
            
                update = getattr(converter, funcname)
                update(attribute)
                
            except AttributeError as e:
                try:
                    converter.convert_unknown(attribute)
                except:
                    print "Could not convert "+ funcname + " in file " + self.id + ": " + str(e)
        
        return converter.get_result(), self.id, self.last_updated

class ConvertProvenance :
    '''Class for adding provenance to the general provenance RDFLib Graph.'''
    
    def __init__(self, type, json_parsed, provenance, id, last_updated, version):
        '''Initializes the activity class.
        
        Parameters
        @type: The type of entity, such as activity or organisation.
        @json: A parsed JSON object of the metadata.
        @provenance: A RDFLib Graph of the provenance thus far.
        @id: The id of the entity.
        @last_updated: The last updated time of the entity.
        @version: The version of the entity.
        @document_name: The name of the original document.'''
        
        self.defaults = dict([('type', type),
                              ('json', json_parsed),
                              ('provenance', provenance),
                              ('id', id),
                              ('last_updated', last_updated),
                              ('version', version),
                              ('document_name', json_parsed['name'])])
        
        self.json = json_parsed
    
    def convert(self, namespace):
        '''Converts the JSON and XML attributes into a RDFLib graph.
        
        Parameters
        @namespace: A RDFLib Namespace.
        
        Returns
        @graph: The RDFLib Graph of the provenance.'''
        
        if (self.defaults['id'] == None) or (self.defaults['id'] == ""):
            return None
        
        converter = IatiElements.ProvenanceElements(self.defaults, namespace)
        
        for entry in self.json:
            
            try:
                funcname = entry.replace("-","_").replace("id","func_id").replace("version", "func_version")
            
                update = getattr(converter, funcname)
                update(self.json[entry])
                
            except AttributeError as e:
                print "Error in " + funcname + ", " + self.defaults['id'] + ": " + str(e)
        
        provenance = converter.get_result()
        
        return provenance      
    
    