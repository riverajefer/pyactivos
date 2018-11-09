#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################
#
## @file database.py
#
###########################################################################

import sqlite3
from sqlite3 import Error

###########################################################################
#
##   A wrapper around the sqlite3 python library.
#
#    The Database class is a high-level wrapper around the sqlite3
#    library. It allows users to create a database connection and
#    write to or fetch data from the selected database. It also has
#    various utility functions such as getLast(), which retrieves
#    only the very last item in the database, toCSV(), which writes
#    entries from a database to a CSV file, and summary(), a function
#    that takes a dataset and returns only the maximum, minimum and
#    average for each column. The Database can be opened either by passing
#    on the name of the sqlite database in the constructor, or optionally
#    after constructing the database without a name first, the open()
#    method can be used. Additionally, the Database can be opened as a
#    context method, using a 'with .. as' statement. The latter takes
#    care of closing the database.
#
###########################################################################

class Database:

    #######################################################################
    #
    ## The constructor of the Database class
    #
    #  The constructor can either be passed the name of the database to open
    #  or not, it is optional. The database can also be opened manually with
    #  the open() method or as a context manager.
    #
    #  @param name Optionally, the name of the database to open.
    #
    #  @see open()
    #
    #######################################################################
    
    def __init__(self, name=None):
        
        self.conn = None
        self.cursor = None

        if name:
            self.open(name)


    #######################################################################
    #
    ## Opens a new database connection.
    #
    #  This function manually opens a new database connection. The database
    #  can also be opened in the constructor or as a context manager.
    #
    #  @param name The name of the database to open.
    #
    #  @see \__init\__()
    #
    #######################################################################
    def open(self,name):
        
        try:
            self.conn = sqlite3.connect(name);
            self.cursor = self.conn.cursor()
            print ("Opened database successfully")

        except sqlite3.Error as e:
            print("Error connecting to database!")


    #######################################################################
    #
    ## Function to close a datbase connection.
    #
    #  The database connection needs to be closed before you exit a program,
    #  otherwise changes might be lost. You can also manage the database
    #  connection as a context manager, then the closing is done for you. If
    #  you opened the database connection with the open() method or with the
    #  constructor ( \__init\__() ), you must close the connection with this
    #  method.
    #
    #  @see open()
    #
    #  @see \__init\__()
    #
    #######################################################################
    
    def close(self):
        
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()


    def __enter__(self):
        
        return self

    def __exit__(self,exc_type,exc_value,traceback):
        
        self.close()


    #######################################################################
    #
    ## create a new table
    #
    #
    #######################################################################
    
    def create(self):
        try:
            sql_activos = """CREATE TABLE IF NOT EXISTS activos
                    (id integer PRIMARY KEY,
                    nombre text NOT NULL,
                    imagen text,
                    nfc text)"""
            sql_users = """CREATE TABLE IF NOT EXISTS Usuarios
                    (id integer PRIMARY KEY,
                    nombre text NOT NULL,
                    usuario text,
                    password text,
                    cuenta text)"""
            self.cursor.execute(sql_activos)
            self.cursor.execute(sql_users)
        except:
            pass

    #######################################################################
    #
    ## Function to fetch/query data from a database.
    #
    #  This is the main function used to query a database for data.
    #
    #  @param table The name of the database's table to query from.
    #
    #  @param columns The string of columns, comma-separated, to fetch.
    #
    #  @param limit Optionally, a limit of items to fetch.
    #
    #######################################################################

    def get(self,table,columns,limit=None):

        query = "SELECT {0} from {1};".format(columns,table)
        self.cursor.execute(query)

        # fetch data
        rows = self.cursor.fetchall()

        return rows[len(rows)-limit if limit else 0:]


    #######################################################################
    #
    ## Utilty function to get the last row of data from a database.
    #
    #  @param table The database's table from which to query.
    #
    #  @param columns The columns which to query.
    #
    #######################################################################

    def getLast(self,table,columns):
        
        return self.get(table,columns,limit=1)[0]

    
    #######################################################################
    #
    ## Utility function that converts a dataset into CSV format.
    #
    #  @param data The data, retrieved from the get() function.
    #
    #  @param fname The file name to store the data in.
    #
    #  @see get()
    #
    #######################################################################

    @staticmethod
    def toCSV(data,fname="output.csv"):
        
        with open(fname,'a') as file:
            file.write(",".join([str(j) for i in data for j in i]))


    #######################################################################
    #
    ## Function to write data to the database.
    #
    #  The write() function inserts new data into a table of the database.
    #
    #  @param table The name of the database's table to write to.
    #
    #  @param columns The columns to insert into, as a comma-separated string.
    #
    #  @param data The new data to insert, as a comma-separated string.
    #
    #######################################################################
                
    def write(self,table,columns,data):
        try:
            query = "INSERT INTO {0} ({1}) VALUES ({2});".format(table,columns,data)
            print(str(query))
            self.cursor.execute(query)
            return self.cursor.lastrowid
        except Exception as err:
            print('Query Failed: Error: %s' % (str(err)))
        finally:
            self.conn.commit()        


    #######################################################################
    #
    ## Function to query any other SQL statement.
    #
    #  This function is there in case you want to execute any other sql
    #  statement other than a write or get.
    #
    #  @param sql A valid SQL statement in string format.
    #
    #######################################################################

    def query(self,sql):
        self.cursor.execute(sql)


    #######################################################################
    #
    ## Utility function that summarizes a dataset.
    #
    #  This function takes a dataset, retrieved via the get() function, and
    #  returns only the maximum, minimum and average for each column.
    #
    #  @param rows The retrieved data.
    #
    #######################################################################

    @staticmethod
    def summary(rows):
            
        # split the rows into columns
        cols = [ [r[c] for r in rows] for c in range(len(rows[0])) ]
        
        # the time in terms of fractions of hours of how long ago
        # the sample was assumes the sampling period is 10 minutes
        t = lambda col: "{:.1f}".format((len(rows) - col) / 6.0)

        # return a tuple, consisting of tuples of the maximum,
        # the minimum and the average for each column and their
        # respective time (how long ago, in fractions of hours)
        # average has no time, of course
        ret = []

        for c in cols:
            hi = max(c)
            hi_t = t(c.index(hi))

            lo = min(c)
            lo_t = t(c.index(lo))

            avg = sum(c)/len(rows)

            ret.append(((hi,hi_t),(lo,lo_t),avg))

        return ret

    #######################################################################
    #
    ## Function to Login any other SQL statement.
    #
    #  This function is there in case you want to execute any other sql
    #  statement other than a write or get.
    #
    #  @param sql A valid SQL statement in string format.
    #
    #######################################################################

    def login(self,usuario,password):
        query = "SELECT id from Usuarios WHERE usuario = '{0}' and password = '{1}' ;".format(usuario,password)
        self.cursor.execute(query)
        print(str(query))
        # fetch data
        rows = self.cursor.fetchall()
        
        if(len(rows)>0):
            return rows[0][0]
        else:
            return False

    def addTagToId(self, tag, id):
        try:
            query = "UPDATE activos SET tag = '{0}' WHERE id = '{1}' ;".format(tag, id)
            self.cursor.execute(query)
            print(str(query))
            return True
        except Exception as err:
            print('Query update Failed: Error: %s' % (str(err)))
            return False
        finally:
            self.conn.commit()            

    def existeNFC(self,tag):
        query = "SELECT id from activos WHERE tag = '{0}' ;".format(tag)
        self.cursor.execute(query)
        print(str(query))
        rows = self.cursor.fetchall()
        if(len(rows)>0):
            return True
        else:
            return False

    def buscarPorNumero(self,numero):
        query = "SELECT id from activos WHERE numero = '{0}' ;".format(numero)
        self.cursor.execute(query)
        print(str(query))
        rows = self.cursor.fetchall()
        if(len(rows)>0):
            return rows[0][0] 
        else:
            return False

    def buscarPorTag(self,tag):
        query = "SELECT id from activos WHERE tag = '{0}' ;".format(tag)
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        if(len(rows)>0):
            return rows[0][0] 
        else:
            return False

    def getPorId(self,id):
        query = "SELECT * from activos WHERE id = '{0}' ;".format(id)
        self.cursor.execute(query)
        print(str(query))
        rows = self.cursor.fetchall()
        return rows

    def actualizarSession(self, user_id):
        try:
            query = "UPDATE sesion SET user_id = '{0}' ;".format(user_id)
            self.cursor.execute(query)
            print(str(query))
            return True
        except Exception as err:
            print('Query update Failed: Error: %s' % (str(err)))
            return False
        finally:
            self.conn.commit()
    
    def reportes(self, user_id):
        limit = 100

        query = "SELECT U.nombre, A.numero, UA.fecha, A.obsoleto FROM Usuarios AS U JOIN usuario_activo UA ON U.id = UA.usuario_id JOIN activos A ON UA.activo_id = A.id WHERE U.id = '{0}' ;".format(user_id)
        self.cursor.execute(query)
        print(str(query))
        rows = self.cursor.fetchall()
        return rows[len(rows)-limit if limit else 0:]
            
    def existeNumeroActivo(self,numero):
        query = "SELECT id from activos WHERE numero = '{0}' ;".format(numero)
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        if(len(rows)>0):
            return True
        else:
            return False

    def userIsAdmin(self):
        query = "SELECT * FROM sesion AS S JOIN Usuarios U ON U.id = S.user_id WHERE U.cuenta = 'Administrador' "
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        if(len(rows)>0):
            return True
        else:
            return False
    
    def toggleObsoleto(self, estado, activo_id):
        try:
            query = "UPDATE activos SET obsoleto = '{0}' WHERE id = '{1}' ;".format(estado, activo_id)
            self.cursor.execute(query)
            print(str(query))
            return True
        except Exception as err:
            print('Query update Failed: Error: %s' % (str(err)))
            return False
        finally:
            self.conn.commit()


