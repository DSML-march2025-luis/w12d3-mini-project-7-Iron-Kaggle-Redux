from flask import Flask, request, jsonify, render_template
from datetime import datetime
from marshmallow import Schema, fields, validate, validates, ValidationError
from werkzeug.exceptions import UnsupportedMediaType

from model.run_xgb_model import run_model

app = Flask(__name__)


# GET /
@app.route("/", methods=["GET"])
def home():
    return jsonify("API to predicts sales for a store. Check /docs for more info.")


# GET /docs
@app.route("/docs", methods=["GET"])
def docs():
    return jsonify({
        "endpoints": {
            "/": {
                "method": "GET",
                "description": "Homepage"
            },
            "/docs": {
                "method": "GET",
                "description": "Returns available endpoints and usage."
            },
            "/model/predict-sales": {
                "method": "POST",
                "description": "Predicts sales for a store using an ML model.",
                "request_body": {
                    "required": True,
                    "fields": {
                        "store_ID": "integer - unique identifier of the store",
                        "day_of_week": "integer - day of the week, between 1 and 7",
                        "date": "string - date for the prediction in the format DD-MM-YYYY",
                        "nb_customers_on_day": "integer - expected number of customers",
                        "open": "integer - if the shop is open (1) or not (0)",
                        "promotion": "integer - if there's a promotion (1) or not (0)",
                        "state_holiday": "integer - if there's a state holiday",
                        "school_holiday": "integer - if there's school holiday (1) or not (0)",
                    },
                    "example": {
                        "store_ID": 49,
                        "day_of_week": 4,
                        "date": "26/06/2014",
                        "nb_customers_on_day": 1254,
                        "open": 1,
                        "promotion": 0,
                        "state_holiday": 0,
                        "school holiday": 1,
                    },
                }
            }
        }
    })


class FeaturesSchema(Schema):
    store_ID = fields.Int(required=True)
    day_of_week = fields.Int(required=True)
    date = fields.Date(
        required=True, 
        format='%d/%m/%Y',
        error_messages={'invalid': 'Date must be in the format DD/MM/YYYY'}
    )
    nb_customers_on_day = fields.Int(required=True)
    open = fields.Int(required=True)
    promotion = fields.Int(required=True)
    state_holiday = fields.Int(required=True)
    school_holiday = fields.Int(required=True)

features_schema = FeaturesSchema()


# POST /model/predict-sales
@app.route("/model/predict-sales", methods=["POST"])
def predict_sales():

    try:
        # receive and validate data from request body
        data = features_schema.load(request.get_json())
    except ValidationError as err:
        docs_url = request.host_url.rstrip('/') + '/docs'
        return jsonify({
            'errors': err.messages,
            'message': f"Invalid input: data must be provided in the correct format. Check {docs_url} for more info."
        }), 400

    y_pred = run_model(data)
    prediction_value = y_pred[0].item()
    return jsonify({"prediction": prediction_value})


# 415
@app.errorhandler(UnsupportedMediaType)
def handle_unsupported_media_type(e):
    docs_url = request.host_url.rstrip('/') + '/docs'
    return jsonify({
        'error': 'Invalid Content-Type',
        'message': f"Request must have Content-Type: application/json. Check {docs_url} for more info."
    }), 415


# 404
@app.errorhandler(404)
def not_found(e):
    docs_url = request.host_url.rstrip('/') + '/docs'
    return jsonify({
        'error': 'Not Found',
        'message': f"The requested resource was not found. Check {docs_url} for more info."
    }), 404


if __name__ == '__main__':
    app.run(debug=True)

