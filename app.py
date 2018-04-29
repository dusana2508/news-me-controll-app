from flask import Flask, render_template, redirect, url_for, request
import requests

app = Flask (__name__)



def dovuciPodatkeSaResta():
  global odgovorSaServera
  global moguceOpcijeZaSvakoPoljeKofiguracijeJednogKlijenta
  global trenutneKonfiguracijeAplikacija

  odgovorSaServera = requests.get('http://api-news-me.ml/configurations-with-options').json()
  trenutneKonfiguracijeAplikacija = odgovorSaServera['currentConfigurations']
  moguceOpcijeZaSvakoPoljeKofiguracijeJednogKlijenta = odgovorSaServera['configurationOptions']

dovuciPodatkeSaResta()

def sacuvajTrenutnuVrednostKonfiguracijeUMemoriji (trenutnaVrednostZaDatoPoljeIzKonfikuracije):
  global trenutnaKonfiguracijskaVrednost
  trenutnaKonfiguracijskaVrednost = trenutnaVrednostZaDatoPoljeIzKonfikuracije

  # vracamo prazan string da u template-u ne bi ispisao None na mestu pozivanja funkcije jer ako funkcija nista ne vrati default=na vrednost je None
  return ''

def uzmiTrenutnuVrednostKonfiguracijeIzMemorije ():
  return trenutnaKonfiguracijskaVrednost

@app.route('/')
def homepage():
  return render_template('index.html')

@app.route('/configuration')
def getMeCofiguration():
    return render_template('configuration.html', clients = config)
 

@app.route('/configuration/<nazivKlijenta>', methods = ['GET', 'POST'])
def getMeClientCofiguration(nazivKlijenta):
  if request.method == 'POST':
    requestBody = request.form.to_dict()
    print(requestBody)
    r = requests.post('http://api-news-me.ml/configuration', data = requestBody)
    dovuciPodatkeSaResta()
  for trenutnaKonfiguracija in trenutneKonfiguracijeAplikacija:
    if trenutnaKonfiguracija['client'] == nazivKlijenta:
      # Ako je imeKlijenta u url-u isto kao vrednost polja clijent u trnutnoj konfiguraciji u for petlji
      data = {
        'konfiguracijaIzabranogKlijenta': trenutnaKonfiguracija, 
        'moguceOpcije': moguceOpcijeZaSvakoPoljeKofiguracijeJednogKlijenta,
        'postaviTrenutnuKonfiguracijskuVrednost': sacuvajTrenutnuVrednostKonfiguracijeUMemoriji,
        'uzmiTrenutnuVrednostKonfiguracijeIzMemorije': uzmiTrenutnuVrednostKonfiguracijeIzMemorije
      }
 
     
  return render_template('clientconfig.html', data = data)


@app.route('/users')
def getMeUsers():
  return render_template('users.html')

app.debug = True
app.run()