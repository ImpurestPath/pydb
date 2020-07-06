from eve import Eve

from eve_sqlalchemy import SQL
from domain import Base

from eve_sqlalchemy.validation import ValidatorSQL

app = Eve(validator=ValidatorSQL, data=SQL)
db = app.data.driver
Base.metadata.bind = db.engine
db.Model = Base
db.create_all()
# db.create_all()



app.run(debug=True, port=9003)