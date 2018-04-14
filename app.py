from flask import Flask, render_template, redirect, url_for

app = Flask (__name__)

@app.route('/')
def homepage():
  return render_template('index.html')

@app.route('/configuration/<client>')
def getMeCofiguration(client):
  return render_template('configuration.html', name = client)

@app.route('/configuration')
def configurationWithOutClient():
    return render_template('configuration.html')

@app.route('/users')
def getMeUsers():
  return render_template('users.html')

app.run()