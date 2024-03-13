from flask import Flask, request, jsonify
from copy import deepcopy
import xml.etree.ElementTree as ET
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dataconversion import *
from TimeTableDB import *
from sqlalchemy.exc import SQLAlchemyError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://devuser:D%40auser@dbserver/NetVidyalaya?driver=ODBC+Driver+17+for+SQL+Server'

db = SQLAlchemy(app)

class Timetable(db.Model):
    __tablename__ = 'tTimeTable'
    __table_args__ = {'schema': 's'}
    
    id = db.Column(db.Integer, primary_key=True)
    TimeTableSchemaId = db.Column(db.Integer, nullable=False)
    EmployeeId = db.Column(db.BigInteger, nullable=False)
    DivisionId = db.Column(db.Integer, nullable=False)
    SubjectId = db.Column(db.Integer, nullable=False)
    DayId = db.Column(db.SmallInteger, nullable=False)
    LectureNumber = db.Column(db.SmallInteger, nullable=False)
    LockNo = db.Column(db.BigInteger)
    LockColour = db.Column(db.String(50))
    SchoolRoomId = db.Column(db.Integer)
    IsBreak = db.Column(db.Boolean)
    IsMergeDivision = db.Column(db.Boolean)
    IsBreakBefore = db.Column(db.Boolean)

from flask import Flask, request, jsonify
from copy import deepcopy
import xml.etree.ElementTree as ET
from flask_sqlalchemy import SQLAlchemy
from dataconversion import *
from TimeTableDB import *
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://devuser:D%40auser@dbserver/NetVidyalaya?driver=ODBC+Driver+17+for+SQL+Server'

db = SQLAlchemy(app)

class Timetable(db.Model):
    __tablename__ = 'tTimeTable'
    __table_args__ = {'schema': 'sTimeSTemptable'}
    
    id = db.Column(db.Integer, primary_key=True)
    TimeTableSchemaId = db.Column(db.Integer, nullable=False)
    EmployeeId = db.Column(db.BigInteger, nullable=False)
    DivisionId = db.Column(db.Integer, nullable=False)
    SubjectId = db.Column(db.Integer, nullable=False)
    DayId = db.Column(db.SmallInteger, nullable=False)
    LectureNumber = db.Column(db.SmallInteger, nullable=False)
    LockNo = db.Column(db.BigInteger)
    LockColour = db.Column(db.String(50))
    SchoolRoomId = db.Column(db.Integer)
    IsBreak = db.Column(db.Boolean)
    IsMergeDivision = db.Column(db.Boolean)
    IsBreakBefore = db.Column(db.Boolean)

@app.route('/api/GetTimeTablebyDivision', methods=['POST'])
def TimeTablebyDivision():
    try:
        data = request.json
        rDivisionId = int(data.get('DivisionId'))
        rOrgId = int(data.get('OrgId'))
        rClassId = int(data.get('ClassId'))
        rSchemaId = int(data.get('SchemaId'))
        
        
        sql_query = text("EXEC sTimetable.PWebSetRemainDivisionGet @rDivisionId=:DivisionId,@rSchemaId=:TimeTableSchemaId,@rClassId=:ClassId,@rOrgId=:OrgId")
        workload_result =  db.session.execute(sql_query, {
            "OrgId": rOrgId,
            "ClassId": rClassId,
            "TimeTableSchemaId": rSchemaId,
            "DivisionId": rDivisionId
        })
        lecturedata= []
        results = workload_result.fetchall()
        for row in results:
            Divisiondata = {
              'DivisionId' : row[0],
              'DayCode' : row[1],
              'LectureNumber':  row[2],
              'EmployeeName' : row[3],
              'SubjectCode': row[4]
            }
            lecturedata.append(Divisiondata)
        
        return jsonify(lecturedata)
        
    except Exception as e:
        return jsonify({'error':  str(e)})    

        
if __name__ == "__main__":
    app.run(debug=True)
