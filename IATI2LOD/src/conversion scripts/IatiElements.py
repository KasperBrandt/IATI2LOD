## IatiElements.py
## By Kasper Brandt
## Last updated on 08-04-2013

from rdflib import RDF, RDFS, Literal, URIRef

def __attribute_key(xml, key):
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

def __attribute_text(xml, language):
    '''Checks whether an element has a text and picks the correct language.
    
    Parameters
    @xml: An ElemenTree of the element.
    @language: The default language of the activity.
    
    Returns
    @literal: A RDFLib Literal or None.'''
    
    if xml.text == None:
        return None
    
    node_language = __attribute_key(xml, "{http://www.w3.org/XML/1998/namespace}lang")
    
    text = xml.text
    formatted_text = " ".join(text.split())
    
    if not node_language == None:
        return Literal(formatted_text, lang=node_language)
    
    if not language == None:
        return Literal(formatted_text, lang=language)
    
    return Literal(formatted_text)
    
    

def reporting_org(graph, xml, defaults, progress):
    '''Converts the XML of the reporting-org element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Keys
    ref = __attribute_key(xml, 'ref')
    type = __attribute_key(xml, 'type')
    
    # Text
    name = __attribute_text(xml, defaults['language'])
    
    if not ref == None:
        graph.add((iati['activity/' + str(defaults['id'])],
                   iati['activity-reporting-org'],
                   iati['activity/' + str(defaults['id']) + '/activity-reporting-org/' + str(ref)]))
        
        graph.add((iati['activity/' + str(defaults['id']) + '/activity-reporting-org/' + str(ref)],
                   RDF.type,
                   iati['organisation']))
        
        graph.add((iati['activity/' + str(defaults['id']) + '/activity-reporting-org/' + str(ref)],
                   iati['organisation-code'],
                   iati['codelist/OrganisationIdentifier/' + str(ref)]))
    
        if not name == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/activity-reporting-org/' + str(ref)],
                       RDFS.label,
                       name))
            
        if not type == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/activity-reporting-org/' + str(ref)],
                       iati['organisation-type'],
                       iati['codelist/OrganisationType/' + str(type)]))
               
    return graph

def iati_identifier(graph, xml, defaults, progress):
    '''Converts the XML of the iati-identifier element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Text
    id = xml.text
    id = " ".join(id.split())
    
    if not id == None:
        graph.add((iati['activity/' + str(defaults['id'])],
                   iati['activity-id'],
                   Literal(id)))         
    
    return graph

def other_identifier(graph, xml, defaults, progress):
    '''Converts the XML of the other-identifier element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Keys
    owner_ref = __attribute_key(xml, 'owner-ref')
    owner_name = __attribute_key(xml, 'owner-name')
    
    # Text
    name = xml.text
    name = " ".join(name.split())
    
    if not name == None:
        graph.add((iati['activity/' + str(defaults['id'])],
                   iati['activity-other-identifier'],
                   iati['activity/' + str(defaults['id']) + '/other-identifier' + str(name)]))
        
        if not owner_ref == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/other-identifier' + str(name)],
                       iati['activity-other-identifier-owner-ref'],
                       iati['organisation/' + str(owner_ref)]))
        
        if not owner_name == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/other-identifier' + str(name)],
                       iati['activity-other-identifier-owner-name'],
                       Literal(owner_name)))
    return graph

def activity_website(graph, xml, defaults, progress):
    '''Converts the XML of the activity-website element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Text
    website = xml.text
    website = " ".join(website.split())
    
    if not website == None:
        graph.add((iati['activity/' + str(defaults['id'])],
                   iati['activity-website'],
                   Literal(website)))
    
    return graph

def title(graph, xml, defaults, progress):
    '''Converts the XML of the title element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Text
    title = __attribute_text(xml, defaults['language'])
    
    if not title == None:
        graph.add((iati['activity/' + str(defaults['id'])],
                   RDFS.label,
                   title))
    
    return graph

def description(graph, xml, defaults, progress):
    '''Converts the XML of the description element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Keys
    type = __attribute_key(xml, 'type')
    
    # Text
    description = __attribute_text(xml, defaults['language'])
    
    if not description == None:
        graph.add((iati['activity/' + str(defaults['id'])],
                   iati['activity-description'],
                   iati['activity/' + str(defaults['id']) + '/description' + str(progress['description'])]))
        
        graph.add((iati['activity/' + str(defaults['id']) + '/description' + str(progress['description'])],
                   RDF.type,
                   iati['description']))
        
        graph.add((iati['activity/' + str(defaults['id']) + '/description' + str(progress['description'])],
                   iati['description'],
                   description))
        
        if not type == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/description' + str(progress['description'])],
                       iati['description-type'],
                       iati['codelist/DescriptionType/' + str(type)]))            
    
    return graph

def activity_status(graph, xml, defaults, progress):
    '''Converts the XML of the activity-status element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Keys
    code = __attribute_key(xml, 'code')
    
    if not code == None:
        graph.add((iati['activity/' + str(defaults['id'])],
                   iati['activity-status'],
                   iati['codelist/ActivityStatus/' + str(code)]))
    
    return graph

def activity_date(graph, xml, defaults, progress):
    '''Converts the XML of the activity-date element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Keys
    type = __attribute_key(xml, 'type')
    iso_date = __attribute_key(xml, 'iso-date')
    
    # Text
    date = xml.text
    date = " ".join(date.split())
    
    if not iso_date == None:
        date = iso_date
    
    if not date == None:
        if type == "start-actual":
            graph.add((iati['activity/' + str(defaults['id'])],
                       iati['activity-actual-start-date'],
                       Literal(date)))
            
        elif type == "end-actual":
            graph.add((iati['activity/' + str(defaults['id'])],
                       iati['activity-actual-end-date'],
                       Literal(date)))
        
        elif type == "start-planned":
            graph.add((iati['activity/' + str(defaults['id'])],
                       iati['activity-planned-start-date'],
                       Literal(date)))
            
        elif type == "end-planned":
            graph.add((iati['activity/' + str(defaults['id'])],
                       iati['activity-planned-end-date'],
                       Literal(date)))
    
    return graph

def contact_info(graph, xml, defaults, progress):
    '''Converts the XML of the contact-info element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    graph.add((iati['activity/' + str(defaults['id'])],
           iati['activity-contact-info'],
           iati['activity/' + str(defaults['id']) + '/contact-info']))
    
    for element in xml:
        
        info = element.text
        info = " ".join(info.split())
        
        graph.add((iati['activity/' + str(defaults['id']) + '/contact-info'],
           iati[element.tag],
           Literal(info)))
    
    return graph

def participating_org(graph, xml, defaults, progress):
    '''Converts the XML of the participating-org element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Keys
    ref = __attribute_key(xml, 'ref')
    type = __attribute_key(xml, 'type')
    role = __attribute_key(xml, 'role')
    
    # Text
    name = __attribute_text(xml, defaults['language'])
    
    if not ref == None:
        graph.add((iati['activity/' + str(defaults['id'])],
                   iati['activity-participating-org'],
                   iati['activity/' + str(defaults['id']) + '/participating-org/' + str(ref)]))
        
        graph.add((iati['activity/' + str(defaults['id']) + '/participating-org/' + str(ref)],
                   RDF.type,
                   iati['organisation']))
        
        graph.add((iati['activity/' + str(defaults['id']) + '/participating-org/' + str(ref)],
                   iati['organisation-code'],
                   iati['codelist/OrganisationIdentifier/' + str(ref)]))
    
        if not name == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/participating-org/' + str(ref)],
                       RDFS.label,
                       name))
            
        if not type == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/participating-org/' + str(ref)],
                       iati['organisation-type'],
                       iati['codelist/OrganisationType/' + str(type)]))
            
        if not role == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/participating-org/' + str(ref)],
                       iati['organisation-role'],
                       iati['codelist/OrganisationRole/' + str(role)]))

    return graph

def recipient_country(graph, xml, defaults, progress):
    '''Converts the XML of the recipient-country element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Keys
    code = __attribute_key(xml, 'code')
    percentage = __attribute_key(xml, 'percentage')
    
    # Text
    country_name = __attribute_text(xml, defaults['language'])
    
    if not code == None:
        graph.add((iati['activity/' + str(defaults['id'])],
                   iati['activity-recipient-country'],
                   iati['activity/' + str(defaults['id']) + '/recipient-country/' + str(code)]))
        
        graph.add((iati['activity/' + str(defaults['id']) + '/recipient-country/' + str(code)],
                   RDF.type,
                   iati['country']))
        
        graph.add((iati['activity/' + str(defaults['id']) + '/recipient-country/' + str(code)],
                   iati['country-code'],
                   iati['codelist/Country/' + str(code)]))
    
        if not country_name == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/recipient-country/' + str(code)],
                       RDFS.label,
                       country_name))
            
        if not percentage == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/recipient-country/' + str(code)],
                       iati['percentage'],
                       Literal(percentage)))

    return graph

def recipient_region(graph, xml, defaults, progress):
    '''Converts the XML of the recipient-region element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Keys
    code = __attribute_key(xml, 'code')
    percentage = __attribute_key(xml, 'percentage')
    
    # Text
    region_name = __attribute_text(xml, defaults['language'])
    
    if not code == None:
        graph.add((iati['activity/' + str(defaults['id'])],
                   iati['activity-recipient-region'],
                   iati['activity/' + str(defaults['id']) + '/recipient-region/' + str(code)]))
        
        graph.add((iati['activity/' + str(defaults['id']) + '/recipient-region/' + str(code)],
                   RDF.type,
                   iati['region']))
        
        graph.add((iati['activity/' + str(defaults['id']) + '/recipient-region/' + str(code)],
                   iati['region-code'],
                   iati['codelist/Region/' + str(code)]))
    
        if not region_name == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/recipient-region/' + str(code)],
                       RDFS.label,
                       region_name))
            
        if not percentage == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/recipient-region/' + str(code)],
                       iati['percentage'],
                       Literal(percentage)))

    return graph

def location(graph, xml, defaults, progress):
    '''Converts the XML of the location element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Keys
    percentage = __attribute_key(xml, 'percentage')
    
    # Elements
    name = xml.find('name')
    descriptions = xml.findall('description')
    location_type = xml.find('location-type')
    administrative = xml.find('administrative')
    coordinates = xml.find('coordinates')
    gazetteer_entry = xml.find('gazetteer-entry')
    
    graph.add((iati['activity/' + str(defaults['id'])],
           iati['activity-location'],
           iati['activity/' + str(defaults['id']) + '/location' + str(progress['location'])]))
    
    graph.add((iati['activity/' + str(defaults['id']) + '/location' + str(progress['location'])],
               RDF.type,
               iati['location']))    
    
    if not name == None:
        # Text
        name_text = __attribute_text(name, defaults['language'])
        
        graph.add((iati['activity/' + str(defaults['id']) + '/location' + str(progress['location'])],
                   RDFS.label,
                   name_text))
    
    if not descriptions == []:
        description_counter = 1
        
        for description in descriptions:
            # Keys
            type = __attribute_key(description, 'type')
            
            # Text
            description_text = __attribute_text(description, defaults['language'])
            
            if not description_text == None:
                graph.add((iati['activity/' + str(defaults['id']) + '/location' + str(progress['location'])],
                           iati['location-description'],
                           iati['activity/' + str(defaults['id']) + '/location' + str(progress['location']) + 
                                '/description' + str(description_counter)]))
                
                graph.add((iati['activity/' + str(defaults['id']) + '/location' + str(progress['location']) + 
                                '/description' + str(description_counter)],
                           RDF.type,
                           iati['description']))
                
                graph.add((iati['activity/' + str(defaults['id']) + '/location' + str(progress['location']) + 
                                '/description' + str(description_counter)],
                           iati['description'],
                           description_text))
                
                if not type == None:
                    graph.add((iati['activity/' + str(defaults['id']) + '/location' + str(progress['location']) + 
                                '/description' + str(description_counter)],
                               iati['description-type'],
                               iati['codelist/DescriptionType/' + str(type)]))  
                
                description_counter += 1
    
    if not location_type == None:
        # Keys
        location_type_code = __attribute_key(location_type, 'code')
        
        if not location_type_code == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/location' + str(progress['location'])],
                       iati['location-type'],
                       iati['codelist/LocationType/' + str(location_type_code)]))
    
    if not administrative == None:
        # Keys
        administrative_country = __attribute_key(administrative, 'country')
        
        # Text
        administrative_text = __attribute_text(administrative, defaults['language'])
        
        graph.add((iati['activity/' + str(defaults['id']) + '/location' + str(progress['location'])],
                   iati['location-administrative'],
                   iati['activity/' + str(defaults['id']) + '/location' + str(progress['location']) +
                        '/administrative']))
        
        if not administrative_country == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/location' + str(progress['location']) +
                            '/administrative'],
                       iati['administrative-country'],
                       iati['codelist/Country/' + str(administrative_country)]))
            
        if not administrative_text == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/location' + str(progress['location']) +
                            '/administrative'],
                       RDFS.label,
                       administrative_text))
    
    if not coordinates == None:
        # Keys
        latitude = __attribute_key(coordinates, 'latitude')
        longitude = __attribute_key(coordinates, 'longitude')
        precision = __attribute_key(coordinates, 'precision')
        
        graph.add((iati['activity/' + str(defaults['id']) + '/location' + str(progress['location'])],
                   iati['location-coordinates'],
                   iati['activity/' + str(defaults['id']) + '/location' + str(progress['location']) + '/coordinates']))
        
        if not latitude == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/location' + str(progress['location']) + '/coordinates'],
                       iati['latitude'],
                       Literal(latitude)))

        if not longitude == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/location' + str(progress['location']) + '/coordinates'],
                       iati['longitude'],
                       Literal(longitude)))
        
        if not precision == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/location' + str(progress['location']) + '/coordinates'],
                       iati['precision'],
                       iati['codelist/GeographicalPrecision/' + str(precision)]))
    
    if not gazetteer_entry == None:
        # Keys
        gazetteer_ref = __attribute_key(gazetteer_entry, 'gazzetteer-ref')
        
        # Text
        gazetteer_entry_text = gazetteer_entry.text
        gazetteer_entry_text = " ".join(gazetteer_entry_text.split())
        
        if not gazetteer_ref == None:
            if not gazetteer_entry_text == None:
            
                graph.add((iati['activity/' + str(defaults['id']) + '/location' + str(progress['location'])],
                           iati['location-gazetteer-entry'],
                           iati['gazetteer/' + str(gazetteer_ref) + str('/') + str(gazetteer_entry_text)]))
            
    return graph
 
def sector(graph, xml, defaults, progress):
    '''Converts the XML of the sector element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Keys
    code = __attribute_key(xml, 'code')
    vocabulary = __attribute_key(xml, 'vocabulary')
    percentage = __attribute_key(xml, 'percentage')
    
    # Text
    name = __attribute_text(xml, defaults['language'])
    
    if not code == None:
        if not vocabulary == None:
            
            graph.add((iati['activity/' + str(defaults['id'])],
                       iati['activity-sector'],
                       iati['activity/' + str(defaults['id']) + '/sector/' + str(vocabulary) +
                            '/' + str(code)]))
            
            graph.add((iati['activity/' + str(defaults['id']) + '/sector/' + str(vocabulary) +
                            '/' + str(code)],
                       RDF.type,
                       iati['sector']))
            
            graph.add((iati['activity/' + str(defaults['id']) + '/sector/' + str(vocabulary) +
                            '/' + str(code)],
                       iati['sector-code'],
                       iati['codelist/Sector/' + str(vocabulary) + '/' + str(code)]))
            
            if not percentage == None:
                graph.add((iati['activity/' + str(defaults['id']) + '/sector/' + str(vocabulary) +
                                '/' + str(code)],
                           iati['percentage'],
                           Literal(percentage)))
                
            if not name == None:
                graph.add((iati['activity/' + str(defaults['id']) + '/sector/' + str(vocabulary) +
                                '/' + str(code)],
                           RDFS.label,
                           name))                

    return graph

def policy_marker(graph, xml, defaults, progress):
    '''Converts the XML of the policy-marker element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Keys
    code = __attribute_key(xml, 'code')
    vocabulary = __attribute_key(xml, 'vocabulary')
    significance = __attribute_key(xml, 'significance')
    
    # Text
    name = __attribute_text(xml, defaults['language'])
    
    if not code == None:
        if not vocabulary == None:
            
            graph.add((iati['activity/' + str(defaults['id'])],
                       iati['activity-policy-marker'],
                       iati['activity/' + str(defaults['id']) + '/policy-marker/' + str(vocabulary) +
                            '/' + str(code)]))
            
            graph.add((iati['activity/' + str(defaults['id']) + '/policy-marker/' + str(vocabulary) +
                            '/' + str(code)],
                       RDF.type,
                       iati['policy-marker']))
            
            graph.add((iati['activity/' + str(defaults['id']) + '/policy-marker/' + str(vocabulary) +
                            '/' + str(code)],
                       iati['policy-marker-code'],
                       iati['codelist/PolicyMarker/' + str(vocabulary) + '/' + str(code)]))
            
            if not significance == None:
                graph.add((iati['activity/' + str(defaults['id']) + '/policy-marker/' + str(vocabulary) +
                                '/' + str(code)],
                           iati['significance-code'],
                           iati['codelist/PolicySignificance/' + str(significance)]))
                
            if not name == None:
                graph.add((iati['activity/' + str(defaults['id']) + '/policy-marker/' + str(vocabulary) +
                                '/' + str(code)],
                           RDFS.label,
                           name))                

    return graph

def collaboration_type(graph, xml, defaults, progress):
    '''Converts the XML of the collaboration-type element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Keys
    code = __attribute_key(xml, 'code')
    
    if not code == None:
        graph.add((iati['activity/' + str(defaults['id'])],
                   iati['activity-collaboration-type'],
                   iati['codelist/CollaborationType/' + str(code)]))
    
    return graph

def default_finance_type(graph, xml, defaults, progress):
    '''Converts the XML of the default-finance-type element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Keys
    code = __attribute_key(xml, 'code')
    
    if not code == None:
        graph.add((iati['activity/' + str(defaults['id'])],
                   iati['activity-default-finance-type'],
                   iati['codelist/FinanceType/' + str(code)]))
    
    return graph

def default_flow_type(graph, xml, defaults, progress):
    '''Converts the XML of the default-flow-type element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Keys
    code = __attribute_key(xml, 'code')
    
    if not code == None:
        graph.add((iati['activity/' + str(defaults['id'])],
                   iati['activity-default-flow-type'],
                   iati['codelist/FlowType/' + str(code)]))
    
    return graph

def default_aid_type(graph, xml, defaults, progress):
    '''Converts the XML of the default-aid-type element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Keys
    code = __attribute_key(xml, 'code')
    
    if not code == None:
        graph.add((iati['activity/' + str(defaults['id'])],
                   iati['activity-default-aid-type'],
                   iati['codelist/AidType/' + str(code)]))
    
    return graph

def default_tied_status(graph, xml, defaults, progress):
    '''Converts the XML of the default-tied-status element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Keys
    code = __attribute_key(xml, 'code')
    
    if not code == None:
        graph.add((iati['activity/' + str(defaults['id'])],
                   iati['activity-default-tied-status'],
                   iati['codelist/TiedStatus/' + str(code)]))
    
    return graph

def budget(graph, xml, defaults, progress):
    '''Converts the XML of the budget element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Keys
    type = __attribute_key(xml, 'type')
    
    # Elements
    period_start = xml.find('period-start')
    period_end = xml.find('period-end')
    value = xml.find('value')
    
    graph.add((iati['activity/' + str(defaults['id'])],
               iati['activity-budget'],
               iati['activity/' + str(defaults['id']) + '/budget' + str(progress['budget'])]))
    
    graph.add((iati['activity/' + str(defaults['id']) + '/budget' + str(progress['budget'])],
               RDF.type,
               iati['budget']))
    
    if not type == None:        
        graph.add((iati['activity/' + str(defaults['id']) + '/budget' + str(progress['budget'])],
                   iati['budget-type'],
                   iati['codelist/BudgetType/' + str(type)]))
    
    if not period_start == None:
        # Keys
        date = __attribute_key(period_start, 'iso-date')
        
        # Text
        period_start_text = __attribute_text(period_start, defaults['language'])
        
        graph.add((iati['activity/' + str(defaults['id']) + '/budget' + str(progress['budget'])],
                   iati['budget-period-start'],
                   iati['activity/' + str(defaults['id']) + '/budget' + str(progress['budget']) + '/period-start']))
        
        if not date == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/budget' + str(progress['budget']) + '/period-start'],
                       iati['date'],
                       Literal(date)))
        
        if not period_start_text == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/budget' + str(progress['budget']) + '/period-start'],
                       RDFS.label,
                       period_start_text))
    
    if not period_end == None:
        # Keys
        date = __attribute_key(period_end, 'iso-date')
        
        # Text
        period_end_text = __attribute_text(period_end, defaults['language'])
        
        graph.add((iati['activity/' + str(defaults['id']) + '/budget' + str(progress['budget'])],
                   iati['budget-period-end'],
                   iati['activity/' + str(defaults['id']) + '/budget' + str(progress['budget']) + '/period-end']))
        
        if not date == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/budget' + str(progress['budget']) + '/period-end'],
                       iati['date'],
                       Literal(date)))
        
        if not period_end_text == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/budget' + str(progress['budget']) + '/period-end'],
                       RDFS.label,
                       period_end_text))
    
    if not value == None:
        # Keys
        currency = __attribute_key(value, 'currency')
        value_date = __attribute_key(value, 'value-date')
        
        # Text
        value_text = value.text
        value_text = " ".join(value_text.split())
        
        if not value_text == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/budget' + str(progress['budget'])],
                       iati['budget-value'],
                       iati['activity/' + str(defaults['id']) + '/budget' + str(progress['budget']) + '/value']))
            
            graph.add((iati['activity/' + str(defaults['id']) + '/budget' + str(progress['budget']) + '/value'],
                       RDF.type,
                       iati['value']))
            
            graph.add((iati['activity/' + str(defaults['id']) + '/budget' + str(progress['budget']) + '/value'],
                       iati['value'],
                       Literal(value_text)))
            
            if not currency == None:
                graph.add((iati['activity/' + str(defaults['id']) + '/budget' + str(progress['budget']) + '/value'],
                           iati['currency'],
                           iati['codelist/Currency/' + str(currency)]))
            
            elif not defaults['currency'] == None:
                graph.add((iati['activity/' + str(defaults['id']) + '/budget' + str(progress['budget']) + '/value'],
                           iati['currency'],
                           iati['codelist/Currency/' + str(defaults['currency'])]))
            
            if not value_date == None:
                graph.add((iati['activity/' + str(defaults['id']) + '/budget' + str(progress['budget']) + '/value'],
                           iati['value-date'],
                           Literal(value_date)))                                          

    return graph

def planned_disbursement(graph, xml, defaults, progress):
    '''Converts the XML of the planned-disbursement element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Keys
    updated = __attribute_key(xml, 'updated')
    
    # Elements
    period_start = xml.find('period-start')
    period_end = xml.find('period-end')
    value = xml.find('value')
    
    graph.add((iati['activity/' + str(defaults['id'])],
               iati['activity-planned-disbursement'],
               iati['activity/' + str(defaults['id']) + '/planned-disbursement' + str(progress['planned_disbursement'])]))
    
    graph.add((iati['activity/' + str(defaults['id']) + '/planned-disbursement' + str(progress['planned_disbursement'])],
               RDF.type,
               iati['planned-disbursement']))
    
    if not updated == None:        
        graph.add((iati['activity/' + str(defaults['id']) + '/planned-disbursement' + str(progress['planned_disbursement'])],
                   iati['updated'],
                   Literal(updated)))
    
    if not period_start == None:
        # Keys
        date = __attribute_key(period_start, 'iso-date')
        
        # Text
        period_start_text = __attribute_text(period_start, defaults['language'])
        
        graph.add((iati['activity/' + str(defaults['id']) + '/planned-disbursement' + str(progress['planned_disbursement'])],
                   iati['planned-disbursement-period-start'],
                   iati['activity/' + str(defaults['id']) + '/planned-disbursement' + str(progress['planned_disbursement']) + 
                        '/period-start']))
        
        if not date == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/planned-disbursement' + 
                            str(progress['planned_disbursement']) + '/period-start'],
                       iati['date'],
                       Literal(date)))
        
        if not period_start_text == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/planned-disbursement' + 
                            str(progress['planned_disbursement']) + '/period-start'],
                       RDFS.label,
                       period_start_text))
    
    if not period_end == None:
        # Keys
        date = __attribute_key(period_end, 'iso-date')
        
        # Text
        period_end_text = __attribute_text(period_end, defaults['language'])
        
        graph.add((iati['activity/' + str(defaults['id']) + '/planned-disbursement' + str(progress['planned_disbursement'])],
                   iati['planned-disbursement-period-end'],
                   iati['activity/' + str(defaults['id']) + '/planned-disbursement' + str(progress['planned_disbursement']) + 
                        '/period-end']))
        
        if not date == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/planned-disbursement' + 
                            str(progress['planned_disbursement']) + '/period-end'],
                       iati['date'],
                       Literal(date)))
        
        if not period_end_text == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/planned-disbursement' + 
                            str(progress['planned_disbursement']) + '/period-end'],
                       RDFS.label,
                       period_end_text))
    
    if not value == None:
        # Keys
        currency = __attribute_key(value, 'currency')
        value_date = __attribute_key(value, 'value-date')
        
        # Text
        value_text = value.text
        value_text = " ".join(value_text.split())
        
        if not value_text == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/planned-disbursement' + str(progress['planned_disbursement'])],
                       iati['planned-disbursement-value'],
                       iati['activity/' + str(defaults['id']) + '/planned-disbursement' + 
                            str(progress['planned_disbursement']) + '/value']))
            
            graph.add((iati['activity/' + str(defaults['id']) + '/planned-disbursement' + 
                            str(progress['planned_disbursement']) + '/value'],
                       RDF.type,
                       iati['value']))
            
            graph.add((iati['activity/' + str(defaults['id']) + '/planned-disbursement' + 
                            str(progress['planned_disbursement']) + '/value'],
                       iati['value'],
                       Literal(value_text)))
            
            if not currency == None:
                graph.add((iati['activity/' + str(defaults['id']) + '/planned-disbursement' + 
                                str(progress['planned_disbursement']) + '/value'],
                           iati['currency'],
                           iati['codelist/Currency/' + str(currency)]))
            
            elif not defaults['currency'] == None:
                graph.add((iati['activity/' + str(defaults['id']) + '/planned-disbursement' + 
                                str(progress['planned_disbursement']) + '/value'],
                           iati['currency'],
                           iati['codelist/Currency/' + str(defaults['currency'])]))
            
            if not value_date == None:
                graph.add((iati['activity/' + str(defaults['id']) + '/planned-disbursement' + 
                                str(progress['planned_disbursement']) + '/value'],
                           iati['value-date'],
                           Literal(value_date)))                                          

    return graph

def transaction(graph, xml, defaults, progress):
    '''Converts the XML of the transaction element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Keys
    ref = __attribute_key(xml, 'ref')
    
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
    
    if not ref == None:
        transaction_id = iati['activity/' + str(defaults['id']) + '/transaction/' + str(ref)]
    else:
        transaction_id = iati['activity/' + str(defaults['id']) + '/transaction' + str(progress['transaction'])]
        
    graph.add((iati['activity/' + str(defaults['id'])],
               iati['activity-transaction'],
               transaction_id))        
    
    graph.add((transaction_id,
               RDF.type,
               iati['transaction']))
    
    if not aid_type == None:
        # Keys
        code = __attribute_key(aid_type, 'code')
        
        if not code == None:
            graph.add((transaction_id,
                       iati['aid-type'],
                       iati['codelist/AidType/' + str(code)]))
            
        elif not defaults['aid_type'] == None:
            graph.add((transaction_id,
                       iati['aid-type'],
                       iati['codelist/AidType/' + str(defaults['aid_type'])]))
        
    elif not defaults['aid_type'] == None:
        graph.add((transaction_id,
                   iati['aid-type'],
                   iati['codelist/AidType/' + str(defaults['aid_type'])]))
        
    if not descriptions == []:
        description_counter = 1
        
        for description in descriptions:
            # Keys
            type = __attribute_key(description, 'type')
            
            # Text
            description_text = __attribute_text(description, defaults['language'])
            
            if not description_text == None:
                graph.add((transaction_id,
                           iati['transaction-description'],
                           URIRef(transaction_id + '/description' + str(description_counter))))
                
                graph.add((URIRef(transaction_id + '/description' + str(description_counter)),
                           RDF.type,
                           iati['description']))
                
                graph.add((URIRef(transaction_id + '/description' + str(description_counter)),
                           iati['description'],
                           description_text))
                
                if not type == None:
                    graph.add((URIRef(transaction_id + '/description' + str(description_counter)),
                               iati['description-type'],
                               iati['codelist/DescriptionType/' + str(type)]))  
                
                description_counter += 1
    
    if not disbursement_channel == None:
        # Keys
        code = __attribute_key(disbursement_channel, 'code')
        
        graph.add((transaction_id,
                   iati['disbursement-channel'],
                   iati['codelist/disbursementChannel/' + str(code)]))
    
    if not finance_type == None:
        # Keys
        code = __attribute_key(finance_type, 'code')
        
        if not code == None:
            graph.add((transaction_id,
                       iati['finance-type'],
                       iati['codelist/FinanceType/' + str(code)]))
            
        elif not defaults['finance_type'] == None:
            graph.add((transaction_id,
                       iati['finance-type'],
                       iati['codelist/FinanceType/' + str(defaults['finance_type'])]))
        
    elif not defaults['tied_status'] == None:
        graph.add((transaction_id,
                   iati['finance-type'],
                   iati['codelist/FinanceType/' + str(defaults['finance_type'])]))
    
    if not flow_type == None:
        # Keys
        code = __attribute_key(flow_type, 'code')
        
        if not code == None:
            graph.add((transaction_id,
                       iati['flow-type'],
                       iati['codelist/FlowType/' + str(code)]))
            
        elif not defaults['flow_type'] == None:
            graph.add((transaction_id,
                       iati['flow-type'],
                       iati['codelist/FlowType/' + str(defaults['flow_type'])]))
        
    elif not defaults['tied_status'] == None:
        graph.add((transaction_id,
                   iati['flow-type'],
                   iati['codelist/FlowType/' + str(defaults['flow_type'])]))
    
    if not provider_org == None:
        # Keys
        ref = __attribute_key(provider_org, 'ref')
        provider_activity_id = __attribute_key(provider_org, 'provider-activity-id')
        
        # Text
        provider_org_text = provider_org.text
        provider_org_text = " ".join(provider_org_text.split())
        
        graph.add((transaction_id,
                   iati['provider-org'],
                   URIRef(transaction_id + '/provider-org')))        
        
        if not ref == None:
            graph.add((URIRef(transaction_id + '/provider-org'),
                       iati['organisation-ref'],
                       iati['codelist/OrganisationIdentifier/' + str(ref)]))
        
        if not provider_activity_id == None:
            graph.add((URIRef(transaction_id + '/provider-org'),
                       iati['provider-activity-id'],
                       iati['activity/' + str(provider_activity_id)]))
            
    if not receiver_org == None:
        # Keys
        ref = __attribute_key(receiver_org, 'ref')
        receiver_activity_id = __attribute_key(receiver_org, 'receiver-activity-id')
        
        # Text
        receiver_org_text = receiver_org.text
        receiver_org_text = " ".join(receiver_org_text.split())
        
        graph.add((transaction_id,
                   iati['receiver-org'],
                   URIRef(transaction_id + '/receiver-org')))        
        
        if not ref == None:
            graph.add((URIRef(transaction_id + '/receiver-org'),
                       iati['organisation-ref'],
                       iati['codelist/OrganisationIdentifier/' + str(ref)]))
        
        if not receiver_activity_id == None:
            graph.add((URIRef(transaction_id + '/receiver-org'),
                       iati['receiver-activity-id'],
                       iati['activity/' + str(receiver_activity_id)]))

    if not tied_status == None:
        # Keys
        code = __attribute_key(tied_status, 'code')
        
        if not code == None:
            graph.add((transaction_id,
                       iati['tied-status'],
                       iati['codelist/TiedStatus/' + str(code)]))
            
        elif not defaults['tied_status'] == None:
            graph.add((transaction_id,
                       iati['tied-status'],
                       iati['codelist/TiedStatus/' + str(defaults['tied_status'])]))
        
    elif not defaults['tied_status'] == None:
        graph.add((transaction_id,
                   iati['tied-status'],
                   iati['codelist/TiedStatus/' + str(defaults['tied_status'])]))
    
    if not transaction_date == None:
        # Keys
        iso_date = __attribute_key(transaction_date, 'iso-date')
        
        if not iso_date == None:
            graph.add((transaction_id,
                       iati['transaction-date'],
                       Literal(iso_date)))
        
    if not transaction_type == None:
        # Keys
        code = __attribute_key(transaction_type, 'code')
        
        if not code == None:
            graph.add((transaction_id,
                       iati['transaction-type'],
                       iati['codelist/TransactionType/' + str(code)]))            
                                     
    if not value == None:
        # Keys
        currency = __attribute_key(value, 'currency')
        value_date = __attribute_key(value, 'value-date')
        
        # Text
        value_text = value.text
        value_text = " ".join(value_text.split())
        
        if not value_text == None:
            graph.add((transaction_id,
                       iati['transaction-value'],
                       URIRef(transaction_id + '/value')))
            
            graph.add((URIRef(transaction_id + '/value'),
                       RDF.type,
                       iati['value']))
            
            graph.add((URIRef(transaction_id + '/value'),
                       iati['value'],
                       Literal(value_text)))
            
            if not currency == None:
                graph.add((URIRef(transaction_id + '/value'),
                           iati['currency'],
                           iati['codelist/Currency/' + str(currency)]))
            
            elif not defaults['currency'] == None:
                graph.add((URIRef(transaction_id + '/value'),
                           iati['currency'],
                           iati['codelist/Currency/' + str(defaults['currency'])]))
            
            if not value_date == None:
                graph.add((URIRef(transaction_id + '/value'),
                           iati['value-date'],
                           Literal(value_date)))  

    return graph

def document_link(graph, xml, defaults, progress):
    '''Converts the XML of the document-link element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Keys
    url = __attribute_key(xml, 'url')
    format = __attribute_key(xml, 'format')
    
    # Elements
    titles = xml.findall('title')
    category = xml.find('category')
    languages = xml.findall('language')
    
    graph.add((iati['activity/' + str(defaults['id'])],
               iati['activity-document-link'],
               iati['document-link' + str(progress['document_link'])]))
    
    graph.add((iati['document-link' + str(progress['document_link'])],
               RDF.type,
               iati['document-link']))    
    
    if not url == None:
        graph.add((iati['document-link' + str(progress['document_link'])],
                   iati['url'],
                   URIRef(url)))
    
    if not format == None:
        graph.add((iati['document-link' + str(progress['document_link'])],
                   iati['format'],
                   iati['codelist/FileFormat/' + str(format)]))
        
    if not titles == []:
        for title in titles:
            # Text
            name = __attribute_text(title, defaults['language'])
            
            graph.add((iati['document-link' + str(progress['document_link'])],
                       RDFS.label,
                       name))
            
    if not category == None:
        # Keys
        code = __attribute_key(category, 'code')
        
        graph.add((iati['document-link' + str(progress['document_link'])],
                   iati['document-category'],
                   iati['codelist/DocumentCategory/' + str(code)]))
    
    if not languages == []:
        for language in languages:
            # Keys
            code = __attribute_key(language, 'code')
            
            # Text
            name = __attribute_text(language, defaults['language'])
            
            if not code == None:
                graph.add((iati['document-link' + str(progress['document_link'])],
                           iati['language'],
                           iati['document-link' + str(progress['document_link']) + '/language/' + str(code)]))
                
                if not name == None:
                    graph.add((iati['document-link' + str(progress['document_link']) + '/language/' + str(code)],
                               RDFS.label,
                               name))
    
    return graph

def related_activity(graph, xml, defaults, progress):
    '''Converts the XML of the related-activity element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Keys
    ref = __attribute_key(xml, 'ref')
    type = __attribute_key(xml, 'type')
    
    # Text
    name = __attribute_text(xml, defaults['language'])
    
    if not ref == None:
        graph.add((iati['activity/' + str(defaults['id'])],
                   iati['related-activity'],
                   iati['activity/' + str(defaults['id']) + '/related-activity/' + str(ref)]))
        
        graph.add((iati['activity/' + str(defaults['id']) + '/related-activity/' + str(ref)],
                   iati['activity-id'],
                   iati['activity/' + str(ref)]))
        
        if not type == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/related-activity/' + str(ref)],
                   iati['related-activity-type'],
                   iati['codelist/RelatedActivityType/' + str(type)]))
    
        if not name == None:
            graph.add((iati['activity/' + str(defaults['id']) + '/elated-activity/' + str(ref)],
                       RDFS.label,
                       name))
               
    return graph

def conditions(graph, xml, defaults, progress):
    '''Converts the XML of the conditions element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Elements
    conditions = xml.findall('condition')
    
    if not conditions == []:
        condition_counter = 1
        
        for condition in conditions:
            # Keys
            type = __attribute_key(condition, 'type')
            
            # Text
            condition_text = __attribute_text(condition, defaults['language'])
            
            if not condition_text == None:
                   graph.add((iati['activity/' + str(defaults['id'])],
                              iati['activity-condition'],
                              iati['activity/' + str(defaults['id']) + '/condition' + str(condition_counter)]))
                   
                   graph.add((iati['activity/' + str(defaults['id']) + '/condition' + str(condition_counter)],
                              RDF.type,
                              iati['condition']))
                   
                   if not type == None:
                       graph.add((iati['activity/' + str(defaults['id']) + '/condition' + str(condition_counter)],
                                  iati['condition-type'],
                                  iati['codelist/ConditionType/' + str(type)]))                                          
        
            condition_counter += 1
               
    return graph

def result(graph, xml, defaults, progress):
    '''Converts the XML of the conditions element to a RDFLib Graph.
    
    Parameters
    @graph: The RDFLib Graph to which statement should be added.
    @xml: The XML of this element.
    @defaults: A dictionary of defaults of the activity.
    @progress: A dictionary of the progress so far.
    
    Returns
    @graph: The RDFLib Graph with statements added.'''
    
    iati = defaults['namespace']
    
    # Keys
    type = __attribute_key(xml, 'type')
    aggregation_status = __attribute_key(xml, 'aggregation-status')
    
    # Elements
    titles = xml.findall('title')
    descriptions = xml.findall('description')
    indicators = xml.findall('indicator')
    
    graph.add((iati['activity/' + str(defaults['id'])],
               iati['activity-result'],
               iati['activity/' + str(defaults['id']) + '/result' + str(progress['result'])]))
    
    graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result'])],
               RDF.type,
               iati['result']))    
    
    if not titles == []:
        for title in titles:
            # Text
            title_text = __attribute_text(title, defaults['language'])
            
            if not title_text == None:
                graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result'])],
                           RDFS.label,
                           title_text))
    
    if not descriptions == []:
        description_counter = 1
        
        for description in descriptions:
            # Keys
            type = __attribute_key(description, 'type')
            
            # Text
            description_text = __attribute_text(description, defaults['language'])
            
            if not description_text == None:
                graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result'])],
                           iati['result-description'],
                           iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                '/description' + str(description_counter)]))
                
                graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                '/description' + str(description_counter)],
                           RDF.type,
                           iati['description']))
                
                graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                '/description' + str(description_counter)],
                           iati['description'],
                           description_text))
                
                if not type == None:
                    graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                    '/description' + str(description_counter)],
                               iati['description-type'],
                               iati['codelist/DescriptionType/' + str(type)]))                                   
            
            description_counter += 1
        
    if not indicators == []:
        indicator_counter = 1
        
        for indicator in indicators:
            # Keys
            measure = __attribute_key(description, 'measure')
            ascending = __attribute_key(description, 'ascending')
            
            # Elements
            titles = indicator.findall('title')
            descriptions = indicator.findall('description')
            periods = indicator.findall('indicator')
            baseline = indicator.find('baseline')
            
            graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result'])],
                       iati['result-indicator'],
                       iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                            '/indicator' + str(indicator_counter)]))
            
            graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                            '/indicator' + str(indicator_counter)],
                       RDF.type,
                       iati['indicator']))
            
            if not measure == None:
                graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                '/indicator' + str(indicator_counter)],
                           iati['indicator-measure'],
                           iati['codelist/IndicatorMeasure/' + str(measure)]))
            
            if not ascending == None:
                graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                '/indicator' + str(indicator_counter)],
                           iati['indicator-ascending'],
                           Literal(ascending)))

            if not titles == []:
                for title in titles:
                    # Text
                    title_text = __attribute_text(title, defaults['language'])
                    
                    if not title_text == None:
                        graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                        '/indicator' + str(indicator_counter)],
                                   RDFS.label,
                                   title_text))

            if not descriptions == []:
                description_counter = 1
                
                for description in descriptions:
                    # Keys
                    type = __attribute_key(description, 'type')
                    
                    # Text
                    description_text = __attribute_text(description, defaults['language'])
                    
                    if not description_text == None:
                        graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                        '/indicator' + str(indicator_counter)],
                                   iati['indicator-description'],
                                   iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                        '/indicator' + str(indicator_counter) + '/description' + 
                                        str(description_counter)]))
                        
                        graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                        '/indicator' + str(indicator_counter) + '/description' + 
                                        str(description_counter)],
                                   RDF.type,
                                   iati['description']))
                        
                        graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                        '/indicator' + str(indicator_counter) + '/description' + 
                                        str(description_counter)],
                                   iati['description'],
                                   description_text))
                        
                        if not type == None:
                            graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                            '/indicator' + str(indicator_counter) + '/description' + 
                                            str(description_counter)],
                                       iati['description-type'],
                                       iati['codelist/DescriptionType/' + str(type)]))                                   
                    
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
                        date = __attribute_key(period_start, 'iso-date')
                        
                        # Text
                        period_start_text = __attribute_text(period_start, defaults['language'])
                        
                        graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                        '/indicator' + str(indicator_counter)],
                                   iati['indicator-period-start'],
                                   iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                        '/indicator' + str(indicator_counter) + '/period-start']))
                        
                        if not date == None:
                            graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                            '/indicator' + str(indicator_counter) + '/period-start'],
                                       iati['date'],
                                       Literal(date)))
                        
                        if not period_start_text == None:
                            graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                            '/indicator' + str(indicator_counter) + '/period-start'],
                                       RDFS.label,
                                       period_start_text))
                        
                    if not period_end == None:
                        # Keys
                        date = __attribute_key(period_end, 'iso-date')
                        
                        # Text
                        period_end_text = __attribute_text(period_end, defaults['language'])
                        
                        graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                        '/indicator' + str(indicator_counter)],
                                   iati['indicator-period-end'],
                                   iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                        '/indicator' + str(indicator_counter) + '/period-end']))
                        
                        if not date == None:
                            graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                            '/indicator' + str(indicator_counter) + '/period-end'],
                                       iati['date'],
                                       Literal(date)))
                        
                        if not period_end_text == None:
                            graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                            '/indicator' + str(indicator_counter) + '/period-end'],
                                       RDFS.label,
                                       period_end_text))
                    
                    if not target == None:
                        # Keys
                        value = __attribute_key(target, 'value')
                        
                        if not value == None:
                            graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                            '/indicator' + str(indicator_counter)],
                                       iati['indicator-target'],
                                       Literal(value)))
                        
                    if not actual == None:
                        # Keys
                        value = __attribute_key(actual, 'value')
                        
                        if not value == None:
                            graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                            '/indicator' + str(indicator_counter)],
                                       iati['indicator-actual'],
                                       Literal(value)))                    
                        
                    period_counter += 1
                    
                if not baseline == None:
                    # Keys
                    year = __attribute_key(baseline, 'year')
                    value = __attribute_key(baseline, 'value')
                    
                    # Elements
                    comment = baseline.find('comment')
                    
                    graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                    '/indicator' + str(indicator_counter)],
                               iati['indicator-baseline'],
                               iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                    '/indicator' + str(indicator_counter) + '/baseline']))                       
                    
                    if not value == None:
                        graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                        '/indicator' + str(indicator_counter) + '/baseline'],
                                   iati['value'],
                                   Literal(value)))
                        
                    if not year == None:
                        graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                        '/indicator' + str(indicator_counter) + '/baseline'],
                                   iati['year'],
                                   Literal(year)))
                    
                    if not comment == None:
                        # Text
                        comment_text = __attribute_text(comment, defaults['language'])
                        
                        graph.add((iati['activity/' + str(defaults['id']) + '/result' + str(progress['result']) + 
                                        '/indicator' + str(indicator_counter) + '/baseline'],
                                   RDFS.comment,
                                   comment_text))                        
            
            indicator_counter += 1
               
    return graph