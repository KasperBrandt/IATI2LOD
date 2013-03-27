## SparqlContext.py
## By Kasper Brandt
## Last updated on 25-03-2013

from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Literal, Graph, URIRef

class context :
    '''Class for easy querying of a context and convert it to a RDFLib Graph.'''
    
    def __init__(self, triple_store, context):
        '''Initializes the sparql class.
        
        Parameters
        @triple_store: The URL of the triple store.
        @context: The URL of the context.'''
        
        query = """
        SELECT ?subject ?predicate ?object
        FROM NAMED <""" + context + """>
        WHERE {
            GRAPH <""" + context + """>
                { ?subject ?predicate ?object . }
        }
        """
        
        self.wrapper = SPARQLWrapper(triple_store)
        self.wrapper.setQuery(query)
        self.wrapper.setReturnFormat(JSON)
        
        self.graph = Graph()
    
    def __get_value(self, triple_value):
        '''Retrieves the value of the URI or Literal. Other types are not considered.
        
        Parameters
        @triple_value: A dictionary of a triple value.
        
        Returns
        @value: A RDFLib value. Either an URI string or RDFLib Literal.'''

        if triple_value['type'] == 'uri':
            return URIRef(triple_value['value'])
        elif triple_value['type'] == 'literal':
            return Literal(triple_value['value'])
        elif triple_value['type'] == 'typed-literal':
            return Literal(triple_value['value'], datatype=triple_value['datatype'])
        else:
            return URIRef(triple_value['value'])
    
    def convert(self):
        '''Converts the query to a RDFLib Graph.
        
        Returns
        @graph: A RDFLib Graph.'''
        
        content = self.wrapper.query().convert()
        
        for triple in content['results']['bindings']:
            triple_subject = self.__get_value(triple['subject'])
            triple_predicate = self.__get_value(triple['predicate'])
            triple_object = self.__get_value(triple['object'])
            
            self.graph.add((triple_subject, triple_predicate, triple_object))
        
        return self.graph