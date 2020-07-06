from eve_sqlalchemy.config import DomainConfig, ResourceConfig
from eve_sqlalchemy.examples.simple.tables import Invoices, People
import domain
import d2
import os
DEBUG = True
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'postgresql://testuser:testuser@localhost:5432/test'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False
RESOURCE_METHODS = ['GET', 'POST']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

# The following two lines will output the SQL statements executed by
# SQLAlchemy. This is useful while debugging and in development, but is turned
# off by default.
# --------
# SQLALCHEMY_ECHO = True
# SQLALCHEMY_RECORD_QUERIES = True

# The default schema is generated using DomainConfig:
DOMAIN = DomainConfig({
    'logIpInfo': ResourceConfig(domain.logIpInfo),
    'logIpCnt': ResourceConfig(domain.logIpCnt),
    'regionCity': ResourceConfig(domain.regionCity),
    'clientProfile': ResourceConfig(domain.clientProfile),
    'clientAuth': ResourceConfig(domain.clientAuth),
    'clientLogIpInfo': ResourceConfig(domain.clientLogIpInfo),
    'paysClient': ResourceConfig(domain.paysClient),
    'rubrics': ResourceConfig(domain.rubrics),
    'staticPages': ResourceConfig(domain.staticPages),
    'analiticRubrics': ResourceConfig(domain.analiticRubrics),
    'sourceParse': ResourceConfig(domain.sourceParse),
    'parseLog': ResourceConfig(domain.parseLog),
    'chatMessage': ResourceConfig(domain.chatMessage),
    'chatStatuses': ResourceConfig(domain.chatStatuses),
    'calendar': ResourceConfig(domain.calendar),
    'services': ResourceConfig(domain.services),
    'usersCompany': ResourceConfig(domain.usersCompany),
    'usersLoginInfo': ResourceConfig(domain.usersLoginInfo),
    'settings': ResourceConfig(domain.settings)
    # 'aaa': ResourceConfig(d2.aaa)
}).render()