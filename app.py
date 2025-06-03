from flask import Flask, request, jsonify, render_template
from datetime import datetime
from marshmallow import Schema, fields, validate, validates, ValidationError
from werkzeug.exceptions import UnsupportedMediaType

from model.run_xgb_model import run_model

app = Flask(__name__)


# GET /
@app.route("/", methods=["GET"])
def home():
    return render_template('index.html')


# GET /docs
@app.route("/docs", methods=["GET"])
def docs():
    return render_template('docs.html')


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
    state_holiday = fields.Str(required=True, validate=validate.OneOf(["0", "a", "b", "c"]))
    school_holiday = fields.Int(required=True)

    @validates('date')
    def validate_date(self, value, **kwargs):
        min = '31/07/2015'
        min_date = datetime.strptime(min, '%d/%m/%Y').date()
        if value <= min_date:
            raise ValidationError(f"Date must be later than {min}")

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

