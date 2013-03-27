## CodelistsConverter.py
## By Kasper Brandt
## Last updated on 27-03-2013

from rdflib import RDFS, Namespace, URIRef, Literal, XSD

class codelist :
    '''Class for converting a codelist dictionary to a RDFLib.'''
    
    def __init__(self, dictionary, graph, triple_store):
        '''Initializes the codelist class.
        
        Parameters
        @dictionary: A dictionary of all codelists to be updated.
        @graph: A graph of all triples in the codelist context.'''
        
        self.dictionary = dictionary
        self.graph = graph
        self.triple_store = triple_store
        
        self.codelist = Namespace(triple_store + "/codelist/")
        
        self.mapping = dict([('name', RDFS.label),
                            ('description', RDFS.comment),
                            ('category', self.codelist['category']),
                            ('category-name', RDFS.label),
                            ('category-description', RDFS.comment),
                            ('abbreviation', self.codelist['abbreviation'])])

    def __element_in_codelist_category(self, codelist_key, element):
        '''Looks whether an element has a category element.
        
        Parameters
        @codelist_key: The key of a codelist.
        @element: The string of the element to be looked for. 
        
        Returns
        @status: True if the element is present. False otherwise.'''
        
        if element in self.dictionary[codelist_key][1].keys():
            return True
        
        return False
    
    def __add_date_last_modified(self, codelist_key):
        '''Adds the date-last-modified to the graph.
        
        Parameters
        @codelist_key: The key of a codelist.'''
        
        subject = self.codelist[codelist_key]
        predicate = self.codelist['date-last-modified']
        object = Literal(self.dictionary[codelist_key]['date-last-modified'], datatype=XSD.dateTime)
        
        self.graph.set((subject, predicate, object))       
    
    def __add_element(self, codelist_key, code_key, has_language):
        '''Adds element to the graph.
        
        Parameters
        @codelist_key: The key of a codelist.
        @code_key: The key of the code.
        @has_language: Boolean whether a language element is present.'''
            
        subject = self.codelist[str(codelist_key) + 
                                    '/' + 
                                    str(self.dictionary[codelist_key][code_key]['code'])]
        self.graph.add((self.codelist[codelist_key], self.codelist['code'], subject))
            
        for key in self.dictionary[codelist_key][code_key]:
            
            if not (key == 'category') and not (key == 'code') and not (key == 'language'):
                
                if (key == 'category-name') or (key == 'category-description'):
                    subject = self.codelist[str(codelist_key) + 
                                    '/' + 
                                    str(self.dictionary[codelist_key][code_key]['category'])]
                
                predicate = self.mapping[key]
                object = Literal(self.dictionary[codelist_key][code_key][key])
                
                if has_language:
                    object = Literal(self.dictionary[codelist_key][code_key][key],
                                     lang = self.dictionary[codelist_key][code_key]['language'])
                
                self.graph.set((subject, predicate, object))
                    
            elif key == 'category':
                predicate = self.mapping[key]
                object = self.codelist[str(codelist_key) + 
                                    '/' + 
                                    str(self.dictionary[codelist_key][code_key][key])]
                
                self.graph.set((subject, predicate, object))
                                  
    
    def __parse_codelist(self, codelist_key):
        '''Parses a codelist from the dictionary.
        
        Parameters
        @codelist_key: The key of a codelist.'''
                        
        has_language = self.__element_in_codelist_category(codelist_key, 'language')
        
        for code_key in self.dictionary[codelist_key]:
             
            if code_key == 'date-last-modified':
                self.__add_date_last_modified(codelist_key)
            
            else:
                self.__add_element(codelist_key, code_key, has_language)

    def update(self):
        '''Updates the Graph with the new values from the dictionary.
        
        Returns
        @updated_graph: An updated RDFLib graph.'''
        
        for codelist_key in self.dictionary:
            
            self.graph.add((Namespace(self.triple_store + "/codelist"),
                            self.codelist['codelist'], 
                            self.codelist[codelist_key]))
            
            self.__parse_codelist(codelist_key)
                                            
        return self.graph