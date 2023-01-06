#Import Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import numpy as np
import datetime as dt


# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Setup App
app = Flask(__name__)

# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes in the Hawaii Database:<br/>"
        f"Homepage: "
        f"/<br/>"
        f"Precipitation readings for a given date: "
        f"/api/v1.0/precipitation<br/>"
        f"List of stations: "
        f"/api/v1.0/stations<br/>"
        f"Dates and temperatures for most active station: "
        f"/api/v1.0/tobs"
        f"Summary statistics for a given start or start-end range: "
        f"/api/v1.0/<start>` and `/api/v1.0/<start>/<end><br/>"
    )
    
@app.route("/api/v1.0/precipitation")
def precip():
    #Create session using engine
    session = Session(engine)
    #Query, pass to list, and jsonify
    data = session.query(Measurement.date, Measurement.prcp).all()
    precip_list = []
    for date, prcp in data:
        pdict = {}
        pdict["date"] = date
        pdict["prcp"] = prcp
        
        precip_list.append(pdict)
    session.close()
    return jsonify(precip_list)

@app.route("/api/v1.0/stations")
#Return a JSON list of stations from the dataset.
def stations():
    #Create session using engine
    session = Session(engine)
    #Query, pass to list, and jsonify
    data = session.query(Station.station, Station.name).all()
    station_list = []
    for station, name in data:
        sdict = {}
        sdict['station'] = station
        sdict['name'] = name
        station_list.append(sdict)
    session.close()
    return jasonify(station_list)
@app.route("/api/v1.0/tobs")

# Return a JSON list of temperature observations (TOBS) for the previous year.
def tobs():
    #Create session using engine
    session = Session(engine)
    #Query, pass to list, and jsonify
    data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station=='USC00519281').all()
    tobs_list = []
    for date, tobs in data:
        tdict = {}
        tdict["date"] = date
        tdict["tobs"] = tobs
        
        tobs_list.append(tdict)
    session.close()
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start_date):
    #Create session using engine
    session = Session(engine)
    #Query, pass to list, and jsonify
    meas_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date>=start_date).all()
    stat_list = []
    for min, max, avg in meas_results:
        stdict = {}
        stdict["Min"] = min
        stdict["Max"] = max
        stdict["Average"] = avg
        stat_list.append(stdict)
    session.close()
    return jsonify(stat_list)
    
@app.route("/api/v1.0/<start>/<end>")
def startend(start_date, end_date):
    #Create session using engine
    session = Session(engine)
    #Query, pass to list, and jsonify
    meas_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date>=start_date).filter(Measurement.date<=start_date).all()
    stat_list = []
    for min, max, avg in meas_results:
        stdict = {}
        stdict["Min"] = min
        stdict["Max"] = max
        stdict["Average"] = avg
        stat_list.append(stdict)
    session.close()
    return jsonify(stat_list)

if __name__ == "__main__":
    app.run(debug=True)
