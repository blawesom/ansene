#!/usr/bin/env python
# coding: utf-8
# __author__ = 'Benjamin'


from models import Amendement
import tools


def get_docs(session, orga, model=Amendement, project_id=None, exam_id=None, amd_id=None):
    if orga in ['AN', 'SEN']:
        if amd_id:
            amd = session.query(model).filter(model.amd_id == amd_id).first()
            amdict = amd.__dict__
            # Check if normal ORM behaviour
            del amdict['_sa_instance_state']
            return amdict

        elif exam_id:
            amd_list = []
            for amd in session.query(model).filter(model.organisme == orga,
                                                   model.project_id == project_id,
                                                   model.exam_id == exam_id):
                amd_list.append(amd.amd_id)
            return amd_list

        elif project_id:
            exam_list = []
            for exam_id in set([r.exam_id for r in session.query(model).filter(model.organisme == orga,
                                                                           model.project_id == project_id)]):
                nb_amd = session.query(model).filter(model.project_id == project_id,
                                                     model.exam_id == exam_id).count()
                exam_list.append(       {'project_id': project_id,
                                         'exam_id': exam_id,
                                         'nb_amd':  nb_amd}          )
            return exam_list
        # Request /an or /sen
        else:
            return set([r.project_id for r in session.query(model).filter(model.organisme == orga)]),  \
                   set([r.project_cat for r in session.query(model).filter(model.organisme == orga)]), \
                   set([r.project_name for r in session.query(model).filter(model.organisme == orga)]),
    # Orga is not known
    else:
        return {}


def add_doc(session, data, model=Amendement):
    obj, created = get_or_create(session, model, **data)
    return created


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        try:
            session.add(instance)
            instance.downloaded = tools.download_amd(instance)
            if instance.downloaded:
                session.commit()
                return instance, True
            else:
                session.rollback()
            return None, False
        except:
            session.rollback()
            return None, False
