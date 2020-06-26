# (Old) Database for Scheduled_trip

How the database for scheduled trips works

## The Table Structure

![db](https://i.imgur.com/2pFxGPR.png)

Each time a user adds a trip to his list, a row is created in this database.


* **user_id** Telegram ID of the user
* **train_id train_number** Train identifiers
* **days** Days of notification to the user (1 = Monday, 7 = Sunday)
* **departure_datetime** Time of the train departs
* **arrival_datetime** Time of the train arrival
* **origin** Origin station of the trip
* **destination** Destination station of the trip
* **last_alert** When the user has been warned last time
* **created_at** When the user has added this train to the list

## How the alert system works

Every **two minutes** the system selects the trains corresponding to the current day of the week (field 'days') and:

- From 15 minutes before departure check if the train is regular, otherwise the user will be alerted
- 5 minutes before departure, inform the user of the imminent departure with track information and delays.
- During the trip check if the train is regular, otherwise alert the user.
- Halfway through the journey sends a summary message about the trip to the user with the necessary information (delays, warnings..)

**Example**

Scheduling a trip
<img src="https://i.imgur.com/yuaaGkR.jpg" alt="example" width="310px" align="center"/>

Receipt of alerts
(train without irregularities)
<img src="https://i.imgur.com/UWfKLm6.jpg" alt="example" width="310px" align="center"/>



The user can decide to monitor the entire route or the route between two certain stations. (see the user documentation)

The notices of train irregularities are not sent every two minutes (they would be too many messages), but they are spaced from the last_alert field (every 8 minutes)
