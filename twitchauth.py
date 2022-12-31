import requests
from urllib.parse import urlencode
from clientshit import client_id , client_secret

query_string = urlencode({'client_id': client_id, 'client_secret': client_secret, "grant_type": "client_credentials"})

#r format is good for url stringsand, a \ is a special character in a string
twitch_url_prefix = r'https://id.twitch.tv/oauth2/token?'

finished_endpoint = twitch_url_prefix + query_string

#meta data that I have to send behind the scenes with your post request
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

#Send the post request with the correct header 
respond = requests.post(finished_endpoint, headers=headers)

#print content contents (do off stream)
print(respond.content, "sockheadrps is the F####ing man")
