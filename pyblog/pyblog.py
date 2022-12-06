#!/usr/bin/env python3
import requests
import argparse
import datetime
import os

parser = argparse.ArgumentParser(description='Enter Wordpress data')
parser.add_argument('-f', '--filename', type=str,  
                    help='''Enter the filename or a "-"''')
parser.add_argument('action', type=str,  default='read',
                    help='''Enter either "read" or "write"''')

args = parser.parse_args()
wordpress_file = args.filename
wordpress_action = args.action
blog_timestamp = datetime.datetime.now().isoformat(timespec = 'seconds')
wordpress_api_id = os.environ.get('WORDPRESS_USER')
wordpress_api_pw = os.environ.get('WORDPRESS_PWD')
wordpress_site = os.environ.get('WORDPRESS_URL')
# wordpress_api_id = 'prequel'
# wordpress_api_pw = 'GJTe Qe6Y Ejfi gkQ1 r2fO qz5H'


def read_input_file(wordpress_file):
    with open(wordpress_file) as blog:
        blog_title = blog.readline().strip('\n')
        content = blog.readlines()
        blog_content = content[1:]
    return blog_title, blog_content


def get_newest_blog():
    """Returns the latest wordpress post"""
    response = requests.get(f'{wordpress_site}/wp-json/wp/v2/posts')
    data = response.json()
    blog_title = data[0]['title']['rendered']
    blog_content = data[0]['content']['rendered']
    print(blog_title)
    print(blog_content)
    return data


def post_blog(blog_title, blog_content):
    # data to be sent to api
    data = {'title':blog_title, 'status':'publish', 'content':blog_content, 'date':blog_timestamp}
    response = requests.post(url = f'{wordpress_site}/wp-json/wp/v2/posts', 
    auth=(wordpress_api_id, wordpress_api_pw), data = data)
    return response
    

if __name__ == '__main__':
    if wordpress_action == 'read' and wordpress_file == None:
        get_newest_blog()
    elif wordpress_action == 'write' and wordpress_file != None:
        blog_title, blog_content = read_input_file(wordpress_file)
        response = post_blog(blog_title, blog_content)
        print(response)
    else:
        print('Invalid action entered.  Please try again!')