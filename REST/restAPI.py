from flask import Flask, jsonify, request
import sqlalchemy as sqlal
#import pyodbc
from sqlalchemy.sql import select, text
import json

# import create_engine
#Server = 'LAPTOP-NLDJQR7G'
Server='192.168.0.105'
#Server='192.168.0.1'
Database = 'test'
Driver = 'ODBC Driver 17 for SQL Server'

ConStr = f'mssql://test:test123@{Server}/{Database}?driver={Driver}'



app = Flask(__name__)

@app.route('/test', methods=['GET'])
def test():
    return 'to jest test'


@app.route('/API/v1/getModelParameters', methods=['GET'])
def getModelParameters():
    engine = sqlal.create_engine(ConStr)

    metadata = sqlal.MetaData(bind=None)
    table = sqlal.Table(
        'Model_Parameters',
        metadata,
        autoload=True,
        autoload_with=engine,
        schema='models'
    )

    stmt = select([
        table.columns.ID,
        table.columns.Model,
        table.columns.Parameter,
        table.columns.Description ,
        table.columns.Value ,
        ]
    )

    connection = engine.connect()
    results = connection.execute(stmt).fetchall()

    a = []
    for result in results:
        a.append(dict(result))
    #print(type(a))
    #print(json.dumps(a))

    return json.dumps(a)

@app.route('/API/v1/addModelParameter', methods=['POST'])
def addModelParameter():
    engine = sqlal.create_engine(ConStr)
    
    with engine.connect() as con:
               
        data = request.json
        print(data)
        statement = text("INSERT INTO models.Model_Parameters VALUES(:Model, :Parameter, :Description, :Value)")
        
        for line in data:
            print(line)
            con.execute(statement, **line)
        
    return 'OK'



app.run(host='0.0.0.0',port=3000)

#  use this in browser!   http://192.168.0.105:3000/test