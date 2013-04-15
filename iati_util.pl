:- module(iati_util,
	  [ load_all_data/0
	  ]).

% user:file_search_path(data,       './IATI2LOD/Data/').
% :- rdf_register_ns(iati, 'http://purl.org/collections/iati/').

:- use_module([	library(semweb/rdf_cache),
		library(semweb/rdf_db),
		library(semweb/rdf_library)
	      ]).

% Parameter: Basename for graph URI
ns('http://purl.org/collections/iati/').

% Parameter: Data files path
datapath('./git/IATI2LOD/IATI2LOD/Data/').


% this loads all the data in separate graphs named
% NS + Filename - '.ttl'

load_all_data:-
	get_all_files(ListOfFiles),
	load_all_files(ListOfFiles).

get_all_files(L):-
	datapath(P),
	atomic_list_concat([P,'*.ttl'],FN),
	expand_file_name(FN,L).

load_all_files([]).
load_all_files([File|T]):-
	file_base_name(File,FBN),
	atom_concat(ID,'.ttl',FBN),
	ns(NS),
	atom_concat(NS,ID,GraphName),
	rdf_load(File,[graph(GraphName)]),
	writef('loaded graph %w\n', [GraphName]), flush,
	load_all_files(T).
