import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    # Query date and precipitation
    precipitation_query =   session.query(Measurement.date, Measurement.prcp).\
                order_by(Measurement.date).all()

    # Convert to list of dictionaries to jsonify
    prcp_date_list = []

    # Put data in a dictionary then append to list
    for date, prcp in precipitation_query:
        new_dict = {}
        new_dict[date] = prcp
        prcp_date_list.append(new_dict)

    session.close()

    return jsonify(prcp_date_list)

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    stations = {}

    
    precipitation_query = session.query(Station.station, Station.name).all()
    for station, name in precipitation_query:
        stations[station] = name

    session.close()
 
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    # find the most recent date
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    # get the date of one year ago from the most recent date
    one_year_ago_date = (dt.datetime.strptime(most_recent_date[0],'%Y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')
    #set up the query information you want returned
    sel = [Measurement.station, func.count(Measurement.station), Measurement.date]
    #make the query
    active_stations=session.query(*sel).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    #query the most active station
    most_active_station =  session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == active_stations[0][0]).filter(Measurement.date > one_year_ago_date).all()

    tobs_list = []

    # Put data in a dictionary then append to list

    for date, tobs in most_active_station:

        tobs_dictionary = {}

        tobs_dictionary[date] = tobs

        tobs_list.append(tobs_dictionary)

    session.close()

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def temperature_information_start(start):
   
    session = Session(engine)
    #query the date, min, avg, and max temperature
    temperature_query =  session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    
    temperature_list = []
    
    # Put data in a dictionary then append to list

    for date, min, avg, max in temperature_query:
        temperature_dictionary = {}
        temperature_dictionary["date"] = date
        temperature_dictionary["minimum temperature"] = min
        temperature_dictionary["average temperature"] = avg
        temperature_dictionary["maximum temperature"] = max
        temperature_list.append(temperature_dictionary)

    session.close()    

    return jsonify(temperature_list)

@app.route("/api/v1.0/<start>/<end>")
def temperature_information_start_end(start,end):
   
    session = Session(engine)
    #query the date, min, avg, and max temperature
    temperature_query =  session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter((Measurement.date >= start, Measurement.date <= end)).group_by(Measurement.date).all()

    temperature_list = []

    for date, min, avg, max in temperature_query:
        temperature_dictionary = {}
        temperature_dictionary["date"] = date
        temperature_dictionary["minimum temperature"] = min
        temperature_dictionary["average temperature"] = avg
        temperature_dictionary["maximum temperature"] = max
        temperature_list.append(temperature_dictionary)

    session.close()    

    return jsonify(temperature_list)


if __name__ == '__main__':
    app.run(debug=True)
