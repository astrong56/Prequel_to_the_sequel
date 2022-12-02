#!/usr/bin/env python3
import requests

def get_wordpress_post():
    """Returns the wordpress post"""
    # user_url = 'http://13.59.180.96:8088/2022/12/02/test-message'
    # response = requests.get(f'{user_url}/wp-json/wp/v2/posts')
    response = requests.get(f'http://13.59.180.96:8088/wp-json/wp/v2/posts')
    data = response.json()
    return data

if __name__ == '__main__':
    wordpress_post = get_wordpress_post()
    print(wordpress_post)