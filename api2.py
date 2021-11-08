from flask import Flask,jsonify,request
from app import getPrediction
app = Flask(__name__)
@app.route('/predict-digit',methods = ['POST'])
def predictData():
    image = request.files.get('alphabet')
    prediction = getPrediction(image)
    return jsonify({
        "Prediction":prediction
    },200)
if __name__ == '__main__':
    app.run(debug = True)