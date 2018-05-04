from flask import Flask, render_template, redirect, url_for, request
import requests

app = Flask (__name__)



def dovuciPodatkeSaResta():
  global odgovorSaServera
  global moguceOpcijeZaSvakoPoljeKofiguracijeJednogKlijenta
  global trenutneKonfiguracijeAplikacija
  global sviKorisniciSaResta
  odgovorSaServera = requests.get('http://api-news-me.ml/configurations-with-options').json()
  trenutneKonfiguracijeAplikacija = odgovorSaServera['currentConfigurations']
  moguceOpcijeZaSvakoPoljeKofiguracijeJednogKlijenta = odgovorSaServera['configurationOptions']

  sviKorisniciSaResta = requests.get('http://api-news-me.ml/controll-app-get-all-users').json()

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

@app.route('/configurations')
def getMeCofiguration():
    return render_template('configuration.html', clients = trenutneKonfiguracijeAplikacija)


@app.route('/configurations/<nazivKlijenta>', methods = ['GET', 'POST'])
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
def listaKorisnika():
  return render_template('korisnici.html', lista = sviKorisniciSaResta)

app.debug = True
app.run()