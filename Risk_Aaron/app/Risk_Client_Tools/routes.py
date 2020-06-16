from flask import Blueprint, render_template, Markup, url_for, request, session, flash, redirect, current_app

from flask_login import current_user, login_user, logout_user, login_required

from Aaron_Lib import *
from app.Swaps.A_Utils import *
from sqlalchemy import text
from app.extensions import db, excel

import plotly
import plotly.graph_objs as go
import plotly.express as px

import pandas as pd
import numpy as np
import json

from app.decorators import roles_required

import emoji
import flag

from app.Swaps.forms import UploadForm

from flask_table import create_table, Col

import requests

import pyexcel
from werkzeug.utils import secure_filename

from flask_table import create_table, Col
from Helper_Flask_Lib import *
from app.Risk_Client_Tools.table import *
from app.Risk_Client_Tools.forms import *
Risk_Client_Tools_bp = Blueprint('Risk_Client_Tools_bp', __name__)


# Want to check and close off account/trades.
@Risk_Client_Tools_bp.route('/Risk_auto_cut', methods=['GET', 'POST'])
@roles_required()
def Risk_auto_cut():

    start = datetime.datetime.now()
    title = "Risk Auto Cut"
    header = "Risk Auto Cut"

    # For %TW% Clients where EQUITY < CREDIT AND ((CREDIT = 0 AND BALANCE > 0) OR CREDIT > 0) AND `ENABLE` = 1 AND ENABLE_READONLY = 0
    # For other clients, where GROUP` IN  aaron.risk_autocut_group and EQUITY < CREDIT
    # For Login in aaron.Risk_autocut and Credit_limit != 0


    description = Markup('Running on <font color = "red">ALL</font> Live 1, Live 2, Live 3 and Live 5.<br>'   + \
         "Will <b>close all client's position</b> and <b>change client to read-only</b>.<br>" + \
         "Sql Table ( <font color = 'red'>aaron.risk_autocut_exclude</font>) for client excluded from the autocut.<br>" + \
         "Sql Table ( <font color = 'red'>aaron.risk_autocut_include</font>) for client with special requests.<br><br>" + \
         "<b>1)</b> For <font color = 'red'>%TW%</font> Clients : <br>EQUITY < CREDIT AND <br>((CREDIT = 0 AND BALANCE > 0) OR CREDIT > 0) AND" + \
                "<br>`ENABLE` = 1 AND ENABLE_READONLY = 0<br>and " + \
                " LOGIN NOT IN ( <font color = 'red'>aaron.risk_autocut_exclude</font>)<br>and LOGIN IN ( <font color = 'red'>aaron.risk_autocut_include</font> where EQUITY_LIMIT <> 0 )<br><br>" + \
         "<b>2)</b>For other clients, where GROUP` IN  <font color = 'red'>aaron.risk_autocut_group</font> and EQUITY < CREDIT and<br>" + \
                " LOGIN NOT IN  (<font color = 'red'>aaron.risk_autocut_exclude</font>)<br>and LOGIN IN ( <font color = 'red'>aaron.risk_autocut_include</font> where EQUITY_LIMIT <> 0 )<br><br>" + \
         "<b>3)</b> For Login in <font color = 'red'>aaron.Risk_autocut_exclude</font> and <font color = 'red'>Credit_limit != 0</font> and <br>" +\
                " LOGIN NOT IN ( <font color = 'red'>aaron.risk_autocut_exclude</font>)<br>and LOGIN IN ( <font color = 'red'>aaron.risk_autocut_include</font> where EQUITY_LIMIT <> 0 )<br><br>" + \
         "<b>4)</b> Tool will not cut for <font color = 'red'>Equity > Credit</font> . For such, kindly look at Equity Protect.<br><br>")


    client_include_tab = Delete_Risk_Autocut_Include_Table_fun()
    client_group_include_tab = Delete_Risk_Autocut_Group_Table_fun()
    client_exclude = Delete_Risk_Autocut_Exclude_Table_fun()

    # client_include_tab = create_table()
    # client_group_include_tab = create_table()
    # client_exclude = create_table()



    print("Generating of tables at risk auto cut took:{}s".format((datetime.datetime.now()-start).total_seconds()))

        # TODO: Add Form to add login/Live/limit into the exclude table.
    return render_template("Webworker_Single_Table.html", backgroud_Filename='css/Scissors.jpg', Table_name="Risk Auto Cut", \
                           title=title, ajax_url=url_for('Risk_Client_Tools_bp.risk_auto_cut_ajax', _external=True), no_backgroud_Cover=True, \
                           header=header, setinterval=10, \
                           description=description, replace_words=Markup(["Today"]),
                            varibles = {"Client Include": client_include_tab,
                                        "Client Group Include": client_group_include_tab,
                                        "Client Exclude": client_exclude}   )



@Risk_Client_Tools_bp.route('/risk_auto_cut_ajax', methods=['GET', 'POST'])
@roles_required()
def risk_auto_cut_ajax(update_tool_time=1):
    # TODO: Check if user exist first.

    #print("Risk Auto Cut Ajax")
    # Using External Table
    # aaron.risk_autocut_exclude
    # aaron.risk_autocut_group

    Live_server = [1,2,3,5]

    # Want to temp kill this tool for awhile. Will be re-writing it.
    #print(current_user.id)
    # print("{}".format( url_for('static', filename='Exec/')))
    # return_val = [{"RESULT": "No clients to be changed. Time: {}".format(time_now())}]
    # return json.dumps(return_val)

    # For %TW% Clients where EQUITY < CREDIT AND ((CREDIT = 0 AND BALANCE > 0) OR CREDIT > 0) AND `ENABLE` = 1 AND ENABLE_READONLY = 0
    # For other clients, where GROUP` IN  aaron.risk_autocut_group and EQUITY < CREDIT
    # For Login in aaron.Risk_autocut and Credit_limit != 0

    # To check the Lucky Draw Login. All TW clients for login not in aaron.risk_autocut_exclude
    # Also done a check to cause hedging clients to SO
    tw_sql_statement = """ SELECT LOGIN, '3' as LIVE, mt4_users.`GROUP`, ROUND(EQUITY, 2) as EQUITY, ROUND(CREDIT, 2) as CREDIT, '-' as EQUITY_LIMIT
            FROM live3.mt4_users WHERE `GROUP` LIKE '%TW%' AND EQUITY < CREDIT AND 
        ((CREDIT = 0 AND BALANCE > 0) OR CREDIT > 0) AND `ENABLE` = 1 AND ENABLE_READONLY = 0 and
        LOGIN not in (select login from aaron.risk_autocut_exclude where LIVE = 3) and 
        LOGIN not in (select login from aaron.risk_autocut_include where LIVE = 3 and EQUITY_LIMIT <> 0) """

    # For the client's whose groups are in aaron.risk_autocut_group, and login not in aaron.risk_autocut_exclude
    group_n_login_raw_sql_statement = """ SELECT DISTINCT mt4_trades.LOGIN,'{Live}' AS LIVE,  mt4_users.`GROUP`, ROUND(EQUITY, 2) as EQUITY, ROUND(CREDIT, 2) as CREDIT, '-' as EQUITY_LIMIT
    FROM live{Live}.mt4_trades, live{Live}.mt4_users WHERE
    mt4_trades.LOGIN = mt4_users.LOGIN AND 
        ( mt4_users.`GROUP` IN (SELECT `GROUP` FROM aaron.risk_autocut_group WHERE LIVE = '{Live}') 
                                OR
        mt4_users.LOGIN IN (SELECT LOGIN FROM aaron.risk_autocut_include WHERE LIVE = '{Live}' and EQUITY_LIMIT = 0)
        )    AND 
    CLOSE_TIME = '1970-01-01 00:00:00' AND 
    CMD < 6 AND 
    EQUITY < CREDIT AND 
    mt4_trades.LOGIN NOT IN (SELECT LOGIN FROM aaron.risk_autocut_exclude WHERE `LIVE` = '{Live}') AND
    mt4_trades.LOGIN NOT IN (SELECT LOGIN FROM aaron.risk_autocut_include WHERE `LIVE` = '{Live}' and EQUITY_LIMIT <> 0) """
    #
    group_n_login_sql_statement = " UNION ".join([group_n_login_raw_sql_statement.format(Live=n) for n in Live_server])  # construct the SQL Statment
    # raw_sql_statement += " UNION " + tw_raw_sql_statement
    #
    # raw_sql_statement = raw_sql_statement.replace("\t", " ").replace("\n", " ")
    # sql_result2 = Query_SQL_db_engine(text(raw_sql_statement))  # Query SQL



    # For the client's who are in aaron.risk_autocut_include and Credit_limit != 0
    login_special_raw_sql_statement = """SELECT DISTINCT T.LOGIN, {Live} AS LIVE,  U.`GROUP`, ROUND(EQUITY, 2) as EQUITY, ROUND(CREDIT, 2) as CREDIT, R.EQUITY_LIMIT as EQUITY_LIMIT
    FROM live{Live}.mt4_users as U, aaron.risk_autocut_include as R, live{Live}.mt4_trades as T
    WHERE R.LIVE = {Live} and R.EQUITY_LIMIT != 0 and
    R.LOGIN = U.LOGIN and U.EQUITY < R.EQUITY_LIMIT and
    U.LOGIN = T.LOGIN and T.CLOSE_TIME = '1970-01-01 00:00:00' AND
    U.LOGIN NOT IN (SELECT LOGIN FROM aaron.risk_autocut_exclude WHERE `LIVE` = '{Live}')"""

    login_special_sql_statement = " UNION ".join([login_special_raw_sql_statement.format(Live=n) for n in Live_server])  # construct the SQL Statment
    raw_sql_statement = "{} UNION {} UNION {}".format(tw_sql_statement, group_n_login_sql_statement, login_special_sql_statement)
    raw_sql_statement = raw_sql_statement.replace("\t", " ").replace("\n", " ")
    sql_result3 = Query_SQL_db_engine(text(raw_sql_statement))  # Query SQL

    #sql_result3 = []

    total_result = dict()
    # sql_result1, sql_result2 has been removed. Union to make SQL statement run faster.
    sql_results = [sql_result3]
    for s in sql_results:   # We want only unique values.
        for ss in s:
            live = ss["LIVE"] if "LIVE" in ss else None
            login = ss["LOGIN"] if "LOGIN" in ss else None
            if live != None and login != None and (live,login) not in total_result:
                total_result[(live,login)] = ss

    C_Return = dict()  # The returns from C++
    C_Return[0] = "User Changed to Read-Only, position forced closed";
    C_Return[-1] = "C++ ERROR: Params Wrong";
    C_Return[1] = "C++ ERROR: Login Param Error";
    C_Return[2] = "C++ ERROR: Server Param Error";
    C_Return[3] = "C++ ERROR: Login Number Error on MT4";
    C_Return[4] = "C++ ERROR: Equity Above Credit";
    C_Return[6] = "C++ ERROR: MT4 Update Error!";
    C_Return[7] = "C++ ERROR: MT4 Connection Error";
    C_Return[-100] = "User changed to Read-only, but SQL ERROR. ";

    To_SQL = []     # To save onto SQL

    for k,d in total_result.items():
        live = d['LIVE'] if "LIVE" in d else None
        login = d['LOGIN'] if "LOGIN" in d else None
        equity_limit = d['EQUITY_LIMIT'] if "EQUITY_LIMIT" in d and  d['EQUITY_LIMIT'] != "-" else 0
        if equity_limit == 0:   # Adding this in to beautify the Table.
            total_result[k]["EQUITY_LIMIT"] = "-"
        if not None in [live, login]:   # If both are not None.

            # # print("Live = {}, Login = {}, equity_limit = {}".format(live, login, equity_limit))
            c_run_return = Run_C_Prog("Risk_Auto_Cut.exe " + " {live} {login} {equity_limit}".format( live=live,
                login=login, equity_limit=equity_limit), cwd=".\\app" + url_for('static', filename='Exec/Risk_Auto_Cut/'))

            #print("c_run_return = {}".format(c_run_return))
            # c_run_return = 0

            if c_run_return[0] == 0:  # Need to save things into SQL as well.
                To_SQL.append(d)
            # elif c_run_return[0] not in C_Return:
            #     print(c_run_return)

            total_result[k]["RESULT"] = C_Return[c_run_return[0]] if c_run_return[0] in C_Return else "Unknown Error"
            if equity_limit != 0:    # Want to state that it's doing a equity protection.
                total_result[k]["RESULT"] += "<br><span style='color:green'>[Equity Protection]</span>"

    return_val = dict()  # Return value to be used
    if len(total_result) > 0:   # Want to send out an email should any changes have been made.

        if len(To_SQL) > 0: # There might not be anything here due to an error in C exe
            raw_insert_sql = " ({live}, {login}, {equity}, {credit}, '{group}', now()) "    # Raw template for insert.
            sql_insert_w_values = ",".join([raw_insert_sql.format(live=d["LIVE"], login=d["LOGIN"], equity=d["EQUITY"], credit=d["CREDIT"], group=d["GROUP"]) for d in To_SQL]) # SQL insert with the values.
            sql_insert = "INSERT INTO  aaron.`risk_autocut_results` (LIVE, LOGIN, EQUITY, CREDIT, `GROUP`, DATE_TIME) VALUES {}".format(sql_insert_w_values)   # Add it to the header.
            sql_insert += " ON DUPLICATE KEY UPDATE `EQUITY`=VALUES(`EQUITY`), `CREDIT`=VALUES(`CREDIT`), `GROUP`=VALUES(`GROUP`)  "


            #print("SQL Statement: {}".format(sql_insert))
            raw_insert_result = db.engine.execute(sql_insert)   # Insert into SQL

        #print("total_result: {}".format(total_result))

        total_result_value = list(total_result.values())
        # print(total_result_value)
        table_data_html =  Array_To_HTML_Table(list(total_result_value[0].keys()),[list(d.values()) for d in total_result_value])

        # Want to set to test, if it's just test accounts.
        # If it's just TEST account. Send to just Aaron and TW.

        email_list = EMAIL_LIST_RISKTW if all([d["GROUP"].lower().find("test") >= 0 for d in To_SQL]) else EMAIL_LIST_BGI


        async_send_email(To_recipients=email_list, cc_recipients=[],
                     Subject="AutoCut: Equity Below Credit.",
                     HTML_Text="{Email_Header}Hi,<br><br>The following client/s have had their position closed, and has been changed to read-only, as their equity was below credit. \
                                <br><br> {table_data_html} This is done to prevent client from trading on credit. \
                               <br><br>This Email was generated at: {datetime_now} (SGT)<br><br>Thanks,<br>Aaron{Email_Footer}".format(
                         Email_Header = Email_Header, table_data_html = table_data_html, datetime_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                         Email_Footer=Email_Footer), Attachment_Name=[])



        return_val = list(total_result.values())

    else:   # If there are nothing to change. We want to show the time
        return_val = [{"RESULT": "No clients to be changed. Time: {}".format(time_now())}]

    # # Need to update Run time on SQL Update table.
    if update_tool_time ==1:
        async_update_Runtime(app=current_app._get_current_object(), Tool="Risk_Auto_Cut")


    return json.dumps(return_val)



# Want to return the table that will be showing the list of client included in the risk auto cut.
def Delete_Risk_Autocut_Include_Table_fun():
    # Need to do a left join. To fully pull out the risk_autocut_include Logins.
    # Some Logins might not even be on the server.
    raw_sql = """SELECT R.Live, R.Login, R.Equity_limit, 
        COALESCE(`Group`,"-") as `Group`, COALESCE(`Enable`,"-") as `Enable`, COALESCE(`Enable_readonly`,"-") as `Enable_readonly`,
        COALESCE(ROUND(`Balance`,2),"-") as `Balance`, COALESCE(ROUND(`Credit`,2),"-") as `Credit`, COALESCE(ROUND(`Equity`,2),"-") as `Equity`
        FROM aaron.`risk_autocut_include` as R
            LEFT JOIN  live{Live}.mt4_users as U ON U.LOGIN = R.LOGIN
       where R.LIVE = {Live} """

    sql_query_array = [raw_sql.format(Live=l) for l in [1,2,3,5]]   # Want to loop thru all the LIVE server

    sql_query = " UNION ".join(sql_query_array) + " ORDER BY Live, Login " # UNION the query all together.
    collate = query_SQL_return_record(text(sql_query))


    if len(collate) == 0:   # There is no data.
        empty_table = [{"Result": "There are currently no single account included in the autocut. There might still be Groups tho."}]
        table = create_table_fun(empty_table, additional_class=["basic_table", "table", "table-striped",
                                                                "table-bordered", "table-hover", "table-sm"])
    else:
        # Live Account and other information of users that are in the Risk AutoCut Group.
        df_data = pd.DataFrame(collate)
        df_data["Equity_limit"] = df_data["Equity_limit"].apply(lambda x: "{:,.0f}".format(x) if type(x) == np.float64 else "{}".format(x))
        df_data["Balance"] = df_data["Balance"].apply(lambda x: "{:,.2f}".format(x) if type(x) == np.float64 else "{}".format(x))
        df_data["Credit"] = df_data["Credit"].apply(lambda x: "{:,.2f}".format(x) if type(x) == np.float64 else "{}".format(x))
        df_data["Equity"] = df_data["Equity"].apply(lambda x: "{:,.2f}".format(x) if type(x) == np.float64 else "{}".format(x))

        table = Delete_Risk_Autocut_Include_Table(df_data.to_dict("record"))
        table.html_attrs = {"class": "basic_table table table-striped table-bordered table-hover table-sm"}
    return table



# Will Query SQL and return the table needed for this.
# To generate the table needed to delete the excluded clients.
def Delete_Risk_Autocut_Exclude_Table_fun():
    # Need to do a left join. To fully pull out the risk_autocut_include Logins.
    # Some Logins might not even be on the server.
    raw_sql = """SELECT R.Live, R.`Login`, 
            COALESCE(`Group`,"-") as `Group`, COALESCE(`Enable`,"-") as `Enable`, COALESCE(`Enable_readonly`,"-") as `Enable_readonly`,
            COALESCE(`Balance`,"-") as `Balance`, COALESCE(`Credit`,"-") as `Credit`, COALESCE(ROUND(`Equity`,2),"-") as `Equity`
            FROM `risk_autocut_exclude` as R
            LEFT JOIN live{Live}.mt4_users as U ON U.LOGIN = R.LOGIN
            WHERE R.LIVE = '{Live}' """

    sql_query_array = [raw_sql.format(Live=l) for l in [1,2,3,5]]   # Want to loop thru all the LIVE server
    sql_query = " UNION ".join(sql_query_array) + " ORDER BY Live, Login " # UNION the query all together.
    collate = query_SQL_return_record(text(sql_query))


    if len(collate) == 0:   # There is no data.
        empty_table = [{"Result": "There are currently no single account excluded from the autocut."}]
        table = create_table_fun(empty_table, additional_class=["basic_table", "table", "table-striped",
                                                                "table-bordered", "table-hover", "table-sm"])
    else:
        # Live Account and other information that would be going into the table.
        df_data = pd.DataFrame(collate)

        table = Delete_Risk_Autocut_Exclude_Table(df_data.to_dict("record"))
        table.html_attrs = {"class": "basic_table table table-striped table-bordered table-hover table-sm"}

    return table



# Generate table from Querying SQL
# To add and remove GROUPS from Risk Auto Cut
def Delete_Risk_Autocut_Group_Table_fun():

    # Need to do a left join. To fully pull out the risk_autocut_group Groups.
    # Some Groups might not have any Logins.
    raw_sql =""" SELECT R.Live, R.`Group`, COALESCE(count(U.LOGIN), 0) as `Num_users`, 
            COALESCE(ROUND(SUM(U.Balance),2), 0) as `Sum_balance`, COALESCE(ROUND(SUM(U.Credit),2), 0) as `Sum_credit`
            FROM aaron.`risk_autocut_group` as R
            LEFT JOIN live{Live}.mt4_users AS U ON U.`Group` = R.`Group`
            WHERE R.Live='{Live}'
            GROUP BY `Group` """

    sql_query_array = [raw_sql.format(Live=l) for l in [1,2,3,5]]   # Want to loop thru all the LIVE server

    sql_query = " UNION ".join(sql_query_array) + " ORDER BY  Live, `Num_users`, `Group` " # UNION the query all together.
    collate = query_SQL_return_record(text(sql_query))

    if len(collate) == 0:   # There is no data.
        empty_table = [{"Result": "There are currently Groups included in the autocut. There might still be Groups tho."}]
        table = create_table_fun(empty_table, additional_class=["basic_table", "table", "table-striped",
                                                                "table-bordered", "table-hover", "table-sm"])
    else:
        # Live Account and other information of users that are in the Risk AutoCut Group.
        df_data = pd.DataFrame(collate)
        # df_data["Sum_balance"] = df_data["Sum_balance"].apply(lambda x: "{:,.2f}".format(x))
        # df_data["Sum_credit"] = df_data["Sum_credit"].apply(lambda x: "{:,.2f}".format(x))
        # df_data["Num_users"] = df_data["Num_users"].apply(lambda x: "{:,.0f}".format(x))
        table = Delete_Risk_Autocut_Group_Table(df_data.to_dict("record"))
        table.html_attrs = {"class": "basic_table table table-striped table-bordered table-hover table-sm"}
    return table


# To remove the account from being excluded.
@Risk_Client_Tools_bp.route('/Remove_Risk_Autocut_Exclude/<Live>/<Login>', methods=['GET', 'POST'])
@roles_required()
def Delete_Risk_Autocut_Exclude_Button_Endpoint(Live="", Login=""):

    # # Write the SQL Statement and Update to disable the Account monitoring.
    sql_update_statement = """DELETE FROM aaron.risk_autocut_exclude WHERE `Live`='{Live}' AND `Login`='{Login}' """.format(Live=Live, Login=Login)
    sql_update_statement = sql_update_statement.replace("\n", "").replace("\t", "")
    print(sql_update_statement)
    sql_update_statement=text(sql_update_statement)
    result = db.engine.execute(sql_update_statement)
    flash(Markup("Live: <b>{Live}</b>, Login: <b>{Login}</b> has been removed from Risk Autocut Exclude.<br>{Login} will no longer be excluded".format(Live=Live,Login=Login)))
    #return redirect(url_for('main_app.Exclude_Risk_Autocut'))
    return redirect(request.referrer)



# To remove the account from Risk Autocut.
@Risk_Client_Tools_bp.route('/Remove_Risk_Autocut_Group/<Live>/<Group>', methods=['GET', 'POST'])
@roles_required()
def Delete_Risk_Autocut_Group_Button_Endpoint(Live="", Group=""):

    # # Write the SQL Statement and Update to disable the Account monitoring.
    sql_update_statement = """DELETE FROM aaron.risk_autocut_group WHERE `Live`='{Live}' AND `Group`='{Group}' """.format(Live=Live, Group=Group)
    sql_update_statement = sql_update_statement.replace("\n", "").replace("\t", "")
    print(sql_update_statement)
    sql_update_statement=text(sql_update_statement)
    result = db.engine.execute(sql_update_statement)
    flash(Markup("Live: <b>{Live}</b>, Group: <b>{Group}</b> has been removed from Risk Autocut Group".format(Live=Live,Group=Group)))
    #return redirect(url_for('main_app.Include_Risk_Autocut_Group'))
    return redirect(request.referrer)


# To remove the account from Risk Autocut.
@Risk_Client_Tools_bp.route('/Remove_Risk_Autocut_User/<Live>/<Login>', methods=['GET', 'POST'])
@roles_required()
def Delete_Risk_Autocut_Include_Button_Endpoint(Live="", Login=""):

    # # Write the SQL Statement and Update to disable the Account monitoring.
    sql_update_statement = """DELETE FROM aaron.risk_autocut_include WHERE Live='{Live}' AND Login='{Login}'""".format(Live=Live, Login=Login)
    sql_update_statement = sql_update_statement.replace("\n", "").replace("\t", "")
    # print(sql_update_statement)
    sql_update_statement=text(sql_update_statement)
    result = db.engine.execute(sql_update_statement)

    flash("Live:{Live}, Login: {Login} has been removed from Risk Autocut".format(Live=Live,Login=Login))
    #print("Request URL: {}".format(redirect(request.url)))
    return redirect(request.referrer)
    #return redirect(url_for('main_app.Include_Risk_Autocut'))



# Want to insert into table.
# From Flask.
@Risk_Client_Tools_bp.route('/Risk_Autocut_include', methods=['GET', 'POST'])
@roles_required()
def Include_Risk_Autocut():

    title = "Risk Auto Cut [Include Client]"
    header =  Markup("Include into<br>Risk Auto Cut [Client]")

    description = Markup(
        """<b>To Include/delete from the running tool of Risk Auto Cut</b>
        <br>Will add/delete account into <span style="color:green"><b>aaron.risk_autocut_include</b></span>.<br>
        To include/remove client from being autocut.<br>
        If Equity_Limit = 0, will cut normally when <u>Equity < credit</u><br>
        Else, it will cut when <u>Equity < Equity_Limit</u>""")

    form = equity_Protect_Cut()

    form.validate_on_submit()
    if request.method == 'POST' and form.validate_on_submit():
        Live = form.Live.data  # Get the Data.
        Login = form.Login.data
        Equity_Limit = form.Equity_Limit.data

        sql_insert = """INSERT INTO  aaron.`risk_autocut_Include` (`Live`, `Login`, `Equity_Limit`) VALUES
            ('{Live}','{Account}','{Equity}') ON DUPLICATE KEY UPDATE `Equity_Limit`=VALUES(`Equity_Limit`) """.format(Live=Live, Account=Login, Equity=Equity_Limit)
        sql_insert = sql_insert.replace("\t", "").replace("\n", "")

        print(sql_insert)
        db.engine.execute(text(sql_insert))  # Insert into DB
        flash("Live: {live}, Login: {login} Equity limit: {equity_limit} has been added to aaron.`risk_autocut_Include`.".format(live=Live, login=Login, equity_limit=Equity_Limit))

    table = Delete_Risk_Autocut_Include_Table_fun()

    #Scissors backgound. We do not want it to cover. So.. we want the picture to be repeated.
    return render_template("General_Form.html", title=title, header=header, table=table, form=form,
                           description=description, backgroud_Filename='css/Scissors.jpg', no_backgroud_Cover=True)



# Want to insert into table.
# From Flask.
@Risk_Client_Tools_bp.route('/Risk_Autocut_exclude', methods=['GET', 'POST'])
@roles_required()
def Exclude_Risk_Autocut():
    title = "Exclude Risk Auto Cut"
    header = Markup("Exclude<br>Risk Auto Cut [Client]")
    description = Markup( """<b>To Exclude into the running tool of Risk Auto Cut</b>
        <br>Will add account into <span style="color:green"><b><u>aaron.risk_autocut_Exclude</u></b></span>.<br>
        To Exclude client from being autocut.""")

    form = risk_AutoCut_Exclude()
    form.validate_on_submit()
    if request.method == 'POST' and form.validate_on_submit():
        Live = form.Live.data  # Get the Data.
        Login = form.Login.data

        sql_insert = """INSERT INTO  aaron.`risk_autocut_exclude` (`Live`, `Login`) VALUES
            ('{Live}','{Account}') ON DUPLICATE KEY UPDATE Login=VALUES(Login)  """.format(Live=Live, Account=Login)
        sql_insert = sql_insert.replace("\t", "").replace("\n", "")
        db.engine.execute(text(sql_insert))  # Insert into DB
        flash("Live: {live}, Login: {login} has been added to aaron.`risk_autocut_exclude`.".format(live=Live, login=Login))

    table = Delete_Risk_Autocut_Exclude_Table_fun()

    #Scissors backgound. We do not want it to cover. So.. we want the picture to be repeated.
    return render_template("General_Form.html", title=title, header=header, table=table, form=form,
                           description=description, backgroud_Filename='css/Scissors.jpg', no_backgroud_Cover=True)



@Risk_Client_Tools_bp.route('/Risk_Autocut_Include_Group', methods=['GET', 'POST'])
@roles_required()
def Include_Risk_Autocut_Group():
    title =  "Risk Auto Cut [Group]"
    header = Markup("Risk Auto Cut [Group]")
    description = Markup("""<b>To Include the Client <span style="color:green"><b>Group</b></span> into the running tool of Risk Auto Cut</b><br>
                         Note that  <span style="color:green"><b><u>%TW% are automatically</u></b></span> included into the search.""")

    form = Live_Group()

    form.validate_on_submit()
    if request.method == 'POST' and form.validate_on_submit():
        Live = form.Live.data  # Get the Data.
        Client_Group = form.Client_Group.data

        sql_insert = """INSERT INTO  aaron.`risk_autocut_group` (`Live`, `GROUP`) VALUES
            ('{Live}','{Group}')""".format(Live=Live, Group=Client_Group)
        sql_insert = sql_insert.replace("\t", "").replace("\n", "")

        db.engine.execute(text(sql_insert))  # Insert into DB
        flash("Live: {live}, Group: {Group} has been added to aaron.`risk_autocut_group`.".format(live=Live, Group=Client_Group))

    table = Delete_Risk_Autocut_Group_Table_fun()

    #Scissors backgound. We do not want it to cover. So.. we want the picture to be repeated.
    return render_template("General_Form.html", title=title, header=header, table=table, form=form,
                           description=description, backgroud_Filename='css/Scissors.jpg', no_backgroud_Cover=True)











## ## Below are code that are not currently in use.
## ## Used previously. But retired.


#
# @main_app.route('/setinterval_test')
# @login_required
# def Aaron_test():
#     description = Markup("Testing Set Interval")
#     return render_template("Standard_Single_Table_Test.html", backgroud_Filename='css/Faded_car.jpg', Table_name="Testing", \
#                            title="Test", ajax_url=url_for('main_app.Aaron_test_ajax'),setinterval=5,
#                            description=description, replace_words=Markup(["Today"]))
#
#
#
# @main_app.route('/Aaron_test_ajax', methods=['GET', 'POST'])
# @login_required
# def Aaron_test_ajax():     # Return the Bloomberg dividend table in Json.
#
#     return_val=[{"Test":"Return: {}".format(time_now())}]
#     return json.dumps(return_val)


# To insert into SQL asynchronously.
# Header - To which database, table, and what columns
# values - Comes in a list, so we can decide how many times to insert it in.
# footer - On duplicate, what do we do?
# sql_max_insert - Optional. How many max do we want to insert at one time.

# @async_fun
# def async_sql_insert(app, header="", values = [" "], footer = "", sql_max_insert=500):
#
#     print("Using async_sql_insert")
#
#     with app.app_context():  # Using current_app._get_current_object()
#         for i in range(math.ceil(len(values) / sql_max_insert)):
#             # To construct the sql statement. header + values + footer.
#             sql_trades_insert = header + " , ".join(values[i * sql_max_insert:(i + 1) * sql_max_insert]) + footer
#             sql_trades_insert = sql_trades_insert.replace("\t", "").replace("\n", "")
#             #print(sql_trades_insert)
#             sql_trades_insert = text(sql_trades_insert)  # To make it to SQL friendly text.
#             raw_insert_result = db.engine.execute(sql_trades_insert)
#     return



#
# # Function to update the SQL position from the CFH FIX.
# # CFH_Position = {"EURUSD": 100000, "GBPUSD": 2300, ...}
# def fix_position_sql_update(CFH_Position):
#
#     # First, we want to update the position, as well as the updated time.
#     fix_position_database = "aaron"
#     fix_position_table = "cfh_live_position_fix"
#
#     # Want to construct the statement for the insert into the  DB.table.
#     # For the values that are non-zero
#     fix_position_header = """INSERT INTO {fix_position_database}.{fix_position_table} (`Symbol`, `position`, `Updated_time`) VALUES """.format(
#         fix_position_database=fix_position_database, fix_position_table=fix_position_table)
#     fix_position_values = ["('{}', '{}', now()) ".format(k,d) for k,d in CFH_Position.items()]
#     fix_position_footer = """ ON DUPLICATE KEY UPDATE position=VALUES(position), Updated_time=VALUES(Updated_time)"""
#
#     # Async update SQL to save runtime
#     async_sql_insert(app=current_app._get_current_object(),header=fix_position_header, values = fix_position_values, footer=fix_position_footer)
#
#     if len(CFH_Position) == 0:
#         CFH_Position[""] = ""
#
#
#     # Want to Update to Zero, for those position that are not opened now.
#     Update_to_zero = """UPDATE {fix_position_database}.{fix_position_table} set position = 0, Updated_time = now() where Symbol not in ({open_symbol})""".format(
#         fix_position_database=fix_position_database, fix_position_table= fix_position_table,
#         open_symbol = " , ".join(['"{}"'.format(k) for k in CFH_Position]))
#
#     # Async update SQL. No header and footer as we will construct the whole statement here.
#     async_sql_insert(app=current_app._get_current_object(),header="", values=[Update_to_zero], footer="")
#
#     return



# @main_app.route('/CFH/Details')
# @roles_required()
# def cfh_details():
#     #TODO: Add this into a blue print.
#     #loop = asyncio.new_event_loop()
#
#     description = Markup("Pull CFH Details.")
#     return render_template("Standard_Multi_Table.html", backgroud_Filename='css/Mac_table_user.jpeg', Table_name=["CFH Account Details", "CFH Live Position"], \
#                            title="CFH Details", ajax_url=url_for('main_app.chf_fix_details_ajax'),setinterval=30,
#                            description=description, replace_words=Markup(["Today"]))


#
# @main_app.route('/CFH/Details_ajax', methods=['GET', 'POST'])
# @roles_required()
# def chf_fix_details_ajax(update_tool_time=1):     # Return the Bloomberg dividend table in Json.
#
#     datetime_now = datetime.datetime.utcnow()
#     datetime_now.weekday() # 0 - monday
#
#
#     if cfh_fix_timing() == False:  # Want to check if CFH Fix still running.
#         return_data = [[{"Comment": "Out of CFH Fix timing. From UTC Sunday 2215 to Friday 2215"}],
#                        [{"Comment": "Out of CFH Fix timing. From UTC Sunday 2215 to Friday 2215"}]]
#         return json.dumps(return_data)
#
#
#     # Get the Position and Info from CFH FIX.
#     [account_info, account_position] = CFH_Position_n_Info()
#
#     if len(account_info) == 0 : # If there are no return.
#         return_data = [[{"Error": "No Return Value"}], [{"Error": "No Return Value"}]]
#         return json.dumps(return_data)
#
#     fix_position_sql_update(account_position)   # Will append the position to SQL. Will Zero out any others.
#     cfh_account_position = [{"Symbol": k, "Position" : d} for k, d in account_position.items()]
#
#
#     # Now, to calculate the Balance and such. Will put into SQL as well.
#     lp = "CFH"
#     deposit = (float(account_info["Balance"]) if "Balance" in account_info else 0) + \
#                 (float(account_info["ClosedPL"]) if "ClosedPL" in account_info else 0)
#
#     pnl = float(account_info["OpenPL"]) if "OpenPL" in account_info else 0
#
#     equity = (float(account_info["Balance"]) if "Balance" in account_info else 0) +\
#              (float(account_info["ClosedPL"]) if "ClosedPL" in account_info else 0) + \
#              (float(account_info["OpenPL"]) if "OpenPL" in account_info else 0) + \
#              (float(account_info["CreditLimit"]) if "CreditLimit" in account_info else 0)
#
#     credit = float(account_info["SecurityDeposit"]) if "SecurityDeposit" in account_info else 0
#     #credit =  account_info['CreditLimit']  if 'CreditLimit' in account_info else 0
#     account_info['equity'] = equity
#
#
#     total_margin = account_info['MarginRequirement'] if 'MarginRequirement' in account_info else 0
#     free_margin = account_info['AvailableForMarginTrading'] if 'AvailableForMarginTrading' in account_info else 0
#
#
#     database = "aaron"
#     db_table = "lp_summary"
#     #db_table = "lp_summary_copy"
#     sql_insert = """INSERT INTO {database}.{db_table} (lp, deposit, pnl, equity, total_margin, free_margin,
#             credit, updated_time) VALUES ('{lp}', '{deposit}', '{pnl}', '{equity}', '{total_margin}',
#             '{free_margin}', '{credit}', now()) ON DUPLICATE KEY UPDATE deposit=VALUES(deposit), pnl=VALUES(pnl),
#             total_margin=VALUES(total_margin), equity=VALUES(equity), credit=VALUES(credit),
#             free_margin=VALUES(free_margin), Updated_Time=VALUES(Updated_Time) """.format(database=database,
#                                     db_table=db_table, lp=lp, deposit=deposit, pnl=pnl, equity=equity,
#                                     total_margin="{:.2f}".format(float(total_margin)),
#                                     free_margin="{:.2f}".format(float(free_margin)), credit=credit)
#
#     # ASYNC send to SQL.
#     async_sql_insert(app=current_app._get_current_object(),header = "", values = [sql_insert], footer="")
#
#     if update_tool_time == 1:
#         async_update_Runtime(app=current_app._get_current_object(), Tool="CFH_FIX_Position")
#
#     return_data = [[account_info], cfh_account_position]
#
#     return json.dumps(return_data)




# @main_app.route('/MT4_Commission')
# @login_required
# def MT4_Commission():
#     description = Markup("Swap values uploaded onto MT4/MT5. <br>\
#    Swaps would be charged on the roll over to the next day.<br> \
#     Three day swaps would be charged for FX on weds and CFDs on fri. ")
#     return render_template("Standard_Single_Table.html", backgroud_Filename='css/Faded_car.jpg', Table_name="BGI_Swaps", \
#                            title="BGISwaps", ajax_url=url_for('main_app.Mt4_Commission_ajax'),
#                            description=description, replace_words=Markup([]))
#
#
# @main_app.route('/Mt4_Commission_ajax', methods=['GET', 'POST'])
# @login_required
# def Mt4_Commission_ajax():     # Return the Bloomberg dividend table in Json.
#
#     # start_date = get_working_day_date(datetime.date.today(), -1, 5)
#     sql_query = text("""select mt4_groups.`GROUP`, mt4_securities.`NAME`, mt4_groups.CURRENCY, mt4_groups.DEFAULT_LEVERAGE, mt4_groups.MARGIN_CALL, mt4_groups.MARGIN_STOPOUT, mt4_secgroups.`SHOW`, mt4_secgroups.TRADE, mt4_secgroups.SPREAD_DIFF,
#         mt4_secgroups.COMM_BASE, mt4_secgroups.COMM_TYPE, mt4_secgroups.COMM_LOTS, mt4_secgroups.COMM_AGENT, mt4_secgroups.COMM_AGENT_TYPE, mt4_secgroups.COMM_AGENT_LOTS  from
#         live5.mt4_groups, live5.mt4_secgroups, live5.mt4_securities
#         where mt4_groups.SECGROUPS = mt4_secgroups.SECGROUPS and mt4_secgroups.TYPE = mt4_securities.TYPE and
#         mt4_secgroups.`SHOW` = 1 and mt4_groups.`ENABLE` = 1
#         GROUP BY `GROUP`, mt4_securities.`NAME`""")
#
#     raw_result = db.engine.execute(sql_query)
#     result_data = raw_result.fetchall()
#     result_col = raw_result.keys()
#     return_result = [dict(zip(result_col, d)) for d in result_data]
#
#     return json.dumps(return_result)