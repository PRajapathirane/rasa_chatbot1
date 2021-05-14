import requests
#import numpy as np
from random import seed
from random import randint

def EntertainUser():
    url = 'http://api.mediastack.com/v1/news?access_key=7b54abd9c81a45036e46c77f80bbeb4b&categories=entertainment'

    json_data = requests.get(url).json()
    format_add = json_data["data"]
    return format_add

# format_a = EntertainUser()
# # print(format_a)
# # x = format_a[7]
# # print(x)
# x = (format_a[randint(0,25)])
# print(x['title'],x['url'])
#print(randint(5,188))


def News_Provider(category, channel):

    api_address = 'http://api.mediastack.com/v1/news?access_key=7b54abd9c81a45036e46c77f80bbeb4b&'

    url = api_address + 'categories=' + category + '&sources=' + channel
    json_data = requests.get(url).json()
    format_add = json_data["data"]
    return format_add
