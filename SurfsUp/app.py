import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#connect to database
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

#reflect existing database into new model
Base = automap_base()
#reflect the table
Base.prepare(engine, reflect=True)

#save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

###########################
#Flask Setup
###########################

app = Flask(__name__)

###########################
#Flask Routes
###########################

@app.route("/")
def home():
    return (
        f"Welcome to Climate API:<br/>"
        f"Available Routes<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"

    )

######################################
@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-23").\
        filter(Measurement.prcp != "None").\
        all()

    prec = {date: prcp for date, prcp in results}

    session.close()

    return jsonify(prec)

#######################################

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    results = session.query(Station.station, Station.name).\
              all()

    statn = {station: name for station, name in results}

    session.close()

    return jsonify(statn)

########################################
@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    results = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date >= "2016-08-23").\
            filter(Measurement.station == "USC00519281").\
            all()

    tobs = {date: tobs for date, tobs in results}

    session.close()

    return jsonify(tobs)

##########################################


if __name__ == '__main__':
    app.run(debug=True)