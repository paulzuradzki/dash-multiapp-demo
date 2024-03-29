import dash
import flask

# for styling / CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
    'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
    'rel': 'stylesheet',
    'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
    'crossorigin': 'anonymous'
    }]

server = flask.Flask(__name__) # define flask app.server

app = dash.Dash(__name__, 
                suppress_callback_exceptions=True, 
                external_stylesheets=external_stylesheets, server=server)
