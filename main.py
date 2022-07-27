from flask import Flask, jsonify, request, send_file
from utils.sqlutil import SqlConn, SqlData
import pyodbc
import pandas as pd
import datetime

app = Flask(__name__)


@app.route('/', methods=['POST'])
def web_flex_tracking():
    # Use a breakpoint in the code line below to debug your script.
    # name = request.args.get('name')

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


    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.200.10.4;DATABASE=hb_GVI_PVS;UID=sa;PWD=Energizer1234!')
    cursor = cnxn.cursor()
    cursor.execute("set nocount on; EXEC WebflexTrackingUser @user = 'GVIAdmin'")
    # cursor.execute("SELECT TOP 50 * FROM Product")
    values = []
    for row in cursor.fetchall():
        values.append(list(row))

    print(values)
    df = pd.DataFrame(values, index=None, columns=['Id', 'MasterItemNumber', 'ProductType',
                                    'SpinMeExportedDay', 'CaseSellable', 'DateVerified',
                                    'RemoteLocationId', 'SpinmePriority', 'AssignedDate',
                                    'WebFlexCompletedDate', 'SecondaryProductDescription',
                                    'BrandName', 'ProductStatus', 'DateCreated', 'UserName',
                                    'DateModified'])

    return df.to_json(orient='columns')


# Press the green button in the gutter to run the script.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
