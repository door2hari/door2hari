import flask
import speech_recognition as sr
from flask import Flask,render_template,request,redirect,url_for,session,jsonify
from main import Processing,sums,all
app = Flask(__name__)
app.secret_key = 'chumma'

@app.route('/',methods=['POST','GET'])
def home():
    try:
        return render_template("index.html")
    except:
        return "Please, give more detailed input"

@app.route('/choose',methods=['POST','GET'])
def predicts_cutoff():
    input = request.form['college']
    try:
        No_of_matches = Processing(input)
        return render_template("output.html", numbers = No_of_matches)
    except:
        return "Please, give more detailed input"

@app.route('/laws',methods=['POST','GET'])
def show_laws():
    try:
       matches = all()
       return render_template("laws.html", matches = matches, summary = summary)
    except ModuleNotFoundError:
       return "Unable to find module."

@app.route('/summary',methods=['POST','GET'])
def summary():
    try:
       data = request.get_json().get('data')
       print(data)
       summary = sums(data)
       session['des'] = data
       session['summ'] = summary
       return redirect(url_for('final'))
    except ModuleNotFoundError:
       return "Unable to find module."

@app.route('/final',methods=['POST','GET'])
def final():
    try:
        data = session.get('des')
        summary = session.get('summ')
        return render_template("summary.html", description = data, summary=summary)
    except ModuleNotFoundError:
       return "Unable to find module."

if __name__ == '__main__':
   app.run(host="localhost",debug = True)
