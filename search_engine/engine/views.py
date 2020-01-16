from django.shortcuts import render
import rdflib

# Create your views here.
def filtering(variable): 
    to_filter = ['type'] 
    if (variable in to_filter): 
        return False
    else: 
        return True

def search(request , criteria, query ):

	g = rdflib.Graph()
	g.parse("music.rdf")

	res_artists = g.query("""
		PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
		PREFIX owl: <http://www.w3.org/2002/07/owl#>
		PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
		PREFIX : <http://www.semanticweb.org/NOM/ontologies/2018/musicontology#>

		SELECT DISTINCT ?s
		WHERE
		{ ?s a :Artiste }
		""")
	artists = [row[0].split('#')[1] for row in res_artists]
	artists = filter(filtering,artists)
	new_artists = []
	for item in artists:
		tmp = item.split("_")
		if len(tmp) > 1:
			mstr = " ".join(tmp)	
		else:
			mstr = tmp[0]
		new_artists.append(mstr)


	res_props = g.query("""
		PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
		PREFIX owl: <http://www.w3.org/2002/07/owl#>
		PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
		PREFIX : <http://www.semanticweb.org/NOM/ontologies/2018/musicontology#>

		SELECT DISTINCT ?property
		WHERE
		{ ?s ?property ?o .
		 ?s a :Chanson . }
		""")
	props = [row[0].split('#')[1] for row in res_props]
	props = filter(filtering,props)

	if not ( criteria == None or query == None ):

		if ' ' in query:
			query = query.replace(' ','_')
		
		qres = g.query("""
			PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
			PREFIX owl: <http://www.w3.org/2002/07/owl#>
			PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
			PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
			PREFIX : <http://www.semanticweb.org/NOM/ontologies/2018/musicontology#>
			SELECT ?album
			WHERE {  ?chanson :""" + criteria +""" :""" + query +""" .?album :contient ?chanson }	
			""")

		for row in qres.result:
			print(row[0].split('#')[1])
		#print(g.predicates("<http://www.semanticweb.org/NOM/ontologies/2018/musicontology#Album>"))

	data = { 
	'list' : new_artists, 
	'criterias' : props, 
	'albums' : [ ('album1','genre1','artist1'), ('album2','genre2','artist2') ],
			}

	return render(request, 'index.html', data)
