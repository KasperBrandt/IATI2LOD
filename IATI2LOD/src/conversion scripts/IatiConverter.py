## IatiConverter.py
## By Kasper Brandt
## Last updated on 13-04-2013

from rdflib import Namespace, Literal, XSD, URIRef, Graph, RDF, RDFS
import xml.etree.ElementTree as ET
import IatiElements, AttributeHelper


class ConvertActivity :
    '''Class for converting a IATI activity XML to a RDFLib Graph.'''
    
    def __init__(self, xml):
        '''Initializes the activity class.
        
        Parameters
        @xml: An ElementTree of an activity.'''
        
        self.xml = xml
        
        self.id = self.get_id()
        self.last_updated = AttributeHelper.attribute_key(self.xml, 'last-updated-datetime')
        
        self.possible_keys = dict([('iati-activity', ['version',
                                                      'last-updated-datetime',
                                                      'default-currency',
                                                      'hierarchy',
                                                      'linked-data-uri',
                                                      '{http://www.w3.org/XML/1998/namespace}lang']),
                                   ('title', ['{http://www.w3.org/XML/1998/namespace}lang'])])

    
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
                         ('tied_status', self.get_default_type('default-tied-status'))])
        
        return defaults
    
    def convert(self, namespace):
        '''Converts the XML file into a RDFLib graph.
        
        Parameters
        @namespace: A RDFLib Namespace.
        
        Returns
        @graph: The RDFLib Graph of the activity.
        @id: The ID of the activity.
        @last_updated: The DateTime of the last update.'''
        
        if self.id == None:
            return None, None, None
        
        defaults = self.get_activity_defaults()
        defaults['namespace'] = namespace
        
        converter = IatiElements.ActivityElements(defaults)
        
        for attribute in self.xml:
            
            try:
                funcname = attribute.tag.replace("-","_").replace("default_", "")
            
                update = getattr(converter, funcname)
                update(attribute)
                
            except AttributeError as e:
                print "Error in " + funcname + ", " + self.id + ": " + str(e)
        
        return converter.get_result(), self.id, self.last_updated
        
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
        
        if self.id == None:
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
            return str(id[0].split()[0])
        
        elif id == None:
            id = AttributeHelper.attribute_text(self.xml, 'identifier')
            
            if not id == None:
                return str(id[0].split()[0])
        
            if id == None:
                try:
                    id = self.xml.find('reporting-org').attrib['ref']
                except:
                    id = None
        
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
        
        if self.id == None:
            return None, None, None
        
        defaults = self.get_organisation_defaults()
        defaults['namespace'] = namespace
        
        converter = IatiElements.OrganisationElements(defaults)
        
        for attribute in self.xml:
            
            try:
                funcname = attribute.tag.replace("-","_")
            
                update = getattr(converter, funcname)
                update(attribute)
                
            except AttributeError as e:
                print "Error in " + funcname + ", " + self.id + ": " + str(e)
        
        return converter.get_result(), self.id, self.last_updated
    