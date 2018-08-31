from flask import Flask
import json
import kube

from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)

@app.route('/create',methods = ['POST'])
def create_minecraft_server():
    app.logger.info("received request")
    resp = kube.create_minecraft_server(app.logger)
    return json.dumps(resp)

@app.route('/list',methods = ['GET'])
def list_minecraft_servers():
    app.logger.info("received request")
    resp = kube.list_services(app.logger)
    return json.dumps(resp)

@app.route('/<name>',methods = ['DELETE'])
def delete_minecraft_server(name):
    app.logger.info("received request")
    resp = kube.delete_service(name, app.logger)
    return json.dumps(resp)

#list_minecraft_servers()
#create_minecraft_server()
#delete_minecraft_server("minecraft-0000")

