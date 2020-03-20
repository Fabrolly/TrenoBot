# Train search API

## Before Starting
I will be brief: there are no public APIs for any Italian railway company. This, in my opinion, is a very bad thing: a public service should expose the API to develop third-party app.

## Where the TrenoBot data comes from
The introduction on how I got these APIs is the same as the documentation on real-time trains: Google Chrome development Console and many attempts.

# Getting the codes of the departure and arrival station
First I need to obtain the identification codes of the departure and arrival station.

The url for this request is: http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/autocompletaStazione/STATION_NAME

Example:
![](https://i.imgur.com/BJBewvV.png)

In this case, the code I have to use is **'S01645'**. I need to use it without the prefix 'S0', then only **'1645'**.

If I use a generic search term, for example 'milano':
![](https://i.imgur.com/FaEWwSW.png)
The answer shows more occurrences

# Request for solutions
Now I need the time and date of departure in this format: **AAAA-MM-GGTHH:MM:SS**
(where 'T' separates the date from the time)

Now I have everything I need:
* Departure station code
* Arrival station code
* Date and time

The url for the request is: http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/soluzioniViaggioNew/STATION_ORIGIN_CODE/STATION_DESTINATION_CODE/DATETIME

Example
![](https://i.imgur.com/mZfbWXL.png)

The traveling response contains a JSON with all possible solutions with trains, timetables, travel time.

# Collecting information from viaggiatreno response
I collect the necessary information to trenobot to respond to the user's request and generate the reply message:
```
for sol in range (0,2): #I am interested in the first two solutions proposed
        for cont in range(0,len(parsed_json['soluzioni'][sol]['vehicles'])): #if the solution has more trains (changes)
            departure_time=parsed_json['soluzioni'][sol]['vehicles'][cont]['orarioPartenza']
            departure_day=departure_time[departure_time.index('T')-2:departure_time.index('T')]
            departure_month=departure_time[departure_time.index('-')+1:]
            departure_month=departure_month[:departure_time.index('-')-2]
            departure_time=departure_time[departure_time.index('T')+1:departure_time.index('T')+6]
            arrival_time=parsed_json['soluzioni'][sol]['vehicles'][cont]['orarioArrivo']
            arrival_time=arrival_time[arrival_time.index('T')+1:arrival_time.index('T')+6]
            
            #Here I have one of the train of the solution
        #Here I have ALL the trains of the solutions
#Here I have two solutions complete
```

# Example in Telegram
<img src="https://i.imgur.com/JlLScTF.jpg" alt="example" width="310px" align="center"/>

Attention: the images in the documentation are non-final examples and realized during the test phase. The final interface is different and includes buttons for interaction and other things.

