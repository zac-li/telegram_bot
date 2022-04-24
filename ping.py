import requests

print("Ping!!")
rsp = requests.get("https://shrouded-fjord-21568.herokuapp.com")
if rsp.status_code == 404:
    print("Fine!!")
else:
    print("Shit!!")
