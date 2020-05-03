# (Old) Database for Trains

How the database for train works.

## The table structure

This is an example of how the database is structured (without the stop field: see the API docs):
![db](https://i.imgur.com/k4kbNX1.png)

I hid the 'stops' field because it contains a JSON with all the train stops, and it can be very long.

* **ID** Id of the reference station for the train
* **number** the unique number of the train
* **origin** Origin station
* **destination** Destination station
* **departure_datetime**
* **arrival_datetime**
* **duration**
* **delay** minutes of delay (if the train already arrived it represents the minutes of delay with which it arrived. It can be negative if the train is early)
* **state** 'Regolare' (regular), 'Parzialmente Soppresso' (Partially suppressed, see the alert field), 'Soppresso' (suppressed)
* **last_detection_time** the last time the train was detected (-- if is not departed yet )
* **last_detection_station** the last station where the train was detected (-- if is not departed yet)
* **alert** if the train is partially suppressed here there is other information about the train (modifications, ecc)
* **last_update** time of last update of the DB

Example for partially suppressed train:
![db](https://i.imgur.com/98hF1H2.png)

The 'stops' field (here omitted) contains, FOR EVERY STOP, the following information: https://camo.githubusercontent.com/400ed3ae913a8f2ebe5a7f2ed781317bc342ca4c/68747470733a2f2f692e696d6775722e636f6d2f36624c636857502e706e67

## When the system need a Train
When the system need a Train:
* Check if the train already exists on the DB
* If the train exists and the last_update field is not older than 2 minutes the system use the local information
* If the train exists and the last_update field is older than 2 minutes the system update all field by a new API request

In this way I have a two-minute 'cache' on all trains.
Very often it happens that, if a specific train has a problem, many users request information on the same train: with this expedient the system doesn't need to interrogate the API every time to get the information from trenitalia.

Any type of request, even those for scheduled alerts, passes through the manager of this database. Higher level operations are not affected by this update procedure.


**Example**

<img src="https://i.imgur.com/IJVNzQP.jpg" alt="example" width="310px" align="center"/>
