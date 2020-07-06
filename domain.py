import sqlalchemy
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Numeric, func, VARCHAR, TEXT
from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property, relationship

Base = declarative_base()

# Basic columns for tables 
class CommonColumns(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # SQLAlchemy is not working properly without these fields
    _created = Column(DateTime, default=func.now())
    _updated = Column(DateTime, default=func.now(), onupdate=func.now())
    _etag = Column(String(40))

# logIpInfo with relationship "logIpCnt"

class logIpInfo(CommonColumns):
    __tablename__ = 'logIpInfo' #tablename in db
    ip = Column(Integer, nullable=False) #Create column with datatype Integer NOT NULL
    coordinates = Column(Geometry('POINT'), nullable=False) #SQLAlchemy has no datatype "point"
    address = Column(VARCHAR, nullable=False)
    child = relationship("logIpCnt") # That relationship can be moved to child class 

# logIpCnt with "logIpInfo" foreign key

class logIpCnt(CommonColumns):
    __tablename__ = 'logIpCnt'
    ipid = Column(Integer, ForeignKey('logIpInfo.id'), nullable=False)
    amount = Column(Integer, nullable=False)

# regionCity with relationships "clientProfile", "calendar"

class regionCity(CommonColumns):
    __tablename__ = 'regionCity'
    region = Column(VARCHAR, nullable=False)
    city = Column(VARCHAR, nullable=False)
    client = relationship("clientProfile") # That relationship can be moved to child class
    calendar_region = relationship('calendar', foreign_keys='calendar.region') # That relationship can be moved to child class
    calendar_city = relationship('calendar', foreign_keys='calendar.city') # That relationship can be moved to child class

# clientProfile with "regionCity" foreign key and relationships "clientAuth", "clientLogIpInfo", "paysClient", "chatMessage"

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
    auth = relationship('clientAuth') # That relationship can be moved to child classv
    logIpInfo = relationship('clientLogIpInfo') # That relationship can be moved to child class
    pays = relationship('paysClient') # That relationship can be moved to child class
    messages = relationship('chatMessage') # That relationship can be moved to child class

# clientAuth with "clientProfile" foreign key "clientProfile"

class clientAuth(CommonColumns):
    __tablename__ = 'clientAuth'
    cid = Column(Integer, ForeignKey('clientProfile.id'), nullable=False)
    password = Column(VARCHAR, nullable=False)

# clientLogIpInfo with "clientProfile" foreign key

class clientLogIpInfo(CommonColumns):
    __tablename__ = 'clientLogIpInfo'
    cid = Column(Integer, ForeignKey('clientProfile.id'), nullable=False)
    ip = Column(Integer, nullable=False)
    date = Column(Integer, nullable=False)
    coordinates = Column(Geometry('POINT')) # SQLAlchemy has no point type

# clientProfile with "clientProfile" and "services" foreign keys 

class paysClient(CommonColumns):
    __tablename__ = 'paysClient'
    date = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    cid = Column(Integer, ForeignKey('clientProfile.id'), nullable=False)
    sid = Column(Integer, ForeignKey('services.id'), nullable=False)
    sum = Column(Numeric, nullable=False)

#rubrics with relationship "staticPages"

class rubrics(CommonColumns):
    __tablename__ = 'rubrics'
    name = Column(VARCHAR, nullable=False)
    parent_rubric = Column(Integer, nullable=False)
    creation_date = Column(Integer, nullable=False)
    static_pages = relationship('staticPages') # That relationship can be moved to child class

#staticPages with "rubrics" foreign key

class staticPages(CommonColumns):
    __tablename__ = 'staticPages'
    title = Column(VARCHAR, nullable=False)
    rid = Column(Integer, ForeignKey('rubrics.id'), nullable=False)
    text = Column(TEXT, nullable=False)
    creation_date = Column(Integer, nullable=False)
    directory = Column(VARCHAR, nullable=False)

# analiticRubrics with relationship "sourceParse" and "usersCompany" foreign key

class analiticRubrics(CommonColumns):
    __tablename__ = 'analiticRubrics'
    name = Column(VARCHAR, nullable=False)
    creation_date = Column(Integer, nullable=False)
    uid = Column(Integer, ForeignKey('usersCompany.id') , nullable=False)
    source_parse = relationship('sourceParse') # That relationship can be moved to child class

# sourceParse with relationship "parseLog" and "analiticRubrics", "usersCompany" foreign key

class sourceParse(CommonColumns):
    __tablename__ = 'sourceParse'
    name = Column(VARCHAR, nullable=False)
    link = Column(VARCHAR, nullable=False)
    rubric_type = Column(Integer, ForeignKey('analiticRubrics.id') , nullable=False)
    uid = Column(Integer, ForeignKey('usersCompany.id'), nullable=False)
    creation_date = Column(Integer, nullable=False)
    parse_log = relationship('parseLog') # That relationship can be moved to child class

# parseLog with "sourceParse" foreign key

class parseLog(CommonColumns):
    __tablename__ = 'parseLog'
    srcid = Column(Integer, ForeignKey('sourceParse.id'), nullable=False)
    date = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)

# chatMessage with relationship "chatStatuses" and "clientProfile" foreign key
# foreign key "usersCompany" WIP

class chatMessage(CommonColumns):
    __tablename__ = 'chatMessage'
    chatUser = Column(Integer,ForeignKey('clientProfile.id'),
    # ForeignKey('usersCompany.id'),
     nullable=False)
    message = Column(TEXT, nullable=False)
    message_type = Column(Integer, nullable=False)
    date = Column(Integer, nullable=False)
    status = relationship('chatStatuses') # That relationship can be moved to child class
    
# chatStatuses with "chatMessage" foreign key

class chatStatuses(CommonColumns):
    __tablename__ = 'chatStatuses'
    mesid = Column(Integer, ForeignKey('chatMessage.id'), nullable=False)
    status = Column(Integer, nullable=False)

# calendar with "regionCity" x 2 , "usersCompany" foreign keys 

class calendar(CommonColumns):
    __tablename__ = 'calendar'
    dateTime = Column(Integer, nullable=False)
    name = Column(VARCHAR, nullable=False)
    region = Column(Integer, ForeignKey('regionCity.id'), nullable=False)
    city = Column(Integer, ForeignKey('regionCity.id'), nullable=False)
    uid = Column(Integer, ForeignKey('usersCompany.id'), nullable=False)
    date = Column(Integer, nullable=False)

#services with relationship "paysClient"  and "usersCompany" foreign key 

class services(CommonColumns):
    __tablename__ = 'services'
    name = Column(VARCHAR, nullable=False)
    price = Column(Numeric, nullable=False)
    period = Column(Integer, nullable=False)
    uid = Column(Integer, ForeignKey('usersCompany.id'), nullable=False)
    date = Column(Integer, nullable=False)
    pays = relationship('paysClient')


# usersCompany with relationships
#"analiticRubrics"
#"sourceParse"
#"chatMessage" WIP
#"calendar"
#"services"
#"usersLoginInfo"


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

# usersLoginInfo with "usersCompany" foreign key

class usersLoginInfo(CommonColumns):
    __tablename__ = 'usersLogINInfo'
    uid = Column(Integer, ForeignKey('usersCompany.id'), nullable=False)
    login = Column(VARCHAR, nullable=False)
    password = Column(VARCHAR, nullable=False)
    block_status = Column(Integer, nullable=False)
    access_rights = Column(sqlalchemy.JSON, nullable=False)

# settings without connections

class settings(CommonColumns):
    __tablename__ = 'settings'
    parameter_name = Column(VARCHAR, nullable=False)
    parameters = Column(sqlalchemy.JSON, nullable=False)
