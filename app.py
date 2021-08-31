import dash
import flask

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


server = flask.Flask(__name__) # define flask app.server
app = dash.Dash(__name__, 
                suppress_callback_exceptions=True, 
                external_stylesheets=external_stylesheets, 
                server=server)
# server = app.server