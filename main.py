from flask import Flask, jsonify, request, send_file
from utils.sqlutil import SqlConn, SqlData
import pymssql
import pandas as pd
import datetime

app = Flask(__name__)


@app.route('/', methods=['GET'])
def web_flex_tracking():
    # Use a breakpoint in the code line below to debug your script.
    name = request.args.get('name')

    # server = "10.200.10.4"
    # database = "hb_GVI_PVS"
    # username = "sa"
    # password = "Energizer1234!"
    # driver = "{ODBC Driver 17 for SQL Server}"
    # print(server, database, username, password, driver)
    # with SqlConn(server, username, password, driver) as gvi_sql:
    #     # input_user = "NULL"
    #     input_product = "'PVSJAX20210730-92337'"
    #     # input_date = "NULL"
    #     sqlquery = f"""\
    #         EXEC [{database}].[dbo].[WebflexTrackingUser] @product = ?;
    #         """
    #     print(sqlquery)
    #     # values = (input_user, input_product, input_date)
    #     values = (input_product)
    #     logging.info("CALL SP FROM DATABASE - SQL QUERY:" + str(sqlquery) + " VALUE: " + str(values))
    #     query_result = gvi_sql.excute_sp(database, sqlquery, values)
    #     logging.info(query_result)
    #     data = query_result[0].fetchall()
    #     print(data)

    conn = pymssql.connect(server='10.200.10.4', user='sa', password='Energizer1234!', database='hb_GVI_PVS')
    cursor = conn.cursor()
    cursor.execute("set nocount on; EXEC WebflexTrackingUser @user = 'GVIAdmin'")
    # cursor.execute("SELECT TOP 50 * FROM Product")
    values = []
    for row in cursor.fetchall():
        values.append(list(row))

    df = pd.DataFrame(values, index=None, columns=['Id', 'MasterItemNumber', 'ProductType',
                                    'SpinMeExportedDay', 'CaseSellable', 'DateVerified',
                                    'RemoteLocationId', 'SpinmePriority', 'AssignedDate',
                                    'WebFlexCompletedDate', 'SecondaryProductDescription',
                                    'BrandName', 'ProductStatus', 'DateCreated', 'UserName',
                                    'DateModified'])

    result = jsonify(df.to_json(orient='columns'))
    # print(df)
    # print(pyodbc.drivers())
    return result

# web_flex_tracking()