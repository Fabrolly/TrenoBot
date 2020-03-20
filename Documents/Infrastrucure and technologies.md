# Infrastructure
Where I develop TrenoBot and the technologies used

## Python
Trenobot is developed with python, since it's first line of code. It seems to be the perfect language for my needs: and so, for now, seems to be.

## mariaDB
A database is necessary to make a cache of requests and to manage all trains and user lists in a simple and safe way.
The database does NOT contain all the trains, but only the last requests of the users: in this way it is not necessary to execute consecutive requests to the trenitalia sites.

The choice of the database was very difficult. Not so much for which database to use but for the version. Initially I was oriented towards MySQL, because from version 5.7.8 it is compatible with JSON data type: I need JSON as data type, for how are structured the responses of trenitalia.
Unfortunately MySQL 5.7.8 (or the version 8), despite a lot of attempts, is not compatible with either Debian 9 or Ubuntu 18.04.
I tried then with mariaDB, compatible with JSON from version 10.2 and it works very well. It has the same syntax as MySQL and python uses the same library (MySQLdb) to interface with MariaDB. Perfect!

## Debian 9

It is not relevant to the project, however ... Initially, TrainBot was operating on Raspian, a modified version of Debian 9 for RaspberryPi.
After the change of infrastructure TrainBot was developed both on Ubuntu 16.04 LTS and Debian 9 (currently still here)

## Amazon AWS and Google Cloud Platform

I tried both platforms above. The first was Amazon AWS with which I found myself very well creating a small virtual machine with ubuntu. Unfortunately, Amazon AWS has a very limited free trial and I had to find an alternative as valid (perhaps even better) to AWS: Google Cloud platform.

Google Cloud Platfom offers for free 730 hours per month for instances composed by a single vCPU with 0.6Gb of RAM. It's true, the free instance is very poor, but theoretically, however, quite powerful for the new bot: the optimizations and the redesign will contribute to a reduction of the use costs of CPU and RAM. This was already one of the objectives of my project and now it is even more so.

The Google Cloud Platform instance I currently use is configured with Debian 9 and mysql Ver 15.1 Distrib 10.3.7-MariaDB