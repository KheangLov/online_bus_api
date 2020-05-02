from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_restful import Api
from database.db import initialize_db
# from resources.routes import initialize_routes
from resources.errors import errors

app = Flask(__name__)
app.debug = True
app.config['JWT_SECRET_KEY'] = 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'kheang015@gmail.com'
app.config['MAIL_PASSWORD'] = 'Not4youbro'
mail = Mail(app)

from resources.routes import initialize_routes

api = Api(app)
api = Api(app, errors=errors)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config['MONGODB_SETTINGS'] = {
  'host': 'mongodb://localhost/online_bus'
}

initialize_db(app)
initialize_routes(api)

@app.cli.command()
def routes():
  'Display registered routes'
  rules = []
  for rule in app.url_map.iter_rules():
    methods = ','.join(sorted(rule.methods))
    rules.append((rule.endpoint, methods, str(rule)))

  sort_by_rule = operator.itemgetter(2)
  for endpoint, methods, rule in sorted(rules, key=sort_by_rule):
    route = '{:50s} {:25s} {}'.format(endpoint, methods, rule)
    print(route)

app.run()