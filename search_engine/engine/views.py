from django.shortcuts import render
import rdflib

# Create your views here.

def search(request):
    
    g = rdflib.Graph()
    g.parse("music.rdf")

    for s,p,o in g:
    	print(s,p,o)

    data = {
    'list' : ["Album", "Artiste", "Chanson", "Genre","Groupe", "Vente", "Interprète", "Compositeur", "Auteur",  "Musique Africo Américaines", "Rock",  "Variétés Internationales",  "Or", "Diamant", "Platinium", "1-Platinium", "2-Platinium", "3-Platinium"],
  	}
    return render(request, 'index.html', data)