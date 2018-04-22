from flask import Flask, render_template, redirect, url_for
import requests

app = Flask (__name__)

configOption = requests.get('http://api-news-me.ml/configurations-with-options').json()

config = configOption['currentConfigurations']
configurationOptions = configOption['configurationOptions']

@app.route('/')
def homepage():
  return render_template('index.html')

@app.route('/configuration')
def getMeCofiguration():
    return render_template('configuration.html', clients = config)
 

@app.route('/configuration/<client>')
def getMeClientCofiguration(client):
  for typeClient in config:
    if typeClient['client'] == client:
      return render_template('clientconfig.html', oneClientConfig = typeClient)

  return 'ok'

@app.route('/users')
def getMeUsers():
  return render_template('users.html')

app.run()