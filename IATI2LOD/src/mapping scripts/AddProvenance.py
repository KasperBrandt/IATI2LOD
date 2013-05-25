## By Kasper Brandt
## Last updated on 22-05-2013

from rdflib import Namespace, Literal, URIRef, Graph, RDF, RDFS
import hashlib

def addProv(namespace, graph, doc_name, start_time, source_xml, entities, script):
    '''Adds W3C Provenance to the provenance graph.
    
    Parameters:
    @namespace: The default RDFLib Namespace.
    @graph: A RDFLib provenance Graph.
    @doc_name: The document name.
    @start_time: The datetime that the activity started.
    @source_xml: The location of the source XML.
    @entities: A list of entities created by the script.
    @script: The name of the script that was used to generate.
    
    Returns:
    @graph: A RDFLib provenance Graph.'''
    
    if not doc_name == None:
        named_graph = URIRef(namespace + 'graph/mapping/' + str(doc_name))
        
        graph.bind('prov', 'http://www.w3.org/ns/prov#')
        prov = Namespace("http://www.w3.org/ns/prov#")
        
        graph.add((named_graph,
                   RDF.type,
                   prov['Entity']))
        
        if not start_time == None:
            graph.add((named_graph,
                       prov['generatedAtTime'],
                       Literal(str(start_time))))
        
        hash = hashlib.md5()
        hash.update(str(start_time))
        hash_date = hash.hexdigest()
        
        activity = URIRef(named_graph + '/activity/' + str(hash_date))
        
        graph.add((named_graph,
                   prov['wasGeneratedBy'],
                   activity))
        
        graph.add((activity,
                   RDF.type,
                   prov['Activity']))
        
        if not start_time == None:
            graph.add((activity,
                       RDFS.label,
                       Literal("Conversion of " + str(doc_name) + " mapping file on " + str(start_time) + ".")))
            
            graph.add((activity,
                       prov['startedAtTime'],
                       Literal(str(start_time))))
        
        if not script == None:
            graph.add((activity,
                       prov['used'],
                       URIRef("https://raw.github.com/KasperBrandt/IATI2LOD/master/IATI2LOD/src/" + str(script))))
            
        for entity in entities:
            if not entity == None:
                graph.add((activity,
                           prov['generated'],
                           namespace['mapping/' + entity]))
            
        return graph
        
    else:
        return graph