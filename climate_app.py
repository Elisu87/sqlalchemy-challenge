# Climate_API based on Hawai SQLITE File 

# Import Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import matplotlib.dates as mdates
import pprint
from flask import Flask, jsonify
import numpy as np

#Data Set Up 
# Create engine connection
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect an existing database into a new model`automap_base()`
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table by assigning the classes to variables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

# Find the latest date of record
latest = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

# Date 12 months before the last date of record
date_start_query = (latest - dt.timedelta(days=365))


# Import Flask
from flask import Flask

# Create an app, being sure to pass __name__
app = Flask(__name__)

# List all available routes

@app.route("/")
def home():
    print("Print all available route ")
    return(
       f"Available Routes:<br/>"
       f"/api/v1.0/precipitation<br/>"
       f"/api/v1.0/stations<br/>"
       f"/api/v1.0/tobs <br/>"
       f"/api/v1.0/&ltstart&gt, for example, /api/v1.0/2016-08-23<br/>"
       f"/api/v1.0/&ltstart&gt/&ltend&gt, for example, /api/v1.0/2016-08-23/2017-08-23"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

   
    #Query dates and precipitation records from last year
    results = session.query(Measurement.date, func.avg(Measurement.prcp)).filter(Measurement.date>=date_start_query).group_by(Measurement.date).all()

    # Convert list of tuples into normal list
    prcp_dates = list(np.ravel(results))

    return jsonify(prcp_dates )

@app.route("/api/v1.0/stations")
def station():

    #Query Station Names 
    station_results = session.query(Station.station).all()

  # Convert list of tuples into normal list
    station_names= list(np.ravel(station_results))

    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():

    #Query Station Names 
    tobs_results = session.query(Measurement.date, func.avg(Measurement.tobs)). \
                      filter(Measurement.date>=date_start_query). \
                      group_by(Measurement.date).all()

    # Convert list of tuples into normal list
    t_results= list(np.ravel(tobs_results))

    return jsonify(t_results)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end=latest):

    #Query Station Names  the minimum temperature, the average temperature, and the max temperature for a given start or start-end range
    
    st_date_dt = dt.datetime.strptime(start, '%Y-%m-%d')
    if end == latest:
        end_date_dt = end
    else:
        end_date_dt = dt.datetime.strptime(end, '%Y-%m-%d')

    range_dates = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    temps = session.query(*range_dates).\
                filter(Measurement.date>=st_date).\
                filter(Measurement.date<=end_date).all()[0]
    
    results_list = [{"temp_min": temps[0]}, 
                    {"temp_avg": temps[1]}, 
                    {"temp_max": temps[2]}]
    return jsonify(results_list)
if __name__ == '__main__':
    app.run(debug=True)    


