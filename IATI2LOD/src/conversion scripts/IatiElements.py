## iatiElements.py
## By Kasper Brandt
## Last updated on 08-04-2013

from rdflib import RDF, RDFS, Literal, URIRef
from rdflib.graph import Graph

class IatiElements :
    '''Class for converting XML elements of self.iati activities to a RDFLib self.graph.'''
    
    def __init__(self, defaults): 
        '''Initializes class.
        
        Parameters
        @defaults: A dictionary of defaults.'''
        
        self.defaults = defaults
        self.progress = dict()
        
        self.id = defaults['id']
        self.default_language = defaults['language']
        self.default_currency = defaults['currency']
        self.default_finance_type = defaults['finance_type']
        self.default_flow_type = defaults['flow_type']
        self.default_aid_type = defaults['aid_type']
        self.default_tied_status = defaults['tied_status']
        self.iati = defaults['namespace']
        
        self.graph = Graph()
        self.graph.bind('iati', self.iati)
    
    def __attribute_key(self, xml, key):
        '''Checks whether a key is in the XML.
        Returns the value of the key or None if not present.
        
        Parameters
        @xml: An ElementTree.
        @key: A string of the key.
        
        Returns
        @value: The value of the key or None if not present.'''
        
        try:
            return xml.attrib[key]
        
        except KeyError:
            return None

    def __attribute_text(self, xml, language):
        '''Checks whether an element has a text and picks the correct language.
        
        Parameters
        @xml: An ElemenTree of the element.
        @language: The default language of the activity.
        
        Returns
        @literal: A RDFLib Literal or None.'''
        
        if xml.text == None:
            return None
        
        node_language = self.__attribute_key(xml, "{http://www.w3.org/XML/1998/namespace}lang")
        
        text = xml.text
        formatted_text = " ".join(text.split())
        
        if not node_language == None:
            return Literal(formatted_text, lang=node_language)
        
        if not language == None:
            return Literal(formatted_text, lang=language)
        
        return Literal(formatted_text)
        
    def __update_progress(self, element):
        '''Updates the progress of the number of elements.
        
        Parameters
        @element: A string of the element name.'''
        
        try:
            self.progress[element] += 1
        except KeyError:
            self.progress[element] = 1

            
    def get_result(self):
        '''Returns the resulting self.graph of the activity.
        
        Returns
        @graph: The RDFLib self.graph with added statements.'''
        
        return self.graph           
    
    def reporting_org(self, xml):
        '''Converts the XML of the reporting-org element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        # Keys
        ref = self.__attribute_key(xml, 'ref')
        type = self.__attribute_key(xml, 'type')
        
        # Text
        name = self.__attribute_text(xml, self.default_language)
        
        if not ref == None:
            self.graph.add((self.iati['activity/' + self.id],
                            self.iati['activity-reporting-org'],
                            self.iati['activity/' + str(self.id) + '/activity-reporting-org/' + str(ref)]))
            
            self.graph.add((self.iati['activity/' + str(self.id) + '/activity-reporting-org/' + str(ref)],
                            RDF.type,
                            self.iati['organisation']))
            
            self.graph.add((self.iati['activity/' + str(self.id) + '/activity-reporting-org/' + str(ref)],
                            self.iati['organisation-code'],
                            self.iati['codelist/OrganisationIdentifier/' + str(ref)]))
        
            if not name == None:
                self.graph.add((self.iati['activity/' + self.id + '/activity-reporting-org/' + str(ref)],
                                RDFS.label,
                                name))
                
            if not type == None:
                self.graph.add((self.iati['activity/' + self.id + '/activity-reporting-org/' + str(ref)],
                                self.iati['organisation-type'],
                                self.iati['codelist/OrganisationType/' + str(type)]))

    
    def iati_identifier(self, xml):
        '''Converts the XML of the self.iati-identifier element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        # Text
        id = xml.text
        id = " ".join(id.split())
        
        if not id == None:
            self.graph.add((self.iati['activity/' + self.id],
                            self.iati['activity-id'],
                            Literal(id)))
    
    def other_identifier(self, xml):
        '''Converts the XML of the other-identifier element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        # Keys
        owner_ref = self.__attribute_key(xml, 'owner-ref')
        owner_name = self.__attribute_key(xml, 'owner-name')
        
        # Text
        name = xml.text
        name = " ".join(name.split())
        
        if not name == None:
            self.graph.add((self.iati['activity/' + self.id],
                            self.iati['activity-other-identifier'],
                            self.iati['activity/' + self.id + '/other-identifier' + str(name)]))
            
            if not owner_ref == None:
                self.graph.add((self.iati['activity/' + self.id + '/other-identifier' + str(name)],
                                self.iati['activity-other-identifier-owner-ref'],
                                self.iati['organisation/' + str(owner_ref)]))
            
            if not owner_name == None:
                self.graph.add((self.iati['activity/' + self.id + '/other-identifier' + str(name)],
                                self.iati['activity-other-identifier-owner-name'],
                                Literal(owner_name)))
    
    def activity_website(self, xml):
        '''Converts the XML of the activity-website element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        # Text
        website = xml.text
        website = " ".join(website.split())
        
        if not website == None:
            self.graph.add((self.iati['activity/' + self.id],
                            self.iati['activity-website'],
                            Literal(website)))
    
    def title(self, xml):
        '''Converts the XML of the title element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        # Text
        title = self.__attribute_text(xml, self.default_language)
        
        if not title == None:
            self.graph.add((self.iati['activity/' + self.id],
                            RDFS.label,
                            title))
    
    def description(self, xml):
        '''Converts the XML of the description element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        # Keys
        type = self.__attribute_key(xml, 'type')
        
        # Text
        description = self.__attribute_text(xml, self.default_language)
        
        # Progress
        self.__update_progress('description')
        
        if not description == None:
            self.graph.add((self.iati['activity/' + self.id],
                            self.iati['activity-description'],
                            self.iati['activity/' + self.id + '/description' + str(self.progress['description'])]))
            
            self.graph.add((self.iati['activity/' + self.id + '/description' + str(self.progress['description'])],
                            RDF.type,
                            self.iati['description']))
            
            self.graph.add((self.iati['activity/' + self.id + '/description' + str(self.progress['description'])],
                            self.iati['description'],
                            description))
            
            if not type == None:
                self.graph.add((self.iati['activity/' + self.id + '/description' + str(self.progress['description'])],
                                self.iati['description-type'],
                                self.iati['codelist/DescriptionType/' + str(type)]))
    
    def activity_status(self, xml):
        '''Converts the XML of the activity-status element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        # Keys
        code = self.__attribute_key(xml, 'code')
        
        if not code == None:
            self.graph.add((self.iati['activity/' + self.id],
                            self.iati['activity-status'],
                            self.iati['codelist/ActivityStatus/' + str(code)]))
    
    def activity_date(self, xml):
        '''Converts the XML of the activity-date element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        # Keys
        type = self.__attribute_key(xml, 'type')
        iso_date = self.__attribute_key(xml, 'iso-date')
        
        # Text
        date = xml.text
        date = " ".join(date.split())
        
        if not iso_date == None:
            date = iso_date
        
        if not date == None:
            if type == "start-actual":
                self.graph.add((self.iati['activity/' + self.id],
                                self.iati['activity-actual-start-date'],
                                Literal(date)))
                
            elif type == "end-actual":
                self.graph.add((self.iati['activity/' + self.id],
                                self.iati['activity-actual-end-date'],
                                Literal(date)))
            
            elif type == "start-planned":
                self.graph.add((self.iati['activity/' + self.id],
                                self.iati['activity-planned-start-date'],
                                Literal(date)))
                
            elif type == "end-planned":
                self.graph.add((self.iati['activity/' + self.id],
                                self.iati['activity-planned-end-date'],
                                Literal(date)))
    
    def contact_info(self, xml):
        '''Converts the XML of the contact-info element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        self.graph.add((self.iati['activity/' + self.id],
                        self.iati['activity-contact-info'],
                        self.iati['activity/' + self.id + '/contact-info']))
        
        for element in xml:
            
            info = element.text
            info = " ".join(info.split())
            
            self.graph.add((self.iati['activity/' + self.id + '/contact-info'],
                            self.iati[element.tag],
                            Literal(info)))
    
    def participating_org(self, xml):
        '''Converts the XML of the participating-org element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        # Keys
        ref = self.__attribute_key(xml, 'ref')
        type = self.__attribute_key(xml, 'type')
        role = self.__attribute_key(xml, 'role')
        
        # Text
        name = self.__attribute_text(xml, self.default_language)
        
        if not ref == None:
            self.graph.add((self.iati['activity/' + self.id],
                            self.iati['activity-participating-org'],
                            self.iati['activity/' + self.id + '/participating-org/' + str(ref)]))
            
            self.graph.add((self.iati['activity/' + self.id + '/participating-org/' + str(ref)],
                            RDF.type,
                            self.iati['organisation']))
            
            self.graph.add((self.iati['activity/' + self.id + '/participating-org/' + str(ref)],
                            self.iati['organisation-code'],
                            self.iati['codelist/OrganisationIdentifier/' + str(ref)]))
        
            if not name == None:
                self.graph.add((self.iati['activity/' + self.id + '/participating-org/' + str(ref)],
                                RDFS.label,
                                name))
                
            if not type == None:
                self.graph.add((self.iati['activity/' + self.id + '/participating-org/' + str(ref)],
                                self.iati['organisation-type'],
                                self.iati['codelist/OrganisationType/' + str(type)]))
                
            if not role == None:
                self.graph.add((self.iati['activity/' + self.id + '/participating-org/' + str(ref)],
                                self.iati['organisation-role'],
                                self.iati['codelist/OrganisationRole/' + str(role)]))
    
    def recipient_country(self, xml):
        '''Converts the XML of the recipient-country element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        # Keys
        code = self.__attribute_key(xml, 'code')
        percentage = self.__attribute_key(xml, 'percentage')
        
        # Text
        country_name = self.__attribute_text(xml, self.default_language)
        
        if not code == None:
            self.graph.add((self.iati['activity/' + self.id],
                            self.iati['activity-recipient-country'],
                            self.iati['activity/' + self.id + '/recipient-country/' + str(code)]))
            
            self.graph.add((self.iati['activity/' + self.id + '/recipient-country/' + str(code)],
                            RDF.type,
                            self.iati['country']))
            
            self.graph.add((self.iati['activity/' + self.id + '/recipient-country/' + str(code)],
                            self.iati['country-code'],
                            self.iati['codelist/Country/' + str(code)]))
        
            if not country_name == None:
                self.graph.add((self.iati['activity/' + self.id + '/recipient-country/' + str(code)],
                                RDFS.label,
                                country_name))
                
            if not percentage == None:
                self.graph.add((self.iati['activity/' + self.id + '/recipient-country/' + str(code)],
                                self.iati['percentage'],
                                Literal(percentage)))
    
    def recipient_region(self, xml):
        '''Converts the XML of the recipient-region element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        # Keys
        code = self.__attribute_key(xml, 'code')
        percentage = self.__attribute_key(xml, 'percentage')
        
        # Text
        region_name = self.__attribute_text(xml, self.default_language)
        
        if not code == None:
            self.graph.add((self.iati['activity/' + self.id],
                            self.iati['activity-recipient-region'],
                            self.iati['activity/' + self.id + '/recipient-region/' + str(code)]))
            
            self.graph.add((self.iati['activity/' + self.id + '/recipient-region/' + str(code)],
                            RDF.type,
                            self.iati['region']))
            
            self.graph.add((self.iati['activity/' + self.id + '/recipient-region/' + str(code)],
                            self.iati['region-code'],
                            self.iati['codelist/Region/' + str(code)]))
        
            if not region_name == None:
                self.graph.add((self.iati['activity/' + self.id + '/recipient-region/' + str(code)],
                                RDFS.label,
                                region_name))
                
            if not percentage == None:
                self.graph.add((self.iati['activity/' + self.id + '/recipient-region/' + str(code)],
                                self.iati['percentage'],
                                Literal(percentage)))
    
    def location(self, xml):
        '''Converts the XML of the location element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        # Keys
        percentage = self.__attribute_key(xml, 'percentage')
        
        # Elements
        name = xml.find('name')
        descriptions = xml.findall('description')
        location_type = xml.find('location-type')
        administrative = xml.find('administrative')
        coordinates = xml.find('coordinates')
        gazetteer_entry = xml.find('gazetteer-entry')
        
        # Progress
        self.__update_progress('location')
        
        self.graph.add((self.iati['activity/' + self.id],
                        self.iati['activity-location'],
                        self.iati['activity/' + self.id + '/location' + str(self.progress['location'])]))
        
        self.graph.add((self.iati['activity/' + self.id + '/location' + str(self.progress['location'])],
                        RDF.type,
                        self.iati['location']))
        
        if not name == None:
            # Text
            name_text = self.__attribute_text(name, self.default_language)
            
            self.graph.add((self.iati['activity/' + self.id + '/location' + str(self.progress['location'])],
                            RDFS.label,
                            name_text))
        
        if not descriptions == []:
            description_counter = 1
            
            for description in descriptions:
                # Keys
                type = self.__attribute_key(description, 'type')
                
                # Text
                description_text = self.__attribute_text(description, self.default_language)
                
                if not description_text == None:
                    self.graph.add((self.iati['activity/' + self.id + '/location' + str(self.progress['location'])],
                                    self.iati['location-description'],
                                    self.iati['activity/' + self.id + '/location' + str(self.progress['location']) + 
                                              '/description' + str(description_counter)]))
                    
                    self.graph.add((self.iati['activity/' + self.id + '/location' + str(self.progress['location']) + 
                                    '/description' + str(description_counter)],
                                    RDF.type,
                                    self.iati['description']))
                    
                    self.graph.add((self.iati['activity/' + self.id + '/location' + str(self.progress['location']) + 
                                              '/description' + str(description_counter)],
                                    self.iati['description'],
                                    description_text))
                    
                    if not type == None:
                        self.graph.add((self.iati['activity/' + self.id + '/location' + str(self.progress['location']) + 
                                                  '/description' + str(description_counter)],
                                        self.iati['description-type'],
                                        self.iati['codelist/DescriptionType/' + str(type)]))  
                    
                    description_counter += 1
        
        if not location_type == None:
            # Keys
            location_type_code = self.__attribute_key(location_type, 'code')
            
            if not location_type_code == None:
                self.graph.add((self.iati['activity/' + self.id + '/location' + str(self.progress['location'])],
                                self.iati['location-type'],
                                self.iati['codelist/LocationType/' + str(location_type_code)]))
        
        if not administrative == None:
            # Keys
            administrative_country = self.__attribute_key(administrative, 'country')
            
            # Text
            administrative_text = self.__attribute_text(administrative, self.default_language)
            
            self.graph.add((self.iati['activity/' + self.id + '/location' + str(self.progress['location'])],
                            self.iati['location-administrative'],
                            self.iati['activity/' + self.id + '/location' + str(self.progress['location']) +
                                      '/administrative']))
            
            if not administrative_country == None:
                self.graph.add((self.iati['activity/' + self.id + '/location' + str(self.progress['location']) +
                                          '/administrative'],
                                self.iati['administrative-country'],
                                self.iati['codelist/Country/' + str(administrative_country)]))
                
            if not administrative_text == None:
                self.graph.add((self.iati['activity/' + self.id + '/location' + str(self.progress['location']) +
                                          '/administrative'],
                                RDFS.label,
                                administrative_text))
        
        if not coordinates == None:
            # Keys
            latitude = self.__attribute_key(coordinates, 'latitude')
            longitude = self.__attribute_key(coordinates, 'longitude')
            precision = self.__attribute_key(coordinates, 'precision')
            
            self.graph.add((self.iati['activity/' + self.id + '/location' + str(self.progress['location'])],
                            self.iati['location-coordinates'],
                            self.iati['activity/' + self.id + '/location' + str(self.progress['location']) + '/coordinates']))
            
            if not latitude == None:
                self.graph.add((self.iati['activity/' + self.id + '/location' + str(self.progress['location']) + 
                                          '/coordinates'],
                                self.iati['latitude'],
                                Literal(latitude)))
    
            if not longitude == None:
                self.graph.add((self.iati['activity/' + self.id + '/location' + str(self.progress['location']) + 
                                          '/coordinates'],
                                self.iati['longitude'],
                                Literal(longitude)))
            
            if not precision == None:
                self.graph.add((self.iati['activity/' + self.id + '/location' + str(self.progress['location']) + 
                                          '/coordinates'],
                                self.iati['precision'],
                                self.iati['codelist/GeographicalPrecision/' + str(precision)]))
        
        if not gazetteer_entry == None:
            # Keys
            gazetteer_ref = self.__attribute_key(gazetteer_entry, 'gazetteer-ref')
            
            # Text
            gazetteer_entry_text = gazetteer_entry.text
            gazetteer_entry_text = " ".join(gazetteer_entry_text.split())
            
            if not gazetteer_ref == None:
                if not gazetteer_entry_text == None:
                
                    self.graph.add((self.iati['activity/' + self.id + '/location' + str(self.progress['location'])],
                                    self.iati['location-gazetteer-entry'],
                                    self.iati['gazetteer/' + str(gazetteer_ref) + str('/') + str(gazetteer_entry_text)]))
     
    def sector(self, xml):
        '''Converts the XML of the sector element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        # Keys
        code = self.__attribute_key(xml, 'code')
        vocabulary = self.__attribute_key(xml, 'vocabulary')
        percentage = self.__attribute_key(xml, 'percentage')
        
        # Text
        name = self.__attribute_text(xml, self.default_language)
        
        if not code == None:
            if not vocabulary == None:
                
                self.graph.add((self.iati['activity/' + self.id],
                                self.iati['activity-sector'],
                                self.iati['activity/' + self.id + '/sector/' + str(vocabulary) +
                                          '/' + str(code)]))
                
                self.graph.add((self.iati['activity/' + self.id + '/sector/' + str(vocabulary) +
                                          '/' + str(code)],
                                RDF.type,
                                self.iati['sector']))
                
                self.graph.add((self.iati['activity/' + self.id + '/sector/' + str(vocabulary) +
                                          '/' + str(code)],
                                self.iati['sector-code'],
                                self.iati['codelist/Sector/' + str(vocabulary) + '/' + str(code)]))
                
                if not percentage == None:
                    self.graph.add((self.iati['activity/' + self.id + '/sector/' + str(vocabulary) +
                                              '/' + str(code)],
                                    self.iati['percentage'],
                                    Literal(percentage)))
                    
                if not name == None:
                    self.graph.add((self.iati['activity/' + self.id + '/sector/' + str(vocabulary) +
                                              '/' + str(code)],
                                    RDFS.label,
                                    name))
    
    def policy_marker(self, xml):
        '''Converts the XML of the policy-marker element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        # Keys
        code = self.__attribute_key(xml, 'code')
        vocabulary = self.__attribute_key(xml, 'vocabulary')
        significance = self.__attribute_key(xml, 'significance')
        
        # Text
        name = self.__attribute_text(xml, self.default_language)
        
        if not code == None:
            if not vocabulary == None:
                
                self.graph.add((self.iati['activity/' + self.id],
                                self.iati['activity-policy-marker'],
                                self.iati['activity/' + self.id + '/policy-marker/' + str(vocabulary) +
                                          '/' + str(code)]))
                
                self.graph.add((self.iati['activity/' + self.id + '/policy-marker/' + str(vocabulary) +
                                          '/' + str(code)],
                                RDF.type,
                                self.iati['policy-marker']))
                
                self.graph.add((self.iati['activity/' + self.id + '/policy-marker/' + str(vocabulary) +
                                          '/' + str(code)],
                                self.iati['policy-marker-code'],
                                self.iati['codelist/PolicyMarker/' + str(vocabulary) + '/' + str(code)]))
                
                if not significance == None:
                    self.graph.add((self.iati['activity/' + self.id + '/policy-marker/' + str(vocabulary) +
                                              '/' + str(code)],
                                    self.iati['significance-code'],
                                    self.iati['codelist/PolicySignificance/' + str(significance)]))
                    
                if not name == None:
                    self.graph.add((self.iati['activity/' + self.id + '/policy-marker/' + str(vocabulary) +
                                              '/' + str(code)],
                                    RDFS.label,
                                    name))
    
    def collaboration_type(self, xml):
        '''Converts the XML of the collaboration-type element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        # Keys
        code = self.__attribute_key(xml, 'code')
        
        if not code == None:
            self.graph.add((self.iati['activity/' + self.id],
                            self.iati['activity-collaboration-type'],
                            self.iati['codelist/CollaborationType/' + str(code)]))
    
    def finance_type(self, xml):
        '''Converts the XML of the default-finance-type element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        # Keys
        code = self.__attribute_key(xml, 'code')
        
        if not code == None:
            self.graph.add((self.iati['activity/' + self.id],
                            self.iati['activity-default-finance-type'],
                            self.iati['codelist/FinanceType/' + str(code)]))
        
        return self.graph
    
    def flow_type(self, xml):
        '''Converts the XML of the default-flow-type element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        # Keys
        code = self.__attribute_key(xml, 'code')
        
        if not code == None:
            self.graph.add((self.iati['activity/' + self.id],
                            self.iati['activity-default-flow-type'],
                            self.iati['codelist/FlowType/' + str(code)]))
    
    def aid_type(self, xml):
        '''Converts the XML of the default-aid-type element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        # Keys
        code = self.__attribute_key(xml, 'code')
        
        if not code == None:
            self.graph.add((self.iati['activity/' + self.id],
                            self.iati['activity-default-aid-type'],
                            self.iati['codelist/AidType/' + str(code)]))
    
    def tied_status(self, xml):
        '''Converts the XML of the default-tied-status element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        # Keys
        code = self.__attribute_key(xml, 'code')
        
        if not code == None:
            self.graph.add((self.iati['activity/' + self.id],
                            self.iati['activity-default-tied-status'],
                            self.iati['codelist/TiedStatus/' + str(code)]))
    
    def budget(self, xml):
        '''Converts the XML of the budget element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        # Keys
        type = self.__attribute_key(xml, 'type')
        
        # Elements
        period_start = xml.find('period-start')
        period_end = xml.find('period-end')
        value = xml.find('value')
        
        # Progress
        self.__update_progress('budget')
        
        self.graph.add((self.iati['activity/' + self.id],
                        self.iati['activity-budget'],
                        self.iati['activity/' + self.id + '/budget' + str(self.progress['budget'])]))
        
        self.graph.add((self.iati['activity/' + self.id + '/budget' + str(self.progress['budget'])],
                        RDF.type,
                        self.iati['budget']))
        
        if not type == None:        
            self.graph.add((self.iati['activity/' + self.id + '/budget' + str(self.progress['budget'])],
                            self.iati['budget-type'],
                            self.iati['codelist/BudgetType/' + str(type)]))
        
        if not period_start == None:
            # Keys
            date = self.__attribute_key(period_start, 'iso-date')
            
            # Text
            period_start_text = self.__attribute_text(period_start, self.default_language)
            
            self.graph.add((self.iati['activity/' + self.id + '/budget' + str(self.progress['budget'])],
                            self.iati['budget-period-start'],
                            self.iati['activity/' + self.id + '/budget' + str(self.progress['budget']) + 
                                      '/period-start']))
            
            if not date == None:
                self.graph.add((self.iati['activity/' + self.id + '/budget' + str(self.progress['budget']) + 
                                          '/period-start'],
                                self.iati['date'],
                                Literal(date)))
            
            if not period_start_text == None:
                self.graph.add((self.iati['activity/' + self.id + '/budget' + str(self.progress['budget']) + 
                                          '/period-start'],
                           RDFS.label,
                           period_start_text))
        
        if not period_end == None:
            # Keys
            date = self.__attribute_key(period_end, 'iso-date')
            
            # Text
            period_end_text = self.__attribute_text(period_end, self.default_language)
            
            self.graph.add((self.iati['activity/' + self.id + '/budget' + str(self.progress['budget'])],
                            self.iati['budget-period-end'],
                            self.iati['activity/' + self.id + '/budget' + str(self.progress['budget']) + 
                                      '/period-end']))
            
            if not date == None:
                self.graph.add((self.iati['activity/' + self.id + '/budget' + str(self.progress['budget']) + 
                                          '/period-end'],
                           self.iati['date'],
                           Literal(date)))
            
            if not period_end_text == None:
                self.graph.add((self.iati['activity/' + self.id + '/budget' + str(self.progress['budget']) + 
                                          '/period-end'],
                           RDFS.label,
                           period_end_text))
        
        if not value == None:
            # Keys
            currency = self.__attribute_key(value, 'currency')
            value_date = self.__attribute_key(value, 'value-date')
            
            # Text
            value_text = value.text
            value_text = " ".join(value_text.split())
            
            if not value_text == None:
                self.graph.add((self.iati['activity/' + self.id + '/budget' + str(self.progress['budget'])],
                                self.iati['budget-value'],
                                self.iati['activity/' + self.id + '/budget' + str(self.progress['budget']) + '/value']))
                
                self.graph.add((self.iati['activity/' + self.id + '/budget' + str(self.progress['budget']) + '/value'],
                                RDF.type,
                                self.iati['value']))
                
                self.graph.add((self.iati['activity/' + self.id + '/budget' + str(self.progress['budget']) + '/value'],
                                self.iati['value'],
                                Literal(value_text)))
                
                if not currency == None:
                    self.graph.add((self.iati['activity/' + self.id + '/budget' + str(self.progress['budget']) + '/value'],
                                    self.iati['currency'],
                                    self.iati['codelist/Currency/' + str(currency)]))
                
                elif not self.default_currency == None:
                    self.graph.add((self.iati['activity/' + self.id + '/budget' + str(self.progress['budget']) + '/value'],
                                    self.iati['currency'],
                                    self.iati['codelist/Currency/' + str(self.default_currency)]))
                
                if not value_date == None:
                    self.graph.add((self.iati['activity/' + self.id + '/budget' + str(self.progress['budget']) + '/value'],
                                    self.iati['value-date'],
                                    Literal(value_date)))
    
    def planned_disbursement(self, xml):
        '''Converts the XML of the planned-disbursement element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        # Keys
        updated = self.__attribute_key(xml, 'updated')
        
        # Elements
        period_start = xml.find('period-start')
        period_end = xml.find('period-end')
        value = xml.find('value')
        
        # Progress
        self.__update_progress('planned_disbursement')
        
        self.graph.add((self.iati['activity/' + self.id],
                        self.iati['activity-planned-disbursement'],
                        self.iati['activity/' + self.id + '/planned-disbursement' + 
                                  str(self.progress['planned_disbursement'])]))
        
        self.graph.add((self.iati['activity/' + self.id + '/planned-disbursement' + 
                                  str(self.progress['planned_disbursement'])],
                        RDF.type,
                        self.iati['planned-disbursement']))
        
        if not updated == None:        
            self.graph.add((self.iati['activity/' + self.id + '/planned-disbursement' + 
                                      str(self.progress['planned_disbursement'])],
                            self.iati['updated'],
                            Literal(updated)))
        
        if not period_start == None:
            # Keys
            date = self.__attribute_key(period_start, 'iso-date')
            
            # Text
            period_start_text = self.__attribute_text(period_start, defaults['language'])
            
            self.graph.add((self.iati['activity/' + self.id + '/planned-disbursement' + 
                                      str(self.progress['planned_disbursement'])],
                            self.iati['planned-disbursement-period-start'],
                            self.iati['activity/' + self.id + '/planned-disbursement' + 
                                      str(self.progress['planned_disbursement']) + '/period-start']))
            
            if not date == None:
                self.graph.add((self.iati['activity/' + self.id + '/planned-disbursement' + 
                                          str(self.progress['planned_disbursement']) + '/period-start'],
                                self.iati['date'],
                                Literal(date)))
            
            if not period_start_text == None:
                self.graph.add((self.iati['activity/' + self.id + '/planned-disbursement' + 
                                          str(self.progress['planned_disbursement']) + '/period-start'],
                                RDFS.label,
                                period_start_text))
        
        if not period_end == None:
            # Keys
            date = self.__attribute_key(period_end, 'iso-date')
            
            # Text
            period_end_text = self.__attribute_text(period_end, defaults['language'])
            
            self.graph.add((self.iati['activity/' + self.id + '/planned-disbursement' + 
                                      str(self.progress['planned_disbursement'])],
                            self.iati['planned-disbursement-period-end'],
                            self.iati['activity/' + self.id + '/planned-disbursement' + 
                                      str(self.progress['planned_disbursement']) + '/period-end']))
            
            if not date == None:
                self.graph.add((self.iati['activity/' + self.id + '/planned-disbursement' + 
                                str(self.progress['planned_disbursement']) + '/period-end'],
                                self.iati['date'],
                                Literal(date)))
            
            if not period_end_text == None:
                self.graph.add((self.iati['activity/' + self.id + '/planned-disbursement' + 
                                          str(self.progress['planned_disbursement']) + '/period-end'],
                                RDFS.label,
                                period_end_text))
        
        if not value == None:
            # Keys
            currency = self.__attribute_key(value, 'currency')
            value_date = self.__attribute_key(value, 'value-date')
            
            # Text
            value_text = value.text
            value_text = " ".join(value_text.split())
            
            if not value_text == None:
                self.graph.add((self.iati['activity/' + self.id + '/planned-disbursement' + 
                                          str(self.progress['planned_disbursement'])],
                                self.iati['planned-disbursement-value'],
                                self.iati['activity/' + self.id + '/planned-disbursement' + 
                                          str(self.progress['planned_disbursement']) + '/value']))
                
                self.graph.add((self.iati['activity/' + self.id + '/planned-disbursement' + 
                                          str(self.progress['planned_disbursement']) + '/value'],
                                RDF.type,
                                self.iati['value']))
                
                self.graph.add((self.iati['activity/' + self.id + '/planned-disbursement' + 
                                          str(self.progress['planned_disbursement']) + '/value'],
                                self.iati['value'],
                                Literal(value_text)))
                
                if not currency == None:
                    self.graph.add((self.iati['activity/' + self.id + '/planned-disbursement' + 
                                              str(self.progress['planned_disbursement']) + '/value'],
                                    self.iati['currency'],
                                    self.iati['codelist/Currency/' + str(currency)]))
                
                elif not defaults['currency'] == None:
                    self.graph.add((self.iati['activity/' + self.id + '/planned-disbursement' + 
                                              str(self.progress['planned_disbursement']) + '/value'],
                                    self.iati['currency'],
                                    self.iati['codelist/Currency/' + str(defaults['currency'])]))
                
                if not value_date == None:
                    self.graph.add((self.iati['activity/' + self.id + '/planned-disbursement' + 
                                              str(self.progress['planned_disbursement']) + '/value'],
                                    self.iati['value-date'],
                                    Literal(value_date)))
    
    def transaction(self, xml):
        '''Converts the XML of the transaction element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        # Keys
        ref = self.__attribute_key(xml, 'ref')
        
        # Elements
        aid_type = xml.find('aid-type')
        descriptions = xml.findall('description')
        disbursement_channel = xml.find('disbursement-channel')
        finance_type = xml.find('finance-type')
        flow_type = xml.find('flow-type')
        provider_org = xml.find('provider-org')
        receiver_org = xml.find('receiver-org')
        tied_status = xml.find('tied-status')
        transaction_date = xml.find('transaction-date')
        transaction_type = xml.find('transaction-type')
        value = xml.find('value')
        
        # Progress
        self.__update_progress('transaction')
        
        if not ref == None:
            transaction_id = self.iati['activity/' + self.id + '/transaction/' + str(ref)]
        else:
            transaction_id = self.iati['activity/' + self.id + '/transaction' + 
                                       str(self.progress['transaction'])]
            
        self.graph.add((self.iati['activity/' + self.id],
                        self.iati['activity-transaction'],
                        transaction_id))        
        
        self.graph.add((transaction_id,
                        RDF.type,
                        self.iati['transaction']))
        
        if not aid_type == None:
            # Keys
            code = self.__attribute_key(aid_type, 'code')
            
            if not code == None:
                self.graph.add((transaction_id,
                                self.iati['aid-type'],
                                self.iati['codelist/AidType/' + str(code)]))
                
            elif not self.default_aid_type == None:
                self.graph.add((transaction_id,
                                self.iati['aid-type'],
                                self.iati['codelist/AidType/' + str(self.default_aid_type)]))
            
        elif not self.default_aid_type == None:
            self.graph.add((transaction_id,
                            self.iati['aid-type'],
                            self.iati['codelist/AidType/' + str(self.default_aid_type)]))
            
        if not descriptions == []:
            description_counter = 1
            
            for description in descriptions:
                # Keys
                type = self.__attribute_key(description, 'type')
                
                # Text
                description_text = self.__attribute_text(description, self.default_language)
                
                if not description_text == None:
                    self.graph.add((transaction_id,
                                    self.iati['transaction-description'],
                                    URIRef(transaction_id + '/description' + str(description_counter))))
                    
                    self.graph.add((URIRef(transaction_id + '/description' + str(description_counter)),
                                    RDF.type,
                                    self.iati['description']))
                    
                    self.graph.add((URIRef(transaction_id + '/description' + str(description_counter)),
                                    self.iati['description'],
                                    description_text))
                    
                    if not type == None:
                        self.graph.add((URIRef(transaction_id + '/description' + str(description_counter)),
                                        self.iati['description-type'],
                                        self.iati['codelist/DescriptionType/' + str(type)]))  
                    
                    description_counter += 1
        
        if not disbursement_channel == None:
            # Keys
            code = self.__attribute_key(disbursement_channel, 'code')
            
            self.graph.add((transaction_id,
                            self.iati['disbursement-channel'],
                            self.iati['codelist/disbursementChannel/' + str(code)]))
        
        if not finance_type == None:
            # Keys
            code = self.__attribute_key(finance_type, 'code')
            
            if not code == None:
                self.graph.add((transaction_id,
                                self.iati['finance-type'],
                                self.iati['codelist/FinanceType/' + str(code)]))
                
            elif not self.default_finance_type == None:
                self.graph.add((transaction_id,
                                self.iati['finance-type'],
                                self.iati['codelist/FinanceType/' + str(self.default_finance_type)]))
            
        elif not self.default_finance_type == None:
            self.graph.add((transaction_id,
                            self.iati['finance-type'],
                            self.iati['codelist/FinanceType/' + str(self.default_finance_type)]))
        
        if not flow_type == None:
            # Keys
            code = self.__attribute_key(flow_type, 'code')
            
            if not code == None:
                self.graph.add((transaction_id,
                                self.iati['flow-type'],
                                self.iati['codelist/FlowType/' + str(code)]))
                
            elif not self.default_flow_type == None:
                self.graph.add((transaction_id,
                                self.iati['flow-type'],
                                self.iati['codelist/FlowType/' + str(self.default_flow_type)]))
            
        elif not self.default_flow_type == None:
            self.graph.add((transaction_id,
                            self.iati['flow-type'],
                            self.iati['codelist/FlowType/' + str(self.default_flow_type)]))
        
        if not provider_org == None:
            # Keys
            ref = self.__attribute_key(provider_org, 'ref')
            provider_activity_id = self.__attribute_key(provider_org, 'provider-activity-id')
            
            # Text
            provider_org_text = provider_org.text
            provider_org_text = " ".join(provider_org_text.split())
            
            self.graph.add((transaction_id,
                            self.iati['provider-org'],
                            URIRef(transaction_id + '/provider-org')))        
            
            if not ref == None:
                self.graph.add((URIRef(transaction_id + '/provider-org'),
                                self.iati['organisation-ref'],
                                self.iati['codelist/OrganisationIdentifier/' + str(ref)]))
            
            if not provider_activity_id == None:
                self.graph.add((URIRef(transaction_id + '/provider-org'),
                                self.iati['provider-activity-id'],
                                self.iati['activity/' + str(provider_activity_id)]))
                
        if not receiver_org == None:
            # Keys
            ref = self.__attribute_key(receiver_org, 'ref')
            receiver_activity_id = self.__attribute_key(receiver_org, 'receiver-activity-id')
            
            # Text
            receiver_org_text = receiver_org.text
            receiver_org_text = " ".join(receiver_org_text.split())
            
            self.graph.add((transaction_id,
                            self.iati['receiver-org'],
                            URIRef(transaction_id + '/receiver-org')))        
            
            if not ref == None:
                self.graph.add((URIRef(transaction_id + '/receiver-org'),
                                self.iati['organisation-ref'],
                                self.iati['codelist/OrganisationIdentifier/' + str(ref)]))
            
            if not receiver_activity_id == None:
                self.graph.add((URIRef(transaction_id + '/receiver-org'),
                                self.iati['receiver-activity-id'],
                                self.iati['activity/' + str(receiver_activity_id)]))
    
        if not tied_status == None:
            # Keys
            code = self.__attribute_key(tied_status, 'code')
            
            if not code == None:
                self.graph.add((transaction_id,
                                self.iati['tied-status'],
                                self.iati['codelist/TiedStatus/' + str(code)]))
                
            elif not self.default_tied_status == None:
                self.graph.add((transaction_id,
                                self.iati['tied-status'],
                                self.iati['codelist/TiedStatus/' + str(self.default_tied_status)]))
            
        elif not self.default_tied_status == None:
            self.graph.add((transaction_id,
                            self.iati['tied-status'],
                            self.iati['codelist/TiedStatus/' + str(self.defaults_tied_status)]))
        
        if not transaction_date == None:
            # Keys
            iso_date = self.__attribute_key(transaction_date, 'iso-date')
            
            if not iso_date == None:
                self.graph.add((transaction_id,
                                self.iati['transaction-date'],
                                Literal(iso_date)))
            
        if not transaction_type == None:
            # Keys
            code = self.__attribute_key(transaction_type, 'code')
            
            if not code == None:
                self.graph.add((transaction_id,
                                self.iati['transaction-type'],
                                self.iati['codelist/TransactionType/' + str(code)]))            
                                         
        if not value == None:
            # Keys
            currency = self.__attribute_key(value, 'currency')
            value_date = self.__attribute_key(value, 'value-date')
            
            # Text
            value_text = value.text
            value_text = " ".join(value_text.split())
            
            if not value_text == None:
                self.graph.add((transaction_id,
                                self.iati['transaction-value'],
                                URIRef(transaction_id + '/value')))
                
                self.graph.add((URIRef(transaction_id + '/value'),
                                RDF.type,
                                self.iati['value']))
                
                self.graph.add((URIRef(transaction_id + '/value'),
                                self.iati['value'],
                                Literal(value_text)))
                
                if not currency == None:
                    self.graph.add((URIRef(transaction_id + '/value'),
                                    self.iati['currency'],
                                    self.iati['codelist/Currency/' + str(currency)]))
                
                elif not self.default_currency == None:
                    self.graph.add((URIRef(transaction_id + '/value'),
                                    self.iati['currency'],
                                    self.iati['codelist/Currency/' + str(self.default_currency)]))
                
                if not value_date == None:
                    self.graph.add((URIRef(transaction_id + '/value'),
                                    self.iati['value-date'],
                                    Literal(value_date)))
    
    def document_link(self, xml):
        '''Converts the XML of the document-link element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        # Keys
        url = self.__attribute_key(xml, 'url')
        format = self.__attribute_key(xml, 'format')
        
        # Elements
        titles = xml.findall('title')
        category = xml.find('category')
        languages = xml.findall('language')
        
        # Progress
        self.__update_progress('document_link')
        
        self.graph.add((self.iati['activity/' + self.id],
                        self.iati['activity-document-link'],
                        self.iati['document-link' + str(self.progress['document_link'])]))
        
        self.graph.add((self.iati['document-link' + str(self.progress['document_link'])],
                        RDF.type,
                        self.iati['document-link']))    
        
        if not url == None:
            self.graph.add((self.iati['document-link' + str(self.progress['document_link'])],
                            self.iati['url'],
                            URIRef(url)))
        
        if not format == None:
            self.graph.add((self.iati['document-link' + str(self.progress['document_link'])],
                            self.iati['format'],
                            self.iati['codelist/FileFormat/' + str(format)]))
            
        if not titles == []:
            for title in titles:
                # Text
                name = self.__attribute_text(title, self.default_language)
                
                self.graph.add((self.iati['document-link' + str(self.progress['document_link'])],
                                RDFS.label,
                                name))
                
        if not category == None:
            # Keys
            code = self.__attribute_key(category, 'code')
            
            self.graph.add((self.iati['document-link' + str(self.progress['document_link'])],
                            self.iati['document-category'],
                            self.iati['codelist/DocumentCategory/' + str(code)]))
        
        if not languages == []:
            for language in languages:
                # Keys
                code = self.__attribute_key(language, 'code')
                
                # Text
                name = self.__attribute_text(language, self.default_language)
                
                if not code == None:
                    self.graph.add((self.iati['document-link' + str(self.progress['document_link'])],
                                    self.iati['language'],
                                    self.iati['document-link' + str(self.progress['document_link']) + 
                                              '/language/' + str(code)]))
                    
                    if not name == None:
                        self.graph.add((self.iati['document-link' + str(self.progress['document_link']) + 
                                                  '/language/' + str(code)],
                                        RDFS.label,
                                        name))
    
    def related_activity(self, xml):
        '''Converts the XML of the related-activity element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        self.iati = defaults['namespace']
        
        # Keys
        ref = self.__attribute_key(xml, 'ref')
        type = self.__attribute_key(xml, 'type')
        
        # Text
        name = self.__attribute_text(xml, defaults['language'])
        
        if not ref == None:
            self.graph.add((self.iati['activity/' + self.id],
                            self.iati['related-activity'],
                            self.iati['activity/' + self.id + '/related-activity/' + str(ref)]))
            
            self.graph.add((self.iati['activity/' + self.id + '/related-activity/' + str(ref)],
                            self.iati['activity-id'],
                            self.iati['activity/' + str(ref)]))
            
            if not type == None:
                self.graph.add((self.iati['activity/' + self.id + '/related-activity/' + str(ref)],
                                self.iati['related-activity-type'],
                                self.iati['codelist/RelatedActivityType/' + str(type)]))
        
            if not name == None:
                self.graph.add((self.iati['activity/' + self.id + '/related-activity/' + str(ref)],
                                RDFS.label,
                                name))
    
    def conditions(self, xml):
        '''Converts the XML of the conditions element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        # Elements
        conditions = xml.findall('condition')
        
        if not conditions == []:
            condition_counter = 1
            
            for condition in conditions:
                # Keys
                type = self.__attribute_key(condition, 'type')
                
                # Text
                condition_text = self.__attribute_text(condition, defaults['language'])
                
                if not condition_text == None:
                       self.graph.add((self.iati['activity/' + self.id],
                                       self.iati['activity-condition'],
                                       self.iati['activity/' + self.id + '/condition' + str(condition_counter)]))
                       
                       self.graph.add((self.iati['activity/' + self.id + '/condition' + str(condition_counter)],
                                       RDF.type,
                                       self.iati['condition']))
                       
                       if not type == None:
                           self.graph.add((self.iati['activity/' + self.id + '/condition' + str(condition_counter)],
                                           self.iati['condition-type'],
                                           self.iati['codelist/ConditionType/' + str(type)]))                                          
            
                condition_counter += 1
    
    def result(self, xml):
        '''Converts the XML of the conditions element to a RDFLib self.graph.
        
        Parameters
        @xml: The XML of this element.'''
        
        # Keys
        type = self.__attribute_key(xml, 'type')
        aggregation_status = self.__attribute_key(xml, 'aggregation-status')
        
        # Elements
        titles = xml.findall('title')
        descriptions = xml.findall('description')
        indicators = xml.findall('indicator')
        
        # Progress
        self.__update_progress('result')
        
        self.graph.add((self.iati['activity/' + self.id],
                        self.iati['activity-result'],
                        self.iati['activity/' + self.id + '/result' + str(self.progress['result'])]))
        
        self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result'])],
                        RDF.type,
                        self.iati['result']))    
        
        if not titles == []:
            for title in titles:
                # Text
                title_text = self.__attribute_text(title, defaults['language'])
                
                if not title_text == None:
                    self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result'])],
                                    RDFS.label,
                                    title_text))
        
        if not descriptions == []:
            description_counter = 1
            
            for description in descriptions:
                # Keys
                type = self.__attribute_key(description, 'type')
                
                # Text
                description_text = self.__attribute_text(description, defaults['language'])
                
                if not description_text == None:
                    self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result'])],
                                    self.iati['result-description'],
                                    self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                              '/description' + str(description_counter)]))
                    
                    self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                              '/description' + str(description_counter)],
                                    RDF.type,
                                    self.iati['description']))
                    
                    self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                              '/description' + str(description_counter)],
                                    self.iati['description'],
                                    description_text))
                    
                    if not type == None:
                        self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                                  '/description' + str(description_counter)],
                                        self.iati['description-type'],
                                        self.iati['codelist/DescriptionType/' + str(type)]))                                   
                
                description_counter += 1
            
        if not indicators == []:
            indicator_counter = 1
            
            for indicator in indicators:
                # Keys
                measure = self.__attribute_key(description, 'measure')
                ascending = self.__attribute_key(description, 'ascending')
                
                # Elements
                titles = indicator.findall('title')
                descriptions = indicator.findall('description')
                periods = indicator.findall('indicator')
                baseline = indicator.find('baseline')
                
                self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result'])],
                                self.iati['result-indicator'],
                                self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                          '/indicator' + str(indicator_counter)]))
                
                self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                          '/indicator' + str(indicator_counter)],
                                RDF.type,
                                self.iati['indicator']))
                
                if not measure == None:
                    self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                              '/indicator' + str(indicator_counter)],
                                    self.iati['indicator-measure'],
                                    self.iati['codelist/IndicatorMeasure/' + str(measure)]))
                
                if not ascending == None:
                    self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                              '/indicator' + str(indicator_counter)],
                                    self.iati['indicator-ascending'],
                                    Literal(ascending)))
    
                if not titles == []:
                    for title in titles:
                        # Text
                        title_text = self.__attribute_text(title, defaults['language'])
                        
                        if not title_text == None:
                            self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                                      '/indicator' + str(indicator_counter)],
                                            RDFS.label,
                                            title_text))
    
                if not descriptions == []:
                    description_counter = 1
                    
                    for description in descriptions:
                        # Keys
                        type = self.__attribute_key(description, 'type')
                        
                        # Text
                        description_text = self.__attribute_text(description, defaults['language'])
                        
                        if not description_text == None:
                            self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                                      '/indicator' + str(indicator_counter)],
                                            self.iati['indicator-description'],
                                            self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                                      '/indicator' + str(indicator_counter) + '/description' + 
                                                      str(description_counter)]))
                            
                            self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                                      '/indicator' + str(indicator_counter) + '/description' + 
                                                      str(description_counter)],
                                            RDF.type,
                                            self.iati['description']))
                            
                            self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                                      '/indicator' + str(indicator_counter) + '/description' + 
                                                      str(description_counter)],
                                            self.iati['description'],
                                            description_text))
                            
                            if not type == None:
                                self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                                          '/indicator' + str(indicator_counter) + '/description' + 
                                                          str(description_counter)],
                                                self.iati['description-type'],
                                                self.iati['codelist/DescriptionType/' + str(type)]))                                   
                        
                        description_counter += 1
                
                if not periods == []:
                    period_counter = 1
                    
                    for period in periods:
                        # Elements
                        period_start = period.find('period-start')
                        period_end = period.find('period-end')
                        target = period.find('target')
                        actual = period.find('actual')
                        
                        if not period_start == None:
                            # Keys
                            date = self.__attribute_key(period_start, 'iso-date')
                            
                            # Text
                            period_start_text = self.__attribute_text(period_start, defaults['language'])
                            
                            self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                                      '/indicator' + str(indicator_counter)],
                                            self.iati['indicator-period-start'],
                                            self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                                      '/indicator' + str(indicator_counter) + '/period-start']))
                            
                            if not date == None:
                                self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                                          '/indicator' + str(indicator_counter) + '/period-start'],
                                                self.iati['date'],
                                                Literal(date)))
                            
                            if not period_start_text == None:
                                self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                                          '/indicator' + str(indicator_counter) + '/period-start'],
                                                RDFS.label,
                                                period_start_text))
                            
                        if not period_end == None:
                            # Keys
                            date = self.__attribute_key(period_end, 'iso-date')
                            
                            # Text
                            period_end_text = self.__attribute_text(period_end, defaults['language'])
                            
                            self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                                      '/indicator' + str(indicator_counter)],
                                            self.iati['indicator-period-end'],
                                            self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                                      '/indicator' + str(indicator_counter) + '/period-end']))
                            
                            if not date == None:
                                self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                                          '/indicator' + str(indicator_counter) + '/period-end'],
                                                self.iati['date'],
                                                Literal(date)))
                            
                            if not period_end_text == None:
                                self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                                          '/indicator' + str(indicator_counter) + '/period-end'],
                                                RDFS.label,
                                                period_end_text))
                        
                        if not target == None:
                            # Keys
                            value = self.__attribute_key(target, 'value')
                            
                            if not value == None:
                                self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                                          '/indicator' + str(indicator_counter)],
                                                self.iati['indicator-target'],
                                                Literal(value)))
                            
                        if not actual == None:
                            # Keys
                            value = self.__attribute_key(actual, 'value')
                            
                            if not value == None:
                                self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                                          '/indicator' + str(indicator_counter)],
                                                self.iati['indicator-actual'],
                                                Literal(value)))                    
                            
                        period_counter += 1
                        
                    if not baseline == None:
                        # Keys
                        year = self.__attribute_key(baseline, 'year')
                        value = self.__attribute_key(baseline, 'value')
                        
                        # Elements
                        comment = baseline.find('comment')
                        
                        self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                                  '/indicator' + str(indicator_counter)],
                                        self.iati['indicator-baseline'],
                                        self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                                  '/indicator' + str(indicator_counter) + '/baseline']))                       
                        
                        if not value == None:
                            self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                                      '/indicator' + str(indicator_counter) + '/baseline'],
                                            self.iati['value'],
                                            Literal(value)))
                            
                        if not year == None:
                            self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                                      '/indicator' + str(indicator_counter) + '/baseline'],
                                            self.iati['year'],
                                            Literal(year)))
                        
                        if not comment == None:
                            # Text
                            comment_text = self.__attribute_text(comment, defaults['language'])
                            
                            self.graph.add((self.iati['activity/' + self.id + '/result' + str(self.progress['result']) + 
                                                      '/indicator' + str(indicator_counter) + '/baseline'],
                                            RDFS.comment,
                                            comment_text))                        
                
                indicator_counter += 1