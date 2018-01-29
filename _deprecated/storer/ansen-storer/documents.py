# coding: utf-8
from datetime import datetime
import base64
import re

class Project(object):
    """
    A law project
    """

    def __init__(self, origin, name, project_id):
        """
        Creates a new Project object

        :param origin: Which portal is this project from : AN or SEN
        :param name: Name of the project
        :param project_id: Identifier of this project
        """
        self.name = name
        self.project_id = str(origin.upper()) + str(project_id)
        self.creation_date = datetime.now()

    def __str__(self):
        return "Project {}: {}".format(self.project_id, self.name)


class Exam(object):
    """
    A law project exam
    """

    def __init__(self, exam_id, project_id):
        """
        Creates a new Exam object

        :param exam_id: Identifier of the exam
        :param project_id: Id of the project this exam refers to
        """

        self.exam_id = str(exam_id)
        self.project_id = str(project_id)
        self.creation_date = datetime.now()

    def __str__(self):
        return "Exam {}".format(self.exam_id)


class Amend(object):
    """
    An amend from a law project exam
    """

    def __init__(self, amend_id, url, exam_id, project_id):
        """
        Creates a new Amendement object

        :param amend_id: Identifier for this amendement
        :param url: URL from where this amendement has been pulled
        :param exam_id: Id of the exam this amendement is from
        :param project_id: Id of the project this amend refers to
        """
        self.amend_id = str(amend_id)
        self.url = url
        self.creation_date = datetime.now()
        self.exam_id = str(exam_id)
        self.project_id = str(project_id)

    def __str__(self):
        return "Amd {} from exam {} for project {}".format(self.amend_id,
                                                           self.exam_id,
                                                           self.project_id)

class Download(object):
    """
    A downloaded document
    """

    def __init__(self, url, content, amend_id):
        self.download_id = "{}.pdf".format(self.url_to_id(url))
        self.amend_id = amend_id
        self.content = content
        self.creation_date = datetime.now()

    def url_to_id(self, url):
        encoded_url = str(base64.urlsafe_b64encode(bytes(url, encoding='utf-8')))
        return re.match("b'([a-zA-Z0-9]*)={0,2}'", encoded_url).groups()[0]

    def __str__(self):
        return self.download_id