#!/usr/bin/env python3
import requests
import argparse
import datetime
import os
import fileinput

parser = argparse.ArgumentParser(description='Enter Wordpress data')
parser.add_argument('-f', '--filename', type=str,  
                    help='''Enter the filename''')
parser.add_argument('action', type=str,  default='read',
                    help='''Enter either "read" or "write"''')

args = parser.parse_args()
wordpress_file = args.filename
wordpress_action = args.action
blog_timestamp = datetime.datetime.now().isoformat(timespec = 'seconds')
wordpress_api_id = os.environ.get('WORDPRESS_USER')
wordpress_api_pw = os.environ.get('WORDPRESS_PWD')
wordpress_site = os.environ.get('WORDPRESS_URL')

def read_std_input():
    with fileinput.input(files=(wordpress_file)) as f:
        for line in f:
            if fileinput.isfirstline() == True:
                blog_title = line
            else:
                lines = []
                lines.append(line)
                blog_content = '\n'.join(lines)
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
    elif wordpress_action == 'write':
        try:
            blog_title, blog_content = read_std_input()
            try:
                response = post_blog(blog_title, blog_content)
                if response.status_code == 201:
                    print(response)
                else:
                    print('unable to post blog due to HTTP error:', response)
            except Exception as e2:
                print('unable to reach blog due to error:', e2)
        except Exception as e1:
            print(e1)
        
    else:
        print('Invalid action entered.  Please try again!')