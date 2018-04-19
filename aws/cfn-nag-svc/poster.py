import requests
import sys

the_data = None

with open(sys.argv[1], 'rb') as food:
    the_data = food.read()

r = requests.post('http://localhost:8080/scan', data=the_data)

print(r.content)
