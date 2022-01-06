from re import DEBUG
from flask import (Flask, render_template, request, g, redirect, url_for,jsonify)
import json

from mathcad import graph_values
import database_controller as dbc
from sqlite3 import dbapi2 as sqlite3


app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/", methods=['GET','POST'])
@app.route("/home", methods=['GET','POST'])
def home():
    print(request.method)

    if request.method == "POST":
        country_name = request.form['countries']
        country_name = country_name.upper()

        cursor = dbc.get_db().execute("select * from Data where country == ? and champion == 'true'", [country_name])
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
            td["percentage"] = result[4]

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
        
        gd["csv_data_p"] = []

        for i in range(len(gd["xs"])):
            gd["csv_data_p"].append([gd["xs"][i], gd["graph_values_p"][i]])
        
        # print(gd["csv_data_p"])


        # print(gd["xs"], gd["graph_values_p"])
        # print(gd["graph_values_n"])
        # print(gd["graph_values_p"])


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
        # print(gd["cigre_graph_values_p"])
        # print(gd["cigre_graph_values_n"])
        dbc.close_connection()

        print(td)
        return render_template("index.html", table_data=td, graph_data=gd, literature_data=ld)


    # Get country names from db
    cursor = dbc.get_db().execute("select distinct(country) from Data")
    results = cursor.fetchall()
    # print(type(results))  # check what cursor returns (list of tuples)
    # print(results)
    country_names = [country[0] for country in results]
    # The above line is equal as the below block
    # country_name = []
    # for country in results:
    #     country_name.append(country[0])
    print(country_names)
    dbc.close_connection()
    return render_template("form.html", option_list=country_names)


@app.route("/country",  methods=['GET','POST'])
def country():
    print("Country")
    print(request.method)


@app.route("/addData",  methods=['GET','POST'])
def addData():
    
    if request.method == "POST":
        result = request.form.to_dict()
        print (result)

       
        #result.items() list of tuples k for key and v for values
        for k,v in result.items():
            #if value is empty put none
            if not v:
                result[k] = "NULL"
        
        #Checkbox create false value
        if "is_champion" not in result.keys():
            result["is_champion"] = False

        #print(result["is_champion"])

        db = dbc.get_db()

        insert_data_sql = "Insert into Data values(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13)" 
        data = (result["country_input"],
                result["LLS_input"],
                result["DE_input"],
                result["LA_input"],
                result["ng_input"],
                result["median_p_input"],
                result["std_p_input"],
                result["median_n_input"],
                result["std_n_input"],
                result["multi_input"],
                result["comment_input"],
                result["cite_input"],
                result["is_champion"])  
    
        # insert_data_sql = "Insert into {} ({}) values({})" \
        #     .format("Data",
        #             "country", 
        #             result["country_input"]
        #             )
        print(insert_data_sql)
        cursor = db.execute(insert_data_sql, data)


        db.commit()
            
        dbc.close_connection()

    return render_template("addDataForm.html")