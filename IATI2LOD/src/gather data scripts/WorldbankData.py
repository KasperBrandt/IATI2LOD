## By Kasper Brandt
## Last updated on 26-05-2013

import os, sys, datetime, urllib, urllib2, AddProvenance
import xml.etree.ElementTree as ET
from rdflib import Namespace, Graph, Literal, RDF

# Settings
worldbank_folder = "/media/Acer/School/IATI-data/dataset/WorldBank/"
worldbank_file = "/media/Acer/School/IATI-data/mappings/WorldBank/worldbank-countries.ttl"
indicator_file = "/media/Acer/School/IATI-data/dataset/WorldBank/worldbank-indicator.ttl"

indicator_data = Graph()
indicator_data.bind('wbld-dataset', "http://worldbank.270a.info/dataset/")
indicator_data.bind('skos', "http://www.w3.org/2008/05/skos#")
indicator_data.bind('dct', "http://purl.org/dc/terms/")
indicator_data.bind('cube', "http://purl.org/linked-data/cube#")

Iati = Namespace("http://purl.org/collections/iati/")
IatiC = Namespace(Iati + "codelist/country/")
WBD = Namespace("http://worldbank.270a.info/dataset/")
WBI = Namespace("http://worldbank.270a.info/classification/indicator/")
WBC = Namespace("http://worldbank.270a.info/classification/country/")
WBP = Namespace("http://worldbank.270a.info/property/")
SKOS = Namespace("http://www.w3.org/2008/05/skos#")
DCT = Namespace("http://purl.org/dc/terms/")
CUBE = Namespace("http://purl.org/linked-data/cube#")
MEASURE = Namespace("http://purl.org/linked-data/sdmx/2009/measure#")
DIMENSION = Namespace("http://purl.org/linked-data/sdmx/2009/dimension#")
YEAR = Namespace("http://reference.data.gov.uk/id/year/")

if not os.path.isdir(worldbank_folder):
    os.makedirs(worldbank_folder)

# Provenance settings
sources = []
start_time = datetime.datetime.now()

# World bank indicators selection
indicators = ['AG.LND.TOTL.K2',
              'AG.PRD.FOOD.XD',
              'BN.CAB.XOKA.CD',
              'DT.ODA.ODAT.GN.ZS',
              'DT.ODA.ODAT.PC.ZS',
              'DT.ODA.ALLD.CD',
              'DT.ODA.ODAT.CD',
              'ER.H2O.FWTL.K3',
              'ER.H2O.INTR.PC',
              'ER.H2O.INTR.K3',
              'FI.RES.TOTL.CD',
              'GC.BAL.CASH.GD.ZS',
              'GC.TAX.TOTL.GD.ZS',
              'IC.LGL.CRED.XQ',
              'IC.TAX.PAYM',
              'IC.TAX.TOTL.CP.ZS',
              'IT.CEL.SETS.P2',
              'IT.NET.USER.P2',
              'IT.NET.SECR.P6',
              'MS.MIL.XPND.ZS',
              'MS.MIL.XPND.GD.ZS',
              'NY.GDP.MKTP.CD',
              'NY.GNP.PCAP.CD',
              'SH.DYN.MORT',
              'SH.STA.ACSN',
              'SH.STA.BRTC.ZS',
              'SH.DYN.AIDS.ZS',
              'SH.HIV.1524.FE.ZS',
              'SH.HIV.1524.MA.ZS',
              'SL.TLF.TOTL.IN',
              'SL.TLF.CACT.FE.ZS',
              'SL.TLF.CACT.MA.ZS',
              'SL.TLF.CACT.ZS',
              'SL.UEM.TOTL.FE.ZS',
              'SL.UEM.TOTL.MA.ZS',
              'SL.UEM.TOTL.ZS',
              'SM.POP.REFG.OR',
              'SM.POP.REFG',
              'SP.DYN.LE00.FE.IN',
              'SP.DYN.LE00.MA.IN',
              'SP.DYN.CBRT.IN',
              'SP.DYN.CONU.ZS',
              'SP.DYN.CDRT.IN',
              'SP.DYN.LE00.IN',
              'SP.MTR.1519.ZS',
              'SP.POP.GROW',
              'SP.POP.TOTL',
              'SP.RUR.TOTL',
              'SP.RUR.TOTL.ZS',
              'SP.URB.TOTL',
              'SP.URB.TOTL.IN.ZS']


indicator_webservice = "http://api.worldbank.org/indicators/"
errors = 0

for indicator in indicators:
    print "Processing " + indicator + "..."
    
    data = Graph()
    data.bind('iati-country', "http://purl.org/collections/iati/codelist/country/")
    data.bind('wbld-country', "http://worldbank.270a.info/classification/country/")
    data.bind('wb-property', "http://worldbank.270a.info/property/")
    data.bind('cube', "http://purl.org/linked-data/cube#")
    data.bind('measure', "http://purl.org/linked-data/sdmx/2009/measure#")
    data.bind('dimension', "http://purl.org/linked-data/sdmx/2009/dimension#")
    
    url = indicator_webservice + indicator
    sources.append(url)
    
    response = urllib2.urlopen(url).read()
    xml = ET.fromstring(response)
    
    for indicator_node in xml:
        name = indicator_node.find('{http://www.worldbank.org}name').text
        comment = indicator_node.find('{http://www.worldbank.org}sourceNote').text
        
        indicator_data.add((WBD[indicator],
                        DCT['identifier'],
                        Literal(indicator)))
        
        indicator_data.add((WBD[indicator],
                        RDF.type,
                        CUBE['DataSet']))
        
        if not name == None:
            indicator_data.add((WBD[indicator],
                            DCT['title'],
                            Literal(str(name))))
        
        if not comment == None:
            indicator_data.add((WBD[indicator],
                            SKOS['definition'],
                            Literal(str(comment))))
    
    # Get the countries from WorldBank file
    with open(worldbank_file, 'r') as f:
        for line in f:
            
            if "owl:sameAs" in line:
                found_data = False
                
                line_list = line.split()
                iati_code = line_list[2].rsplit(":",1)[1]
                worldbank_code = line_list[2].rsplit(":",1)[1]
                
                webservice = "http://api.worldbank.org/countries/" + str(worldbank_code) + "/indicators/" + indicator + "?"
                
                # Webservice settings
                per_page = 500
                page_count = 0
                pages_count = 1
                page = 1
                connected = True
                
                print "Retrieving " + indicator + " for " + worldbank_code + "..."
                
                while page_count < pages_count:
                
                    params = dict([('per_page', per_page),
                                   ('page', page)])
                    
                    params_encoded = urllib.urlencode(params)
                    url = webservice + params_encoded
                    
                    try:
                        response = urllib2.urlopen(url).read()
                    except urllib2.HTTPError as e:
                        print "Connection failed..."
                        errors += 1
                        break
                    except:
                        print "Something failed..."
                        errors += 1
                        break
                        
                    xml = ET.fromstring(response)
                    
                    for data_node in xml:
                        date = data_node.find('{http://www.worldbank.org}date').text
                        value = data_node.find('{http://www.worldbank.org}value').text
        
                        if (not date == None) and (not value == None):
                            observation_uri = WBD['world-bank-indicators/' + indicator + '/' + worldbank_code + '/' + str(date)]
                            
                            sources.append(observation_uri)
                            
                            data.add((observation_uri,
                                      RDF.type,
                                      CUBE['Observation']))
                            
                            data.add((observation_uri,
                                      CUBE['dataSet'],
                                      WBD[indicator]))
                            
                            data.add((observation_uri,
                                      WBP['indicator'],
                                      WBI[indicator]))                            
                            
                            data.add((observation_uri,
                                      MEASURE['obsValue'],
                                      Literal(value)))
                            
                            data.add((observation_uri,
                                      DIMENSION['refArea'],
                                      WBC[worldbank_code]))
                            
                            data.add((observation_uri,
                                      DIMENSION['refArea'],
                                      IatiC[iati_code]))
                            
                            data.add((observation_uri,
                                      DIMENSION['refPeriod'],
                                      Literal(date)))
                            
                            data.add((observation_uri,
                                      DIMENSION['refPeriod'],
                                      YEAR[date]))
                        
                    pages_count = int(xml.attrib['pages'])    
                    page_count += 1
                           
    print "Adding to file..."
    print
    
    turtle = data.serialize(format='turtle')
    with open(worldbank_folder + 'worldbank-'+ indicator +'.ttl', 'w') as turtle_file:
        turtle_file.write(turtle)
    
    
    
print "Adding indicator data to file..."
print

turtle = indicator_data.serialize(format='turtle')
with open(worldbank_folder + 'worldbank-indicators.ttl', 'w') as turtle_file:
    turtle_file.write(turtle)

# Add provenance
provenance = Graph()

provenance = AddProvenance.addProv(Iati,
                                   provenance,
                                   'WorldBank',
                                   start_time,
                                   sources,
                                   ['WorldBank'],
                                   "gather%20data%20scripts/WorldbankData.py")

provenance_turtle = provenance.serialize(format='turtle')

with open(worldbank_folder + 'provenance-worldbank.ttl', 'w') as turtle_file_prov:
    turtle_file_prov.write(provenance_turtle)
    
print "Done! " + str(errors) + " errors."
                
    