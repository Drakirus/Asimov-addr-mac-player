## Lan get Mac and User data

### Introduction

This application is a website for Asimov events, its aim is to 
win time during preparation of events and to fit with some legal rules. 
We are forced to save Mac adress, IP Addr, Name, Firstname of every person using
University's network.

So this website permits us to get those datas and get others informations about
somes aspects of current event.

### How does it work ?

Its a python script retrieving ip addr from client sending post datas on a page
hosted specifically for an event and just link this one to Mac addr using arp
table and regexp. Finally when IP addr and MAC addr are linked, the website
save them with Name, Firstname corresponding and with any further informations
wanted for a great event.


### For `python2`

```
sudo pip install -r requirements.txt
sudo python2 ./app.py
```
