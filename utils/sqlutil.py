import pyodbc  # pylint: disable=E0401,E0611
import pandas as pd  # pylint: disable=E0401,E0611





class SqlData:
    """
    Represents a row of data from a query
    """

    def __init__(self, columns, data):
        if len(columns) != len(data):
            raise Exception("Columns must equal data {} != {}".format(len(columns), len(data)))

        for idx in range(len(columns)):
            #print(columns[idx], data[idx])
            setattr(self, columns[idx], data[idx])


class SqlConn:
    """
    SQL Connection class to hide details of executing a query and saving data
    to a file. Support for CSV and PARQUET files currently.
    """

    def __init__(self, server, user, credential, driver):
        self.connections = {}
        self.server = server
        self.user = user
        self.credential = credential
        self.driver = driver

    def _yeild_execute(self, database, query):  # pylint: disable=method-hidden
        return_value = []
        #print(database,query)
        connection = self._connect(database)
        with connection.cursor() as cursor:
            cursor.execute(query)
            if cursor.description:
                columns = []

                for desc in cursor.description:
                    print("cdcdcdcdcd")
                    print(desc)
                    columns.append(desc[0])

                row = cursor.fetchone()
                while row:
                    if columns:
                        #print(row)
                        return_value.append(SqlData(columns, row))
                    row = cursor.fetchone()
            else:
                # If no description we can find out if there are row counts
                # which will reflect insert/delete rows affected, etc.
                return_value.append(SqlData(["rows"], [cursor.rowcount]))
            #cursor.close()
        return return_value
        #connection.cursor().close()

    def excute_sp(self, database, query,values):  # pylint: disable=method-hidden
        return_value = []
        #print(database,query)
        connection = self._connect(database)
        with connection.cursor() as cursor:
            cursor.execute(query, values)
            for row in cursor.fetchall():
                return_value.append(list(row))
            #cursor.close()
        return return_value
        #connection.cursor().close()

    def __enter__(self):
        """
        Support for using in a 'with' clause
        """
        return self

    def __exit__(self, type, value, traceback):
        """
        Support for using in a 'with' clause
        """
        self._disconnect()

    def _disconnect(self):
        """
        Close all open connections.
        """
        for conn in self.connections:
            #print(conn)
            self.connections[conn].close()

    def _connect(self, database):
        """
        Create a database connection of one does not already exist.
        Parameters:
        database:
            Name of the database for the connection
        Returns:
            Connection object
        """
        if database not in self.connections:
            if not self.server:
                raise Exception("Server must be identified")
            if not self.user:
                raise Exception("User must be identified")
            if not self.credential:
                raise Exception("User Credential must be identified")
            if not self.driver:
                raise Exception("ODBC Driver must be identified")

                # 'DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password
            conn_str = 'DRIVER={};SERVER={};PORT=1433;DATABASE={};UID={};PWD={}'.format(
                self.driver,
                self.server,
                database,
                self.user,
                self.credential
            )
            #print(conn_str)

            self.connections[database] = pyodbc.connect(conn_str)
        else:
            print("dfsfdsfsdfsd")
        return self.connections[database]