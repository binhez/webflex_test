import configparser
from flask import Flask, jsonify, request, send_file
import pandas as pd
from utils.sqlutil import SqlConn
import datetime
app = Flask(__name__)


@app.route('/', methods=['GET'])
def web_flex_tracking():
    # Use a breakpoint in the code line below to debug your script.
    product_name = request.args.get('product')
    user_name = request.args.get('user')
    day = request.args.get('date')

    config = configparser.ConfigParser()
    config.read('appconfig.ini')

    server = config['SQL_CONNECTION']['SERVER']
    database = config['SQL_CONNECTION']['GVI_DATABASE']
    username = config['SQL_CONNECTION']['USERNAME']
    password = config['SQL_CONNECTION']['PASSWORD']
    driver = config['SQL_CONNECTION']['DRIVER']
    procedure = config['SQL_CONNECTION']['PROCEDURE']
    # server = "10.200.10.4"
    # database = "hb_GVI_PVS"
    # username = "sa"
    # password = "Energizer1234!"
    # driver = "{ODBC Driver 17 for SQL Server}"
    print(server, database, username, password, driver)
    with SqlConn(server, username, password, driver) as gvi_sql:
        input_user = user_name
        input_product = product_name
        input_date = day
        print(input_product)
        sqlquery = f"""\
            SET NOCOUNT ON;
            EXEC [{database}].[dbo].[{procedure}] @user = ?, @product = ?, @date = ?;
            """
        print(sqlquery)
        values = (input_user, input_product, input_date)
        # values = (input_product)
        query_result = gvi_sql.excute_sp(database, sqlquery, values)
        print(query_result)

    # conn = pymssql.connect(server='10.200.10.4', user='sa', password='Energizer1234!', database='hb_GVI_PVS')
    # cursor = conn.cursor()
    # cursor.execute("set nocount on; EXEC WebflexTrackingUser @user = 'GVIAdmin'")
    # cursor.execute("SELECT TOP 50 * FROM Product")
    values = query_result
    # for row in cursor.fetchall():
    #     values.append(list(row))

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