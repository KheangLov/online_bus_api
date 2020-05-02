from resources.bus import BusApi, BusesApi
from resources.auth import SignupApi, LoginApi
from resources.reset_password import ForgotPassword, ResetPassword

def initialize_routes(api):
  api.add_resource(BusesApi, '/api/buses')
  api.add_resource(BusApi, '/api/buses/<id>')

  api.add_resource(SignupApi, '/api/auth/register')
  api.add_resource(LoginApi, '/api/auth/login')

  api.add_resource(ForgotPassword, '/api/auth/forgot')
  api.add_resource(ResetPassword, '/api/auth/reset')