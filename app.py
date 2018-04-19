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
 

@app.route('/configuration')
def configurationWithOutClient():
    return render_template('configuration.html')

@app.route('/users')
def getMeUsers():
  return render_template('users.html')

app.run()