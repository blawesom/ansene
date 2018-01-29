# coding: utf-8
import pymongo
import werkzeug
import inspect

from settings import MONGODB
import documents


class NotFoundError(IndexError):
    """
    Exception when a requested document wasn't found
    """

    def __init__(self, document_type, document_id):
        self.document_id = document_id
        self.document_type = document_type

    def __str__(self):
        return "The {} {} wasn't found and might not exist".format(self.document_type,
                                                                   self.document_id)


class NotAValidDocumentType(AttributeError):
    """
    Exception when trying to create an object from an inexistant document type
    """

    def __init__(self, document_type):
        self.document_type = document_type

    def __str__(self):
        return "{} is not a valid Document type".format(self.document_type)


class MongoConnection(object):

    def __init__(self, endpoint=MONGODB['endpoint'], port=MONGODB['port'], database='ansen', module=documents):
        self.conn = pymongo.MongoClient("mongodb://{}:{}".format(endpoint, port))
        self.database = self.conn[database]
        self.collections = []
        self.get_valid_collections(module)
        self.init_db_constraints(module)

    def init_db_constraints(self, module):
        for collection in self.collections:
            self.database[collection].create_index('{}_id'.format(collection.lower()), unique=True)

    def get_valid_collections(self, module):
        self.collections = [str(cl[0]).lower() for cl in inspect.getmembers(module, inspect.isclass)
                            if cl[1].__module__ == module.__name__]

    def insert_document(self, document):
        """
        Insert a document into the database"
        """

        collection = document.__class__.__name__.lower()
        ids = {k.split('_')[0]: v for k, v in document.__dict__.items()
               if k.endswith('_id')
               if not k.startswith(collection)}
        for k, v in ids.items():
            if not self.document_exists(k, v):
                raise NotFoundError(k, v)
        try:
            return self.database[collection].insert_one(document.__dict__)
        except pymongo.errors.DuplicateKeyError as err:
            raise werkzeug.exceptions.Conflict()

    def get_all_documents(self, document_type, filter=None):
        return list(self.database[document_type].find(filter=filter,
                                                      projection={'_id': False}))

    def get_document(self, document_type, document_id):
        """
        Retrieves a document from the database

        :param document_type: the type of document to retrieve
        :param document_id:  the id of the document to retrieve
        :param database: which database to retrieve the document from
        :return: a list of documents
        """

        doc = self.database[document_type].find_one({'{}_id'.format(document_type): document_id},
                                                    projection={'_id': False})
        if not doc:
            raise NotFoundError(document_type, document_id)
        return doc

    def get_or_create_document(self, document_type, document_id, data=None):
        """
        Get a document from a database. It the document doesn't exist, creates it

        :param document_type: the type of document to retrieve
        :param document_id: the id of the document to retreve
        :param data: a dict containing necessary data to create object
        :param database: which database to retrieve the document from
        :return: a document
        """

        try:
            doc = self.get_document(document_type, document_id)
        except NotFoundError:
            document = generate_document_object(document_type, data)
            result = self.insert_document(document).inserted_id
            doc = self.database[document_type].find_one({"_id": result})
        return doc

    def update_document(self, document_type, document_id, data):
        to_modify = {'{}_id'.format(document_type): document_id}
        modification = {'$addToSet': {'download_list': data['download_list']}}
        doc = self.database[document_type].find_one_and_update(to_modify,
                                                               modification,
                                                               projection={'_id': False})
        return doc

    def document_exists(self, document_type, document_id):
        try:
            self.get_document(document_type, document_id)
            return True
        except NotFoundError:
            return False

    def __str__(self):
        return self.conn.__str__()


def generate_document_object(document_type, data):
    """
    Generates a document of any valid Document types

    :param document_type: which type of document to create
    :param data: the data to build the object
    :return: a <documents.document_type> object
    """

    try:
        doc_constructor = getattr(documents, document_type.capitalize())
    except AttributeError:
        raise NotAValidDocumentType(document_type)
    init_vars = [var for var in doc_constructor.__init__.__code__.co_varnames if var != 'self']
    document = doc_constructor(**{attr: data[attr] for attr in init_vars})
    return document
