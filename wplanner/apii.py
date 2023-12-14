import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient
import logging

import arrow  # Replacement for datetime, based on moment.js
import flask
from flask import request

import api  # brevet time calculations
import config


app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY




client = MongoClient(host="todo_mongodb", port=27017)
db = client.tododb
db.tododb.delete_many({}) 
 




@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('index.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


@app.route("/_calc_times")
def _calc_times():
   
    app.logger.debug("Got a JSON request")
   

    place =  request.args.get('place', "", type = str)
    Hour =  request.args.get('Hour', 0, type = int)
    plan =  request.args.get('plan', "", type = str)
    date =  request.args.get('date', "", type = str)
    #get start date and time, and then combine with arrow into one date/moment
    #these are our boxes for date and time on host page
    #similar to getting km except string instead of float
    app.logger.debug( date + "Got a JSON request")
    #date = arrow.get(date, 'YYYY-MM-DD')
    app.logger.debug("request.args: {}".format(request.args))
    info = api.gett(place, arrow.get(date).format('YYYY-MM-DD'), Hour )
    t = str(info[0])
    w = str(info[1])
    r = str(info[2])
    
        #use arrow for our time and format properly here now so it displays in the boxes correctly
    result = {"tem": t,"wind": w,"rain": r}
    return flask.jsonify(result=result)



@app.route('/display', methods=['POST'])
def display():
    #checkpoint, opentime, closetime stored
    _items = db.tododb.find()
    items = [item for item in _items]

    #if there are no values entered then nothing to display
    #return warning message
    if (len(items) == 0): return render_template('errorWarning.html')

    #else, go to html and display checkpoint, opentime, closetime
    return render_template('display.html', items=items)


@app.route('/submiterror')
def submiterror():
    return render_template('submiterror.html')



""" @app.route('/')
def todo():
    _items = db.tododb.find()
    items = [item for item in _items]

    return render_template('todo.html', items=items)
 """

@app.route('/new', methods=['POST'])
def new():
   







    
    openInfo = request.form.getlist("place")
    closeInfo = request.form.getlist("date")
    kmInfo = request.form.getlist("plan")
    tem = request.form.getlist("t")
    wind = request.form.getlist("w")
    rain = request.form.getlist("r")


    siftedO = []
    siftedC = []
    siftedK = []
    siftedw = []
    siftedt = []
    siftedr = []

    #if the value isn't empty, then add it into the list
    for item in openInfo:
        if (str(item) != ""): siftedO.append(str(item))

    for item in closeInfo:
        if (str(item) != ""): siftedC.append(str(item))

    for item in kmInfo:
        if (str(item) != ""): siftedK.append(str(item))

    for item in wind:
        if (str(item) != ""): siftedw.append(str(item))
    
    for item in rain:
        if (str(item) != ""): siftedr.append(str(item))
    
    for item in tem:
        if (str(item) != ""): siftedt.append(str(item))

    
    length = max(len(siftedO), len(siftedC), len(siftedK) , len(siftedw),  len(siftedt),  len(siftedr))

    
    if length == 0:
        return redirect(url_for('submiterror'))
    
    
    for i in range(length):
        item_doc = {
            'openInfoDone': siftedO[i],
            'closeInfoDone': siftedC[i],
            'kmInfoDone': siftedK[i],
            'tInfoDone': siftedt[i],
            'wInfoDone': siftedw[i],
            'rInfoDone': siftedr[i]
        }
        db.tododb.insert_one(item_doc)

   
    _items = db.tododb.find()
    items = [item for item in _items]

    #if there are no values entered then nothing to display
    #return warning message
    if (len(items) == 0): return render_template('errorWarning.html')

    #else, go to html and display checkpoint, opentime, closetime
    return render_template('index.html', items=items)











    


app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
