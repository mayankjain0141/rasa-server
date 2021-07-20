import requests

url = 'http://192.168.1.34:5000/'

myobj = {
  "sid": "132",
  "message" : "hi",
  "game": "model1"
}


for i in range(1000):
    x = requests.post(url, json = myobj)
    print(x)


