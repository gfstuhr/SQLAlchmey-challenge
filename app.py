import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base=automap_base()
Base.prepare(engine, reflect=True)

Measurement=Base.classes.measurement
Station=Base.classes.station

app=Flask(__name__)

@app.route("/")
def welcome():
    return(
        f"""Welcome to my api! <br>
        Below are the available api routes!<br>
        /api/v1.0/precipitation<br>
        /api/v1.0/stations<br>
        /api/v1.0/tobs<br>
        /api/v1.0/start date<br>
        /api/v1.0/start date/end date"""
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    session=Session(engine)

    last_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    last_date=dt.datetime.strptime(last_date,"%Y-%m-%d")
    year_ago=last_date-dt.timedelta(days=365)
    precip_data=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()

    session.close()

    precip_results=[]
    for date, prcp in precip_data:
        precip_dict={}
        precip_dict["date"]= date
        precip_dict["prcp"]=prcp
        precip_results.append(precip_dict)
    return jsonify(precip_results)

@app.route("/api/v1.0/stations")
def stations():
    session=Session(engine)
    station_list=session.query(Station.id, Station.station,Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)

    last_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    last_date=dt.datetime.strptime(last_date,"%Y-%m-%d")
    year_ago=last_date-dt.timedelta(days=365)
    temp_data=session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == "USC00519281").\
    filter(Measurement.date >= year_ago).\
    order_by(Measurement.date.desc()).all()

    session.close()

    return jsonify(temp_data)

@app.route("/api/v1.0/<start>")
def start(start):
    session=Session(engine)

    date_range=session.query(Measurement.date).\
        filter(Measurement.date >= start).all()
    date_range2=[]
    for date in date_range:
        date_range2.append(date[0])
    

    results=[]
    for dates in date_range2:
        dict={}
        [(date, low_temp, high_temp, avg_temp)]=session.query(Measurement.date, func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date == dates).all()
        dict["date"]=date
        dict["low temp"]=low_temp
        dict["high temp"]=high_temp
        dict["avg temp"]=avg_temp
        results.append(dict)

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    session=Session(engine)

    date_range=session.query(Measurement.date).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    
    date_range2=[]
    for date in date_range:
        date_range2.append(date[0])
    

    results=[]
    for dates in date_range2:
        dict={}
        [(date, low_temp, high_temp, avg_temp)]=session.query(Measurement.date, func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date == dates).all()
        dict["date"]=date
        dict["low temp"]=low_temp
        dict["high temp"]=high_temp
        dict["avg temp"]=avg_temp
        results.append(dict)

    session.close()

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)