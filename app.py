import os

import pandas as pd
import numpy as np
import datetime as dt
import calendar
import collections
from datetime import timedelta, date
from pandas.io.json import json_normalize

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, load_only
from sqlalchemy import create_engine, func, desc

from flask import Flask, jsonify, json, render_template, url_for, redirect, url_for, escape, request
from flask_sqlalchemy import SQLAlchemy

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


#################################################
# Routes
#################################################


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


#### Pie Chart for month #####

@app.route("/metadata/piechart/<month>")
def traffic_violation_statistic_metadata_piechart(month):
    """Return the MetaData for a given sample."""

    # Get start search date and end search date
    startDate = f"2016-{month}-01"
    lastDayMonth = calendar.monthrange(2016, int(month))[1]
    endDate = f"2016-{month}-{lastDayMonth}"

    traffic_violations_list = []
    traffic_violations_data = []

    for traffic_category in traffic_violations:

        sel = [
            getattr(Traffic_Violations_Metadata, traffic_category),
            func.count(getattr(Traffic_Violations_Metadata, traffic_category))
        ]

        # Query
        results = db.session.query(*sel).\
            filter(Traffic_Violations_Metadata.date_of_stop >= startDate).\
            filter(Traffic_Violations_Metadata.date_of_stop <= endDate).\
            group_by(getattr(Traffic_Violations_Metadata, traffic_category)).all()

        for result in results:

            if result[0] == 1:
                traffic_violations_data.append(int(result[1]))
                traffic_violations_list.append(traffic_category)

    # Generate the plot trace
    trace = {
        "labels": traffic_violations_list,
        "values": traffic_violations_data,
        "type": "pie"
    }

    return jsonify(trace)


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

        # y values
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


#### Table by month ####

@app.route("/metadata/month/table/")
def traffic_violation_statistic_metadata_month_table():
    """Return the MetaData for a given sample."""

    df = pd.read_csv('db/traffic_violation_counts_by_month.csv')
    df_html_table = df.to_html()
    df_html_table = df_html_table.replace('\n', '')

    # Return results
    return df_html_table

#### Line chart by week ####


@app.route("/metadata/week/linechart/")
def traffic_violation_statistic_metadata_week_linechart():
    """Return the MetaData for a given sample."""

    # X value for linechart
    weeks_list = [i + 1 for i in range(52)]

    trace_data = []

    df = pd.read_csv('db/traffic_violation_counts_by_week.csv')

    for traffic_category in traffic_violations:

        df_traffic_category = df.loc[df["Traffic Violation"]
                                     == traffic_category]

        # y values
        traffic_violation_data = df_traffic_category["Traffic Violation Count"].values.tolist(
        )

        # Create trace
        trace = {
            "x": weeks_list,
            "y": traffic_violation_data,
            "type": "scatter",
            "name": traffic_category
        }

        trace_data.append(trace)

    return jsonify(trace_data)


#### Table for year ####

@app.route("/metadata/table/")
def traffic_violation_statistic_metadata_table_year():
    """Return the MetaData for a given sample."""

    # Get start search date and end search date
    startDate = "2016-01-01"
    endDate = "2016-12-31"

    traffic_violation_metadata = []

    for traffic_category in traffic_violations:

        sel = [
            getattr(Traffic_Violations_Metadata, traffic_category),
            func.count(getattr(Traffic_Violations_Metadata, traffic_category))
        ]

        # Query
        results = db.session.query(*sel).\
            filter(Traffic_Violations_Metadata.date_of_stop >= startDate).\
            filter(Traffic_Violations_Metadata.date_of_stop <= endDate).\
            group_by(getattr(Traffic_Violations_Metadata, traffic_category)).\
            order_by(
                desc(getattr(Traffic_Violations_Metadata, traffic_category))).all()

        # Get results
        for result in results:

            # Check only first row
            metadictionary = {}

            if result[0] == 0:

                metadictionary["Traffic Violation"] = traffic_category
                metadictionary["Traffic Violation Count"] = 0

            else:

                metadictionary["Traffic Violation"] = traffic_category
                metadictionary["Traffic Violation Count"] = result[1]

            traffic_violation_metadata.append(metadictionary)

            break

    # Make dataframe and convert to HTML table
    df = pd.DataFrame(traffic_violation_metadata)
    df_html_table = df.to_html()
    df_html_table = df_html_table.replace('\n', '')

    # Return results
    return df_html_table


#### Pie Chart for year ####

@app.route("/metadata/piechart")
def traffic_violation_statistic_metadata_piechart_year():
    """Return the MetaData for a given sample."""

    # Get start search date and end search date
    startDate = "2016-01-01"
    endDate = "2016-12-31"

    traffic_violations_list = []
    traffic_violations_data = []

    for traffic_category in traffic_violations:

        sel = [
            getattr(Traffic_Violations_Metadata, traffic_category),
            func.count(getattr(Traffic_Violations_Metadata, traffic_category))
        ]

        # Query
        results = db.session.query(*sel).\
            filter(Traffic_Violations_Metadata.date_of_stop >= startDate).\
            filter(Traffic_Violations_Metadata.date_of_stop <= endDate).\
            group_by(getattr(Traffic_Violations_Metadata, traffic_category)).all()

        for result in results:

            if result[0] == 1:
                traffic_violations_data.append(int(result[1]))
                traffic_violations_list.append(traffic_category)

    # Generate the plot trace
    trace = {
        "labels": traffic_violations_list,
        "values": traffic_violations_data,
        "type": "pie"
    }

    return jsonify(trace)


#### Table for month ####

@app.route("/metadata/table/<month>")
def traffic_violation_statistic_metadata_table(month):
    """Return the MetaData for a given sample."""

    # Get start search date and end search date
    startDate = f"2016-{month}-01"
    lastDayMonth = calendar.monthrange(2016, int(month))[1]
    endDate = f"2016-{month}-{lastDayMonth}"

    traffic_violation_metadata = []

    for traffic_category in traffic_violations:

        sel = [
            getattr(Traffic_Violations_Metadata, traffic_category),
            func.count(getattr(Traffic_Violations_Metadata, traffic_category))
        ]

        # Query
        results = db.session.query(*sel).\
            filter(Traffic_Violations_Metadata.date_of_stop >= startDate).\
            filter(Traffic_Violations_Metadata.date_of_stop <= endDate).\
            group_by(getattr(Traffic_Violations_Metadata, traffic_category)).\
            order_by(
                desc(getattr(Traffic_Violations_Metadata, traffic_category))).all()

        results_count = db.session.query(*sel).\
            filter(Traffic_Violations_Metadata.date_of_stop >= startDate).\
            filter(Traffic_Violations_Metadata.date_of_stop <= endDate).\
            group_by(getattr(Traffic_Violations_Metadata,
                             traffic_category)).count()

        # Get results

        if results_count == 2:
            for result in results:

                metadictionary = {}

                if result[0] == 1:

                    metadictionary["Month"] = f"{month}"
                    metadictionary["Traffic Violation"] = traffic_category
                    metadictionary["Traffic Violation Count"] = result[1]

                traffic_violation_metadata.append(metadictionary)
                break
        else:
            for result in results:

                metadictionary = {}
                metadictionary["Month"] = f"{month}"
                metadictionary["Traffic Violation"] = traffic_category
                metadictionary["Traffic Violation Count"] = 0

                traffic_violation_metadata.append(metadictionary)

    # Make dataframe and convert to HTML table
    df = pd.DataFrame(traffic_violation_metadata)
    df_html_table = df.to_html()
    df_html_table = df_html_table.replace('\n', '')

    # Return results
    return df_html_table


#### Bar Chart ####

@app.route("/metadata/barchart/<month>")
def traffic_violation_statistic_metadata_barchart(month):
    """Return the MetaData for a given sample."""

    # Get start search date and end search date
    startDate = f"2016-{month}-01"
    lastDayMonth = calendar.monthrange(2016, int(month))[1]
    endDate = f"2016-{month}-{lastDayMonth}"

    traffic_violations_data = []

    for traffic_category in traffic_violations:

        sel = [
            getattr(Traffic_Violations_Metadata, traffic_category),
            func.count(getattr(Traffic_Violations_Metadata, traffic_category))
        ]

        # Query
        results = db.session.query(*sel).\
            filter(Traffic_Violations_Metadata.date_of_stop >= startDate).\
            filter(Traffic_Violations_Metadata.date_of_stop <= endDate).\
            group_by(getattr(Traffic_Violations_Metadata, traffic_category)).all()

        results_count = db.session.query(*sel).\
            filter(Traffic_Violations_Metadata.date_of_stop >= startDate).\
            filter(Traffic_Violations_Metadata.date_of_stop <= endDate).\
            group_by(getattr(Traffic_Violations_Metadata,
                             traffic_category)).count()

        if results_count == 2:
            for result in results:
                if result[0] == 1:
                    traffic_violations_data.append(result[1])

        else:
            for result in results:
                traffic_violations_data.append(0)

    # Generate the plot trace
    trace = {
        "x": traffic_violations,
        "y": traffic_violations_data,
        "marker": {
            "color": "blue"
        },
        "name": "Traffic Violation Count",
        "type": "bar"
    }

    return jsonify(trace)


#### Table for month and demographic  ####

@app.route("/metadata/table/<month>/<traffic_violation>/<demographic>")
def traffic_violation_table_demographic_metadata(month, traffic_violation, demographic):
    """Return the MetaData for a given sample."""

    sel = [
        getattr(Traffic_Violations_Metadata, demographic),
        func.count(getattr(Traffic_Violations_Metadata, demographic)),
        getattr(Traffic_Violations_Metadata, traffic_violation)
    ]

    # Get start search date and end search date
    startDate = f"2016-{month}-01"
    lastDayMonth = calendar.monthrange(2016, int(month))[1]
    endDate = f"2016-{month}-{lastDayMonth}"

    # Query
    results = db.session.query(*sel).\
        filter(Traffic_Violations_Metadata.date_of_stop >= startDate).\
        filter(Traffic_Violations_Metadata.date_of_stop <= endDate).\
        group_by(getattr(Traffic_Violations_Metadata, demographic)).\
        group_by(getattr(Traffic_Violations_Metadata, traffic_violation)).all()

    # Create a dictionary entry for each row of metadata information
    traffic_violation_metadata = []

    # Check if can get a null value for yes

    # Get results
    for result in results:

        metadictionary = {}

        for demographic_type in demographics_categories:
            if result[0] == demographic_type:

                metadictionary["Month"] = f"{month}"

                if result[0] in gender_categories:
                    metadictionary["Gender"] = f"{demographic_type}"
                else:
                    metadictionary["Race"] = f"{demographic_type}"

                metadictionary["Traffic Violation"] = f"{traffic_violation}"

                if result[2] == 0:
                    metadictionary["Yes/No"] = "No"
                    metadictionary["Traffic Violation Count"] = result[1]
                elif result[2] == 1:
                    metadictionary["Yes/No"] = "Yes"
                    metadictionary["Traffic Violation Count"] = result[1]

        traffic_violation_metadata.append(metadictionary)

    # Make dataframe and convert to HTML table
    df = pd.DataFrame(traffic_violation_metadata)
    df_html_table = df.to_html()
    df_html_table = df_html_table.replace('\n', '')

    # Reorder columns

    # Return results
    return df_html_table

#### Bar Chart ####


@app.route("/metadata/barchart/<month>/<traffic_violation>/<demographic>")
def traffic_violation_barchart_demographic_metadata(month, traffic_violation, demographic):
    """Return the MetaData for a given sample."""

    sel = [
        getattr(Traffic_Violations_Metadata, demographic),
        func.count(getattr(Traffic_Violations_Metadata, demographic)),
        getattr(Traffic_Violations_Metadata, traffic_violation)
    ]

    # Get start search date and end search date
    startDate = f"2016-{month}-01"
    lastDayMonth = calendar.monthrange(2016, int(month))[1]
    endDate = f"2016-{month}-{lastDayMonth}"

    # Query
    results = db.session.query(*sel).\
        filter(Traffic_Violations_Metadata.date_of_stop >= startDate).\
        filter(Traffic_Violations_Metadata.date_of_stop <= endDate).\
        group_by(getattr(Traffic_Violations_Metadata, demographic)).\
        group_by(getattr(Traffic_Violations_Metadata, traffic_violation)).all()

    # Create a dictionary entry for each row of metadata information
    traffic_violation_metadata = {}
    #traffic_violation_metadata["Date Range"] = f"{startDate} to {endDate}"

    # Call demographics list
    demographics_list = demographics(startDate, endDate)

    for result in results:
        for demographic_type in demographics_list:
            if result[0] == demographic_type:
                if result[2] == 1:
                    traffic_violation_metadata[f"{demographic_type}, {traffic_violation}"] = result[1]

    traffic_violation_x_list = [*traffic_violation_metadata]
    traffic_violation_y_list = [*traffic_violation_metadata.values()]

    # Generate the plot trace
    trace = {
        "x": traffic_violation_x_list,
        "y": traffic_violation_y_list,
        "marker": {
            "color": "blue"
        },
        "name": "Traffic Violation Count by Demographic",
        "type": "bar"
    }

    return jsonify(trace)


#### Table for month and state and demographic ####

@app.route("/metadata/table/violation_type/<month>/<user_state>/<demographic>")
def state_statistic_demographic_violation_type_metadata(month, user_state, demographic):
    """Return the MetaData for a given sample."""

    sel = [
        Traffic_Violations_Metadata.state,
        getattr(Traffic_Violations_Metadata, demographic),
        Traffic_Violations_Metadata.violation_type,
        func.count(Traffic_Violations_Metadata.violation_type)
    ]

    # Get start search date and end search date
    startDate = f"2016-{month}-01"
    lastDayMonth = calendar.monthrange(2016, int(month))[1]
    endDate = f"2016-{month}-{lastDayMonth}"

    # Query
    results = db.session.query(*sel).\
        filter(Traffic_Violations_Metadata.date_of_stop >= startDate).\
        filter(Traffic_Violations_Metadata.date_of_stop <= endDate).\
        filter(Traffic_Violations_Metadata.state == user_state).\
        group_by(getattr(Traffic_Violations_Metadata, demographic)).\
        group_by(Traffic_Violations_Metadata.violation_type).all()

    # Create a dictionary entry for each row of metadata information
    traffic_violation_metadata = []

    for result in results:

        metadictionary = {}

        for demographic_type in demographics_categories:
            if result[1] == demographic_type:
                for recorded_violation_type in violation_type_categories:
                    if result[2] == recorded_violation_type:
                        metadictionary["State"] = f"{user_state}"
                        if result[1] in gender_categories:
                            metadictionary["Gender"] = f"{demographic_type}"
                        else:
                            metadictionary["Race"] = f"{demographic_type}"
                        metadictionary["Violation Type"] = f"{recorded_violation_type}"
                        metadictionary["Violation Type Count"] = result[3]

        traffic_violation_metadata.append(metadictionary)

    # Make dataframe and convert to HTML table
    df = pd.DataFrame(traffic_violation_metadata)
    df_html_table = df.to_html()
    df_html_table = df_html_table.replace('\n', '')

    # Return results
    return df_html_table


#### Bar Chart ####

@app.route("/metadata/barchart/violation_type/<month>/<user_state>/<demographic>")
def state_barchart_demographic_violation_type_metadata(month, user_state, demographic):
    """Return the MetaData for a given sample."""

    sel = [
        Traffic_Violations_Metadata.state,
        getattr(Traffic_Violations_Metadata, demographic),
        Traffic_Violations_Metadata.violation_type,
        func.count(Traffic_Violations_Metadata.violation_type)
    ]

    # Get start search date and end search date
    startDate = f"2016-{month}-01"
    lastDayMonth = calendar.monthrange(2016, int(month))[1]
    endDate = f"2016-{month}-{lastDayMonth}"

    # Query
    results = db.session.query(*sel).\
        filter(Traffic_Violations_Metadata.date_of_stop >= startDate).\
        filter(Traffic_Violations_Metadata.date_of_stop <= endDate).\
        filter(Traffic_Violations_Metadata.state == user_state).\
        group_by(getattr(Traffic_Violations_Metadata, demographic)).\
        group_by(Traffic_Violations_Metadata.violation_type).all()

    # Create a dictionary entry for each row of metadata information
    traffic_violation_metadata = {}

    for result in results:
        traffic_violation_metadata[f"{user_state}"] = {}
        for demographic_type in demographics_categories:
            if result[1] == demographic_type:

                traffic_violation_metadata[f"{user_state}"][f"{demographic_type}"] = {
                }

                for recorded_violation_type in violation_type_categories:

                    if result[2] == recorded_violation_type:

                        traffic_violation_metadata[f"{user_state}, {demographic_type}, {recorded_violation_type}"] = result[3]

    violation_type_x_list = [*traffic_violation_metadata]
    violation_type_y_list = [*traffic_violation_metadata.values()]

    # Generate the plot trace
    trace = {
        "x": violation_type_x_list,
        "y": violation_type_y_list,
        "marker": {
            "color": "blue"
        },
        "name": "Traffic Violation Type Count by Demographic",
        "type": "bar"
    }

    return jsonify(trace)

# END OF ORLANDO'S ROUTES #######################


#################################################
# Mery's Routes Start below


# Returns a list containign Race and Gender of the offender
@app.route('/stats/<sample_id>')
def stats(sample_id):
    """Return a list of genders."""

    stats_db = db.session.query(Traffic_Violations_Metadata.date_of_stop, Traffic_Violations_Metadata.latitude, Traffic_Violations_Metadata.longitude, Traffic_Violations_Metadata.state,
                                Traffic_Violations_Metadata.violation_type, Traffic_Violations_Metadata.race, Traffic_Violations_Metadata.gender).filter(Traffic_Violations_Metadata.__table__.c[sample_id] == 1).all()
    alist = []
    for x in stats_db:
        adict = {
            "date": x[0],
            "lat": x[1],
            "lon": x[2],
            "state": x[3],
            "violation_type": x[4],
            "race": x[5],
            "gender": x[6]
        }
        alist.append(adict)

    # convert to json data
        jsonStr = json.dumps(alist)

    # statelist =[]
    # for dictionary in alist:
    #     statelist.append(dictionary["state"])

        # # Format the data for Plotly
    # traceFatal = {
    #      "x": statelist,
    #      "y": stats_db[sample_id].values.tolist(),
    #      "type": "bar"
    # }
    # return jsonify(traceFatal)
    return jsonify(alist)


###############################################

@app.route("/property")
def property_data():
    """Return Traffic Violations score and Traffic Violations id"""

    query_statement = db.session.query(Traffic_Violations_Metadata).order_by(
        Traffic_Violations_Metadata.property_damage.desc()).limit(4000).statement
    df = pd.read_sql_query(query_statement, db.session.bind)

    # Format the data for Plotly
    traceProperty = {
        "x": df["date_of_stop"].values.tolist(),
        "y": df["property_damage"].values.tolist(),
        "type": "bar"
    }
    return jsonify(traceProperty)


@app.route("/ppeinjury")
def ppeinjury_data():
    """Return Traffic Violations score and Traffic Violations char"""

    # Query for the top 10 Traffic Violations data
    results = db.session.query(Traffic_Violations_Metadata.gender, Traffic_Violations_Metadata.personal_injury).order_by(
        Traffic_Violations_Metadata.personal_injury.desc()).limit(2500).all()

    # Create lists from the query results
    gender = [result[0] for result in results]
    ppe_injury = [int(result[1]) for result in results]

    # Generate the plot trace
    tracePPE = {
        "x": gender,
        "y": ppe_injury,
        "type": "bar"
    }
    return jsonify(tracePPE)


@app.route("/fatal")
def fatal_data():
    """Return Traffic Violations score and Traffic Violations name"""

    # Query for the top 10 Traffic Violations data
    results = db.session.query(Traffic_Violations_Metadata.race, Traffic_Violations_Metadata.fatal).order_by(
        Traffic_Violations_Metadata.fatal.desc()).limit(100).all()
    df = pd.DataFrame(results, columns=['race', 'fatal'])

    # Format the data for Plotly
    traceFatal = {
        "x": df["race"].values.tolist(),
        "y": df["fatal"].values.tolist(),
        "type": "bar"
    }
    return jsonify(traceFatal)


@app.route("/alcohol")
def alcohol_data():
    """Return Traffic Violations score and Traffic Violations id"""

    # Query for the Traffic Violations data using pandas
    query_statement = db.session.query(Traffic_Violations_Metadata).order_by(
        Traffic_Violations_Metadata.alcohol.desc()).limit(300).statement
    df = pd.read_sql_query(query_statement, db.session.bind)

    # Format the data for Plotly
    traceAlcohol = {
        "x": df["arrest_type"].values.tolist(),
        "y": df["alcohol"].values.tolist(),
        "type": "bar"
    }

    return jsonify(traceAlcohol)



@app.route("/comlicense")
def comlicense_data():
    """Return Traffic Violations score and Traffic Violations id"""

    # Query for the Traffic Violations data using pandas
    query_statement = db.session.query(Traffic_Violations_Metadata).order_by(
        Traffic_Violations_Metadata.commercial_license.desc()).limit(5500).statement
    df = pd.read_sql_query(query_statement, db.session.bind)

    # Format the data for Plotly
    traceComlicense = {
        "labels": df["violation_type"].values.tolist(),
        "values": df["commercial_license"].values.tolist(),
        "type": "pie" 
    }
    return jsonify(traceComlicense)



@app.route("/belts")
def belt_data():
    """Return Traffic Violations score and Traffic Violations id"""

    # Query for the Traffic Violations data using pandas
    results = db.session.query(Traffic_Violations_Metadata.date_of_stop, Traffic_Violations_Metadata.belts).order_by(
        Traffic_Violations_Metadata.belts.desc()).limit(7500).all()
    df = pd.DataFrame(results, columns=['date_of_stop', 'belts'])

    # Format the data for Plotly
    traceBelts = {
        "x": df["date_of_stop"].values.tolist(),
        "y": df["belts"].values.tolist(),
        "type": "bar"
    }
    return jsonify(traceBelts)


#################################################
# WILL DEVELOP HTML PAGES TO RENDER CHARTS
#################################################

# This HTML will render a csv table on the html
@app.route("/indexjson")
def indexjson():
    return render_template("index_json.html")


# This route will create an HTML to render one scatter plot
@app.route("/scatterchart")
def scatterchart():
    return render_template("scatterchart.html")

# This route will create an HTML to render one scatter plot
@app.route("/scatterweekly")
def scatterweekly():
    return render_template("scatter.html")


# This route will create an HTML to render the pie plot
@app.route("/pie_chart")
def pie_chart():
    return render_template("pie_chart.html")


# This route will create an HTML to render one of the bar charts
@app.route("/barmonthly")
def barmonthly():
    return render_template("barmonthly.html")

# This route will load the bar chart created using /property damage
@app.route("/propertychart")
def propertychart():
    return render_template("propertychart.html")


# This route will load the bar chart created using /alcohol
@app.route("/alcoholchart")
def alcoholchart():
    return render_template("alcoholchart.html")


# This route will load the bar chart created using /fatal accidents
@app.route("/fatalchart")
def fatalchart():
    return render_template("fatalchart.html")


# This route will load the bar chart created using /Personal Injury
@app.route("/ppeinjurychart")
def ppeinjurychart():
    return render_template("ppeinjurychart.html")


# This route will load the bar chart created using /Commercial License
@app.route("/comlicensebar")
def comlicensebar():
    return render_template("comlicensebar.html")


# This route will load the bar chart created using /seatbelts
@app.route("/seatbeltbar")
def seatbeltbar():
    return render_template("seatbeltbar.html")


# # This route will create an HTML of the data used
# @app.route("/trafficstats")
# def trafficstats():
#     return render_template("trafficstats.html")


# # This route will create an HTML
# @app.route("/tvstats")
# def tvstats():
#     return render_template("tvstats.html")


if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
