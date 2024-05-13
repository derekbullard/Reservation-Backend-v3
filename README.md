# Reservation Backend v3
 Backend Take Home Test

# Steps to run the API

## Create .env file with mongo URI
In this example we are connecting to Mongo Atlas
`MONGO_URI=mongodb+srv://<username>:<password>@cluster0.hh0aew8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0`

Make sure you have a valid certificate

## Running the Flask API
Once inside the Reservation-Backend-v3 folder run:
```
python3 app.py
```
After this the application should be running on `http://127.0.0.1:5000`

## Unit Tests
Unit tests are located in the `test.py` file

To run:
```
python3 -m unittest test.py
```

# API Endpoint
This Api has the following endpoints:
-`/submit_availability`
-`/available_slots`
-`/reserve_slot'`
-`/confirm_reservation'`

# Calling Endpoints Example
## `http://127.0.0.1:5000/confirm_reservation`
Type: `POST`
Body Format:
```
{
    "slot": "2024-05-15 10:15",
    "client_id": "Derek"
}
```

Expected Response:
```
{
    "status": "Reservation confirmed"
}
```

## `http://127.0.0.1:5000/reserve_slot`
Type: `POST`
Body Format:
```
{
    "slot": "2024-05-15 10:15",
    "client_id": "Derek"
}
```

Expected Response:
```
{
    "status": "Slot reserved"
}
```

## `http://127.0.0.1:5000/submit_availability`
Type: `POST`
Body Format:
```
{
    "provider_id": "dr_bullard",
    "date": "2024-05-13",
    "start_time": "10:00",
    "end_time": "15:00"
}
```

Expected Response:
```
{
  "status": "Availability submitted"
}
```

## `http://127.0.0.1:5000/available_slots?provider_id=dr_bullardk&date=2024-05-13`
Type: `GET`
Expected Response:
```
[
    "2024-05-13 08:00",
    "2024-05-13 08:15",
    "2024-05-13 08:30",
    "2024-05-13 08:45",
    "2024-05-13 09:00",
    "2024-05-13 09:15",
    "2024-05-13 09:30",
    "2024-05-13 09:45",
    "2024-05-13 10:00",
    "2024-05-13 10:15",
    "2024-05-13 10:30",
    "2024-05-13 10:45",
]
```


