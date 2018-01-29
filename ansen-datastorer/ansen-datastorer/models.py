#!/usr/bin/env python
# coding: utf-8
# __author__ = 'Benjamin'

from datetime import datetime
from sqlalchemy import Column, Boolean, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Amendement(Base):
    __tablename__ = 'amendements'
    id = Column(Integer, primary_key=True)
    organisme =     Column(String)      # AN or SEN
    project_id =    Column(String)
    project_cat =   Column(String)
    project_name =  Column(String)
    exam_id =       Column(String)
    exam_name =     Column(String)
    amd_id =        Column(String)
    s_type =        Column(String)
    url =           Column(String)
    n_article =     Column(String)
    sort =          Column(String)
    signataires =   Column(String)
    downloaded =    Column(Boolean, default=False)
    # filename
    # filepath
    creation_date = Column(DateTime, default=datetime.now())
