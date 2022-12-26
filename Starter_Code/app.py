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

    # Query for the dates and precipitation values
    results =   session.query(Measurement.date, Measurement.prcp).\
                order_by(Measurement.date).all()

    # Convert to list of dictionaries to jsonify
    prcp_date_list = []

    for date, prcp in results:
        new_dict = {}
        new_dict[date] = prcp
        prcp_date_list.append(new_dict)

    session.close()

    return jsonify(prcp_date_list)

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    stations = {}

    # Query all stations
    results = session.query(Station.station, Station.name).all()
    for s,name in results:
        stations[s] = name

    session.close()
 
    return jsonify(stations)


if __name__ == '__main__':
    app.run(debug=True)
