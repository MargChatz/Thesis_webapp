from math import e
from os import error
from re import DEBUG
from flask import (Flask, render_template, request, g, redirect, url_for,jsonify)
import json
import traceback
import hashlib

from mathcad import graph_values
import database_controller as dbc
from sqlite3 import dbapi2 as sqlite3


app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/", methods=['GET','POST'])
@app.route("/home", methods=['GET','POST'])
def home():

    if request.method == "POST":
        td = {}
        gd = {}
        ld = None
        
        # Getting data for selected country
        country_name = request.form['countries']
        #country_name = country_name.upper()
        result = dbc.get_champion_country_info(country_name)
        # Creating two dictionaries out of the data we got from db
        td, gd = get_champion_country_dict_info (result)

        # Getting data for CIGRE standard
        country_name = "CIGRE"
        result = dbc.get_champion_country_info(country_name)
        # Adding CIGRE data to graph data dictionary
        gd["cigre_median_current_p"] = result[5]
        gd["cigre_std_current_p"] = result[6]
        gd["cigre_median_current_n"] = result[7]
        gd["cigre_std_current_n"] = result[8]
        gd["cigre_graph_values_p"] = graph_values(gd["cigre_median_current_p"], gd["cigre_std_current_p"], 200)[1]
        gd["cigre_graph_values_n"] = graph_values(gd["cigre_median_current_n"], gd["cigre_std_current_n"], 200)[1]

        dbc.close_connection()
        return render_template("index.html", table_data=td, graph_data=gd, literature_data=ld)


    # Get country names from db
    cursor = dbc.get_db().execute("SELECT distinct(country) FROM Data WHERE CHAMPION == 1")
    results = cursor.fetchall()

    country_names = [country[0] for country in results]
    # The above line is equal as the below block
    # country_name = []
    # for country in results:
    #     country_name.append(country[0])

    dbc.close_connection()
    return render_template("form.html", option_list=country_names)


# @app.route("/country",  methods=['GET','POST'])
# def country():
#     print("Country")
#     print(request.method)


@app.route("/addData",  methods=['GET','POST'])
def addData():
    
    if request.method == "POST":
        try:
            result = request.form.to_dict()

            #result.items() list of tuples k for key and v for values
            for k,v in result.items():
                #if value is empty put none
                if not v:
                    result[k] = "NULL"
            
            #Checkbox create false value
            if "is_champion" not in result.keys():
                result["is_champion"] = 0
            else:
                result["is_champion"] = 1

            # Id of the new entry should be +1 from db's max id.
            db = dbc.get_db()
            max_id_in_db = db.execute("SELECT max(ID) from Data").fetchall()[0][0]
            new_entry_id = max_id_in_db + 1

            insert_data_sql = "Insert into Data values(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14)" 
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
                    result["is_champion"],
                    new_entry_id)  

            champion_id = dbc.get_champion_id(db,result["country_input"])
            if result["is_champion"] == 1 and champion_id != -1:
                dbc.set_not_champion(db,champion_id)
            
            cursor = db.execute(insert_data_sql, data)

            # In order to store changes to the db, we commit.
            db.commit()
            dbc.close_connection()

            # result = 1 means everything went well.
            result = {"result": 1}
            return render_template("addDataForm.html", previous_form = result)
        except e:
            print(e)
            print(traceback.format_exc())
            # result = 0 means everything error.
            result = {"result": 0}
            return render_template("addDataForm.html",previous_form = result)

    result = {"result": -1}
    return render_template("addDataForm.html",previous_form = result)


# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        
        pass_to_bytes = str(request.form['password']).encode()
        hash_result = hashlib.md5(pass_to_bytes)
        pass_hex = hash_result.hexdigest()

        access = dbc.check_if_user_allowed_to_add_data(dbc.get_db(), request.form['username'], pass_hex)
        if not access:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect('addData')
    return render_template('login.html', error=error)


def get_champion_country_dict_info (result: list):
    """
    
    """
    
    table_data = {}
    table_data["country"] = result[0]
    table_data["LLS"] = result[1]
    table_data["DE"] = result[2]
    table_data["LA"] = result[3]
    table_data["percentage"] = result[4]

    graph_data = {}
    graph_data["median_current_p"] = result[5]
    graph_data["std_current_p"] = result[6]
    graph_data["median_current_n"] = result[7]
    graph_data["std_current_n"] = result[8]

    table_data["multiplicity"] = result[9]
    table_data["comments"] = result[10]
    table_data["literature"] = result[11]

    # Calculate graph values
    graph_data["xs"], graph_data["graph_values_p"] = graph_values(graph_data["median_current_p"], graph_data["std_current_p"], 200)
    graph_data["graph_values_n"] = graph_values(graph_data["median_current_n"], graph_data["std_current_n"], 200)[1]
    
    graph_data["csv_data_p"] = []
    graph_data["csv_data_n"] = []
    for i in range(len(graph_data["xs"])):
        graph_data["csv_data_p"].append([graph_data["xs"][i], graph_data["graph_values_p"][i]])
        graph_data["csv_data_n"].append([graph_data["xs"][i], graph_data["graph_values_n"][i]])
    
    return table_data, graph_data