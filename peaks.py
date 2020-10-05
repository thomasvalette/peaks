from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flasgger import Swagger

app = Flask(__name__)

# change flasgger/swagger default route
app.config['SWAGGER'] = {
    'specs_route' : '/api/docs/'
}
# swagger object for api documentation
swagger = Swagger(app)

# database configuration
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user="postgres",
    pw=  "example",
    url= "db:5432",
    db=  "postgres")
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

#Initialize Database
db = SQLAlchemy(app)
#initialize Marshmallow
ma = Marshmallow(app)

# Represents the peak table
class Peaks(db.Model):
    id = db.Column('peak_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    alt  = db.Column(db.Integer())  
    lat  = db.Column(db.Float())
    lon  = db.Column(db.Float())

    def __init__(self, name, alt, lat, lon):
        self.name = name
        self.alt  = alt
        self.lat  = lat
        self.lon  = lon

# Marshmallow Schema
class PeaksSchema(ma.Schema):
    class Meta:
        fields = ('id','name','alt','lat', 'lon')

# Initialize schema
peak_schema = PeaksSchema()
peaks_schema = PeaksSchema(many=True)

# Initialize database with some data
db.drop_all()
db.create_all()
# Inserts sample records
db.session.add(Peaks("Everest",8848,27.9860,86.9226))
db.session.add(Peaks("Aconcagua",6959,-32.6531,-70.0108))
db.session.add(Peaks("Denali",6190,63.0695,-151.0074))
db.session.add(Peaks("Kilimandjaro",5892,-3.0656,37.3520))
db.session.add(Peaks("Elbrouz",5642,43.3212,42.4374))
db.session.add(Peaks("Massif Vinson",4892,-78.5338, -85.5341))
db.session.add(Peaks("Puncak Jaya",4884,-4.1218, 137.1602))
db.session.add(Peaks("Mont Blanc",4809,45.803, 6.8651))
db.session.add(Peaks("Mont Kosciuszko",2228,-36.4909, 148.2632))
db.session.commit()


# webservice root
@app.route("/")
def index():
    return render_template("maps.j2")

@app.route('/api')
def api():
    return redirect("/api/docs", code=302)

@app.route('/api/peak/<int:id>', methods=['GET'])
def get_peak(id):
    """Returns peak matching the id
    Returns peak matching the id if it exists
    ---
    tags:
      - Peak
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The id of the peak to retreive
    definitions:
      Peak:
        type: object
        properties:
          name:
            type: string
          alt:
            type: integer
          lat:
            type: number
          lon:
            type: number
    responses:
      200:
        description: The peak attributes
        schema:
          $ref: '#/definitions/Peak'
    """
    peak = Peaks.query.get(id)
    result = peak_schema.dump(peak)
    return jsonify(result) 

    
@app.route('/api/peak', methods=['POST'])
def add_peak():
    """Add peak
    Adds peak in the database

    Example : {"name": "Aneto","alt": 3404,"lat": 42.6006,"lon": 0.6578}
    ---
    tags:
      - Peak
    parameters:
      - name: peak
        in: body
        type: 
        required: true
        description: json containing peak attributes

    definitions:
      Peak:
        type: object
        properties:
          name:
            type: string
          alt:
            type: integer
          lat:
            type: number
          lon:
            type: number
        
    responses:
      200:
        description: The peak attributes created
        schema:
          $ref: '#/definitions/Peak'
    """
    #get data from request
    name = request.json['name']
    alt  = request.json['alt']
    lat  = request.json['lat']
    lon  = request.json['lon']

    #Instantiate new peak
    new_peak = Peaks(name, alt, lat, lon)
    #add new peak
    db.session.add(new_peak)
    #commit the change to reflect in database
    db.session.commit()
    #return the response
    return peak_schema.jsonify(new_peak) 


@app.route('/api/peak/<int:id>', methods=['PUT'])
def update_peak(id):
    """Updates peak matching the id
    Updates peak matching the id if it exists

    Example : {"name": "Mont Bleu","alt": 9999,"lat": 1.2345,"lon": 6.7890}

    ---
    tags:
      - Peak
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The id of the peak to update
      - name: peak
        in: body
        type: 
        required: true
        description: json containing peak attributes 
    definitions:
      Peak:
        type: object
        properties:
          name:
            type: string
          alt:
            type: integer
          lat:
            type: number
          lon:
            type: number
    responses:
      200:
        description: Confirming message
      500:
        description: Error message, the id doesn't match a peak
    """
    peak = Peaks.query.get(id)
    peak.name = request.json['name']
    peak.alt  = request.json['alt']
    peak.lat  = request.json['lat']
    peak.lon  = request.json['lon']
    db.session.commit()
    return {'message':'data updated'}
        

@app.route('/api/peak/<int:id>', methods=['DELETE'])
def delete_peak(id):
    """Deletes peak matching the id
    Deletes peak matching the id if it exists
    ---
    tags:
      - Peak
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The id of the peak to update
    definitions:
      Peak:
        type: object
        properties:
          name:
            type: string
          alt:
            type: integer
          lat:
            type: number
          lon:
            type: number
    responses:
      200:
        description: Confirming message
      500:
        description: Error message, the id doesn't match a peak
    """
    peak = Peaks.query.get(id)
    db.session.delete(peak)
    db.session.commit()
    return {'message':'data deleted successfully'}


@app.route('/api/peaks', methods=['GET'])
def get_all_peaks():
    """Returns all peaks
    Returns all peaks contained in the database
    ---
    tags:
      - Peaks
    definitions:
      Peak:
        type: object
        properties:
          name:
            type: string
          alt:
            type: integer
          lat:
            type: number
          lon:
            type: number
    responses:
      200:
        description: The peak attributes
        schema:
          $ref: '#/definitions/Peak'
    """
    peaks = Peaks.query.all()
    result = peaks_schema.dump(peaks)
    return jsonify(result) 


@app.route('/api/peaks', methods=['POST'])
def get_peaks_box():
    """Returns all peaks a given geographical bounding box
    The bounding box is created with 2 sets of coordinates x/y
    The first set defines the top left point of the box, the second defines the bottom right corner.

    Example : {"x1":70,"y1":-169,"x2":-50,"y2":-40}
    ---
    tags:
      - Peaks
    parameters:
      - name: coordinates
        in: body
        type: 
        required: true
        description: json containing coordinates

    definitions:
      Peak:
        type: object
        properties:
          name:
            type: string
          alt:
            type: integer
          lat:
            type: number
          lon:
            type: number
    responses:
      200:
        description: The peak attributes
        schema:
          $ref: '#/definitions/Peak'
    """

    # get peaks in a rectangle shaped box
    # rectangle coordinates
    x1 = request.json['x1']
    y1 = request.json['y1']
    x2 = request.json['x2']
    y2 = request.json['y2']

    peaks = Peaks.query.filter(Peaks.lat <= x1, Peaks.lon >= y1, 
                               Peaks.lat >= x2, Peaks.lon <= y2)   

    result = peaks_schema.dump(peaks)
    return jsonify(result) 


if __name__ == "__main__":
    app.run(debug=True)