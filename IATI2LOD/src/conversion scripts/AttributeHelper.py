from rdflib import Literal

def attribute_key(xml, key):
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

def attribute_text(xml, attribute):
    '''Checks whether an attribute is in the XML.
    Returns the value of the text or None if not present.
    
    Parameters
    @xml: An ElementTree.
    @attribute: A string of the attribute.
    
    Returns
    @value_list: A list of possible text values of the attribute 
                 or None if not present.'''
    
    value_list = []
    
    try:
        for element in xml.findall(attribute):
            value_list.append(element.text)
        
        if value_list == []:
            return None
        else:
            return value_list
    
    except AttributeError:
        return None

def attribute_language(xml, language):
    '''Checks whether an element has a text and picks the correct language.
    
    Parameters
    @xml: An ElemenTree of the element.
    @language: The default language of the activity.
    
    Returns
    @literal: A RDFLib Literal or None.'''
    
    if xml.text == None:
        return None
    
    node_language = attribute_key(xml, "{http://www.w3.org/XML/1998/namespace}lang")
    
    text = xml.text
    formatted_text = " ".join(text.split())
    
    if not node_language == None:
        return Literal(formatted_text, lang=node_language)
    
    if not language == None:
        return Literal(formatted_text, lang=language)
    
    return Literal(formatted_text)