import sqlalchemy
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Numeric, func, VARCHAR, TEXT
from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property, relationship

Base = declarative_base()


class CommonColumns(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    _created = Column(DateTime, default=func.now())
    _updated = Column(DateTime, default=func.now(), onupdate=func.now())
    _etag = Column(String(40))

class logIpInfo(CommonColumns):
    __tablename__ = 'logIpInfo'
    ip = Column(Integer, nullable=False)
    coordinates = Column(Geometry('POINT'), nullable=False)
    address = Column(VARCHAR, nullable=False)
    child = relationship("logIpCnt")

class logIpCnt(CommonColumns):
    __tablename__ = 'logIpCnt'
    ipid = Column(Integer, ForeignKey('logIpInfo.id'), nullable=False)
    amount = Column(Integer, nullable=False)

class regionCity(CommonColumns):
    __tablename__ = 'regionCity'
    region = Column(VARCHAR, nullable=False)
    city = Column(VARCHAR, nullable=False)
    client = relationship("clientProfile")
    calendar_region = relationship('calendar', foreign_keys='calendar.region')
    calendar_city = relationship('calendar', foreign_keys='calendar.city')

class clientProfile(CommonColumns):
    __tablename__ = 'clientProfile'
    first_name = Column(VARCHAR, nullable=False)
    last_name = Column(VARCHAR, nullable=False)
    mid_name = Column(VARCHAR, nullable=False)
    email = Column(VARCHAR, nullable=False)
    birthday = Column(Integer, nullable=False)
    region = Column(Integer, ForeignKey('regionCity.id'), nullable=False)
    job_position = Column(VARCHAR, nullable=False)
    odnoklassniki = Column(VARCHAR, nullable=False)
    vk = Column(VARCHAR, nullable=False)
    instagram = Column(VARCHAR, nullable=False)
    facebook = Column(VARCHAR, nullable=False)
    triggers = Column(VARCHAR, nullable=False)
    auth = relationship('clientAuth')
    logIpInfo = relationship('clientLogIpInfo')
    pays = relationship('paysClient')
    messages = relationship('chatMessage')

class clientAuth(CommonColumns):
    __tablename__ = 'clientAuth'
    cid = Column(Integer, ForeignKey('clientProfile.id'), nullable=False)
    password = Column(VARCHAR, nullable=False)

class clientLogIpInfo(CommonColumns):
    __tablename__ = 'clientLogIpInfo'
    cid = Column(Integer, ForeignKey('clientProfile.id'), nullable=False)
    ip = Column(Integer, nullable=False)
    date = Column(Integer, nullable=False)
    coordinates = Column(Geometry('POINT'))

class paysClient(CommonColumns):
    __tablename__ = 'paysClient'
    date = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    cid = Column(Integer, ForeignKey('clientProfile.id'), nullable=False)
    sid = Column(Integer, ForeignKey('services.id'), nullable=False)
    sum = Column(Numeric, nullable=False)

class rubrics(CommonColumns):
    __tablename__ = 'rubrics'
    name = Column(VARCHAR, nullable=False)
    parent_rubric = Column(Integer, nullable=False)
    creation_date = Column(Integer, nullable=False)
    static_pages = relationship('staticPages')


class staticPages(CommonColumns):
    __tablename__ = 'staticPages'
    title = Column(VARCHAR, nullable=False)
    rid = Column(Integer, ForeignKey('rubrics.id'), nullable=False)
    text = Column(TEXT, nullable=False)
    creation_date = Column(Integer, nullable=False)
    directory = Column(VARCHAR, nullable=False)

class analiticRubrics(CommonColumns):
    __tablename__ = 'analiticRubrics'
    name = Column(VARCHAR, nullable=False)
    creation_date = Column(Integer, nullable=False)
    uid = Column(Integer, ForeignKey('usersCompany.id') , nullable=False)
    source_parse = relationship('sourceParse')

class sourceParse(CommonColumns):
    __tablename__ = 'sourceParse'
    name = Column(VARCHAR, nullable=False)
    link = Column(VARCHAR, nullable=False)
    rubric_type = Column(Integer, ForeignKey('analiticRubrics.id') , nullable=False)
    uid = Column(Integer, ForeignKey('usersCompany.id'), nullable=False)
    creation_date = Column(Integer, nullable=False)
    parse_log = relationship('parseLog')

class parseLog(CommonColumns):
    __tablename__ = 'parseLog'
    srcid = Column(Integer, ForeignKey('sourceParse.id'), nullable=False)
    date = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)

class chatMessage(CommonColumns):
    __tablename__ = 'chatMessage'
    chatUser = Column(Integer,ForeignKey('clientProfile.id'),
    # ForeignKey('usersCompany.id'),
     nullable=False)
    message = Column(TEXT, nullable=False)
    message_type = Column(Integer, nullable=False)
    date = Column(Integer, nullable=False)
    status = relationship('chatStatuses')
    

class chatStatuses(CommonColumns):
    __tablename__ = 'chatStatuses'
    mesid = Column(Integer, ForeignKey('chatMessage.id'), nullable=False)
    status = Column(Integer, nullable=False)

class calendar(CommonColumns):
    __tablename__ = 'calendar'
    dateTime = Column(Integer, nullable=False)
    name = Column(VARCHAR, nullable=False)
    region = Column(Integer, ForeignKey('regionCity.id'), nullable=False)
    city = Column(Integer, ForeignKey('regionCity.id'), nullable=False)
    uid = Column(Integer, ForeignKey('usersCompany.id'), nullable=False)
    date = Column(Integer, nullable=False)

class services(CommonColumns):
    __tablename__ = 'services'
    name = Column(VARCHAR, nullable=False)
    price = Column(Numeric, nullable=False)
    period = Column(Integer, nullable=False)
    uid = Column(Integer, ForeignKey('usersCompany.id'), nullable=False)
    date = Column(Integer, nullable=False)
    pays = relationship('paysClient')

class usersCompany(CommonColumns):
    __tablename__ = 'usersCompany'
    full_name = Column(VARCHAR, nullable=False)
    job_position = Column(VARCHAR, nullable=False)
    email = Column(VARCHAR, nullable=False) # Original - integer
    phone = Column(VARCHAR, nullable=False)
    analitic_rubrics = relationship('analiticRubrics')
    source_parse = relationship('sourceParse')
    # messages = relationship('chatMessage')
    calendar = relationship('calendar')
    services = relationship('services')
    usersLoginInfo = relationship('usersLoginInfo')

class usersLoginInfo(CommonColumns):
    __tablename__ = 'usersLogINInfo'
    uid = Column(Integer, ForeignKey('usersCompany.id'), nullable=False)
    login = Column(VARCHAR, nullable=False)
    password = Column(VARCHAR, nullable=False)
    block_status = Column(Integer, nullable=False)
    access_rights = Column(sqlalchemy.JSON, nullable=False)

class settings(CommonColumns):
    __tablename__ = 'settings'
    parameter_name = Column(VARCHAR, nullable=False)
    parameters = Column(sqlalchemy.JSON, nullable=False)
