#!/usr/bin/env python
# coding: utf-8
# __author__ = 'Benjamin'


from mailin import Mailin


def send_mail(link, dest_mail, dest_name):
    '''
    Gère l'envoie du mail en template et du lien pour le téléchargement du fichier

    :param link:
    :type link: str
    :param dest_mail:
    :param dest_name:
    :return:
    :rtype:
    '''

    # Instantiate the client\
    m = Mailin(base_url="https://api.sendinblue.com/v2.0", api_key=config().get('mailer','apikey'))

    # Define the campaign settings\
    data = {"subject": "Votre recherche sur Ansène.eu",
            "to": { dest_mail : dest_name },
            "from": ["veille@ansene.eu", "Ansène!"],
            "html": "Vous pouvez dès à présent télécharger le résultat de votre recherche ici: {0}".format(link)
            }

    # curl - H    'api-key:S8LaGpt4HUxP5XOQ' - X
    # POST - d    '{"to":{"blaplane@gmail.com":"Client"}, "from":["veille@ansene.eu","Ansene"],' \
    #             ' "subject":"First email", "html":"This is the <h1>HTML</h1>"}'\
    #             'https://api.sendinblue.com/v2.0/email'

    # Make the call to the client\
    result = m.send_mail(data)

    return result