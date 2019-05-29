
# TRAFFIC VIOLATIONS IN THE USA

## Project 2

Group Members: Orlando | Mary | Yuan | Raj

## Theme and Goal

* **Data Source:**   https://www.kaggle.com/felix4guti/traffic-violations-in-usa
* **Goal:** Investigate possible trends in US traffic violations
* **Categories of interest:** traffic violation types, demographics, geolocation, and circumstances associated with the traffic violations.

## Coding Approach 

* **ETL:** clean, transform and load data into database
* **Database:** SQLite
* **Languages and Libraries:** Python Flask, Pandas, HTML/CSS, JavaScript, Plotly, Leaflet, AJAX
* **Frameworks:** Bootstrap 4

### CSV 


| tv_id | date_of_stop | time_of_stop | agency | subagency               | description                                                                                | location                 | latitude | longitude | accident | belts | personal_injury |
|-------|--------------|--------------|--------|-------------------------|--------------------------------------------------------------------------------------------|--------------------------|----------|-----------|----------|-------|-----------------|
| 1     | ########     | 16:40:00     | MCP    | 1st district, Rockville | PEDESTRIAN CROSSING ROADWAY BETWEEN ADJACENT INTERSECTIONS HAVING TRAFFIC   CONTROL SIGNAL | VEIRS MILL / RANDOLPH RD | 39.0565  | -77.0836  | 0        | 0     | 0    

### SQLite 

```mysql
CREATE TABLE "traffic_violations_2016" (
	"tv_id"	INTEGER NOT NULL,
	"date_of_stop"	TEXT,
	"latitude"	INTEGER,
	"longitude"	INTEGER,
	"accident"	INTEGER,
	"belts"	INTEGER,
	"personal_injury"	INTEGER,
	"property_damage"	INTEGER,
	"fatal"	INTEGER,
	"commercial_license"	INTEGER,
	"hazmat"	INTEGER,
	"commercial_vehicle"	INTEGER,
	"alcohol"	INTEGER,
	"work_zone"	INTEGER,
	"state"	TEXT,
	"violation_type"	TEXT,
	"race"	TEXT,
	"gender"	TEXT,
	PRIMARY KEY("tv_id")
);
```

### Python Flask, Pandas, HTML/CSS, JavaScript, Plotly, Leaflet, AJAX

```python
#################################################
# Import Dependencies
#################################################
import os

import pandas as pd
import numpy as np
import datetime as dt
import calendar
from datetime import timedelta, date
from pandas.io.json import json_normalize

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, load_only
from sqlalchemy import create_engine, func, desc

from flask import Flask, jsonify, json, render_template, url_for, redirect, url_for, escape, request
from flask_sqlalchemy import SQLAlchemy

import folium
from cefpython3 import cefpython

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/trafficviolations.db"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Traffic_Violations_Metadata = Base.classes.traffic_violations_2016
# Samples = Base.classes.traffic_violations_statistics


#################################################
# Global Variables
#################################################


traffic_violations = ["accident", "belts", "personal_injury", "property_damage", "fatal", "commercial_license",
                      "hazmat", "commercial_vehicle", "alcohol", "work_zone"]

demographics_categories = ["WHITE", "BLACK", "ASIAN",
                           "HISPANIC", "OTHER", "NATIVE AMERICAN", "M", "F", "U"]
race_categories = ["WHITE", "BLACK", "ASIAN",
                   "HISPANIC", "OTHER", "NATIVE AMERICAN"]
gender_categories = ["M", "F", "U"]

violation_type_categories = ["Citation", "Warning", "ESERO"]

```

### Bootstrap 4 

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" http-equiv="encoding">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <title>ORYM's Project 3 - Traffic Violations</title>
    <!-- Bootstrap core CSS -->
    <link href="static/css/bootstrap.min.css" rel="stylesheet">
    <!-- Custom styles for this template -->
    <link href="static/css/dashboard.css" rel="stylesheet">
    <link href="static/css/table.css" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script src="https://d3js.org/d3.v5.min.js"></script>
  </head>
    ```

# Data Manipulation

1. Limit date_of_stop to 2016 to reduce table size
2. Converted date_of_stop format to yyyy-mm-dd for queries
3. Removed columns not used in queries

# Final Visualizations

```python
#### Line chart by month ####
@app.route("/metadata/month/linechart/")
def traffic_violation_statistic_metadata_month_linechart():
    """Return the MetaData for a given sample."""
    months_list = ["01", "02", "03", "04", "05", "06",
                   "07", "08", "09", "10", "11", "12"]  # the x value
    trace_data = []
    df = pd.read_csv('db/traffic_violation_counts_by_month.csv')
    for traffic_category in traffic_violations:
        df_traffic_category = df.loc[df["Traffic Violation"]
                                     == traffic_category]
        # Y values
        traffic_violation_data = df_traffic_category["Traffic Violation Count"].values.tolist(
        )
        # Create trace
        trace = {
            "x": months_list,
            "y": traffic_violation_data,
            "type": "scatter",
            "name": traffic_category
        }
        trace_data.append(trace)
    return jsonify(trace_data)
```

```python
# This route will create an HTML to render the monthly scatter plot and HTML table
@app.route("/scatterchart")
def scatterchart():
    df = pd.read_csv('db/traffic_violation_counts_by_month.csv')
    # Return results
    return render_template("scatterchart.html", tables=[df.to_html(classes='data')])

```

```js
$.ajax({
    url: '/stats/alcohol',
    success: function (map_data_1) {
        for (var i = 0; i < map_data_1.length; i++) {
            var title_1 = "alcohol";
            var selfIcon = L.divIcon({
                className: 'my-div-icon',
                iconSize: [50, 50],
            });
            var marker = L.marker(new L.LatLng(map_data_1[i].lat, map_data_1[i].lon), {
                title: title_1,
                icon: selfIcon
            }).setBouncingOptions({
                bounceHeight: 20,
                exclusive: true
            }).on('click', function () {
                this.bounce(3);
            }).addTo(markers);
            var content = title_1 + "</br>" + "Latitude:" + map_data_1[i].Latitude + "</br>" + "Longitude:" + map_data_1[i].Longitude;
            marker.bindPopup(content, {
                maxWidth: 600
            });
            markers.addLayer(marker);
            markerList.push(marker);
        }
    }
});
```

# Setbacks and Potential Improvements

* **Issues:**
     * Very large dataset
     * Loading issues with multiple queries
* **Potential improvements:**
    * More categories that can be explored (vehicle type, vehicle year, vehicle maker)
    * More graphs


```python

```
