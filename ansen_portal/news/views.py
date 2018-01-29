from django.shortcuts import render


# Create your views here.
def newslist(request):
    return render(request, 'news/list.html',
                  {'tab_state': {'news': '"active"',
                                 'recherche': '',
                                 'alertes': '',
                                 'profil': ''},
                   'news_items': [{'title': 'Lancement',
                                    'date': 'Aujourd\'hui',
                                    'body': 'Ceci est le texte de Martin Luther King'}]})
