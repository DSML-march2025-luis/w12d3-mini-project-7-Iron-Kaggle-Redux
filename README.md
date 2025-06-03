
# Project: Iron Kaggle Redux - Flask API to allow store sales prediction using Machine Learning


## About

This project is part of my Master's in Data Science & Machine Learning at Ironhack.

<br>


## Project Brief

Goal:
- Create a public API to forecast the sales of a store chain based on historical data.

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



