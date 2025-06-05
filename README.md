
# Project: Iron Kaggle Redux - Flask API to allow store sales prediction using Machine Learning

<br>


## About

This project is part of my Master's in Data Science & Machine Learning at Ironhack.

<br><br>



## Project Brief

Goal:
- Create a public API to forecast the sales of a store chain based on historical data, using Machine Learning.

<br>

Requirements:
- The API should be based on the model we created in our previous project, [Iron-Kaggle](https://github.com/DSML-march2025-luis/w10d3-mini-project-6-Iron-Kaggle)
- This API will provide a POST endpoint to predict the sales of a store on a specific date (see format below)
- It should handle well incorrect requests (e.g. wrong http method, requests with missing data, invalid format, etc)
- It must be deployed to allow public access (e.g. Docker, AWS)

<br>

Example request body:

```json
{
    "store_ID": 49,
    "day_of_week": 4,
    "date": "26/06/2014",
    "nb_customers_on_day": 1254,
    "open": 1,
    "promotion": 0,
    "state_holiday": "a",
    "school_holiday": 1
}
```

<br>

---

<br>

## Setup and Run (Local environment)

1. Create a virtual environment:

```bash
   python -m venv iron-kaggle-redux-venv
   source iron-kaggle-redux-venv/bin/activate  # On Windows: iron-kaggle-redux-venv\Scripts\activate
```


2. Install dependencies

```bash
pip install -r requirements.txt
```


3. Run the app:

```bash
flask --app app run --debug
```


The app will be available at http://127.0.0.1:5000

<br>



## Setup and Run (with Docker)


1. Build the Docker image:

On Linux/Windows:

```bash
docker build -t iron-kaggle-redux .
```

On Mac (this will create an image in x86 architecture, so that it's compatible with the free tier of AWS):

```bash
docker buildx create --use
docker buildx build --platform linux/amd64 -t iron-kaggle-redux:latest . --load
```



2. Run the container:

```bash
docker run -p 5000:5000 iron-kaggle-redux
```

The app will be available at http://127.0.0.1:5000

<br>


## Deployment

To deploy on AWS (ECR + EC2), follow this instructions:
https://gist.github.com/luisjunco/994a77b46cd3a2bcb50407c78e7efdf3

