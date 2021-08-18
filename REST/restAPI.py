from flask import Flask, jsonify, request
import sqlalchemy as sqlal
#import pyodbc
from sqlalchemy.sql import select
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


@app.route('/name', methods=['GET'])
def name():
    engine = sqlal.create_engine(ConStr)

    metadata = sqlal.MetaData(bind=None)
    table = sqlal.Table(
        'Name',
        metadata,
        autoload=True,
        autoload_with=engine
    )

    stmt = select([
        table.columns.id,
        table.columns.name]
    )

    connection = engine.connect()
    results = connection.execute(stmt).fetchall()

    a = []
    for result in results:
        a.append(dict(result))
    #print(type(a))
    #print(json.dumps(a))

    return json.dumps(a)


app.run(host='0.0.0.0',port=3000)

#  use this in browser!   http://192.168.0.105:3000/name