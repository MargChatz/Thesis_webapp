from re import DEBUG
from flask import (Flask, render_template, request, g, redirect, url_for,jsonify)
import json

from mathcad import graph_values
import database_controller as dbc
from sqlite3 import dbapi2 as sqlite3


app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/nav",  methods=['GET','POST'])
def nav():
      return render_template("nav.html")

@app.route("/",  methods=['GET','POST'])
def home():
    print(request.method)

    if request.method == "POST":
        country_name = request.form['countries']
        country_name = country_name.upper()

        cursor = dbc.get_db().execute("select * from Data where country == ?", [country_name])
        results = cursor.fetchall()
        # print(results)
        # print(type(results))
        # print(results[0][0])
        
        td = {}
        gd = {}
        ld = None
        for result in results:
            td["country"] = result[0]
            td["LLS"] = result[1]
            td["DE"] = result[2]
            td["LA"] = result[3]
            td["NG"] = result[4]

            gd["median_current_p"] = result[5]
            gd["std_current_p"] = result[6]
            gd["median_current_n"] = result[7]
            gd["std_current_n"] = result[8]

            td["multiplicity"] = result[9]
            td["comments"] = result[10]
            td["literature"] = result[11]

        
        j = json.dumps(td, indent=4)
        with open("data.json", "w") as outfile:
            outfile.write(j)

        # Calculate graph values
        gd["xs"], gd["graph_values_p"] = graph_values(gd["median_current_p"], gd["std_current_p"], 200)
        gd["graph_values_n"] = graph_values(gd["median_current_n"], gd["std_current_n"], 200)[1]

        country_name = "CIGRE STD"
        cursor = dbc.get_db().execute("select * from Data where country == ?", [country_name])
        results = cursor.fetchall()
        for result in results:
            gd["cigre_median_current_p"] = result[5]
            gd["cigre_std_current_p"] = result[6]
            gd["cigre_median_current_n"] = result[7]
            gd["cigre_std_current_n"] = result[8]
        gd["cigre_graph_values_p"] = graph_values(gd["cigre_median_current_p"], gd["cigre_std_current_p"], 200)[1]
        gd["cigre_graph_values_n"] = graph_values(gd["cigre_median_current_n"], gd["cigre_std_current_n"], 200)[1]
        # print(gd["graph_values_p"])
        # print(gd["graph_values_n"])
        dbc.close_connection()
        return render_template("index.html", table_data=td, graph_data=gd, literature_data=ld)


    # Get country names from db
    cursor = dbc.get_db().execute("select country from Data")
    results = cursor.fetchall()
    # print(type(results))  # check what cursor returns (list of tuples)
    # print(results)
    country_names = [country[0] for country in results]
    # The above line is equal as the below block
    # country_name = []
    # for country in results:
    #     country_name.append(country[0])
    print(country_names)
    return render_template("form.html", option_list=country_names)


@app.route("/country",  methods=['GET','POST'])
def country():
    print("Country")
    print(request.method)



    