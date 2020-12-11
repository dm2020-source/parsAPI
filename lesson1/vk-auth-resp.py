import requests
import json


main_link = 'https://api.vk.com/method/friends.get?v=5.52&access_token=fbba9c2e8623b74216f2e0327fd17d621bb0c101120f1cafea9c7fbdab98803f34b0643049c178b3a0218'

r = requests.get(f'{main_link}')

with open('vk-response.json', 'w') as f:
    json.dump(r.json(), f)


