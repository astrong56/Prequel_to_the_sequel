#!/usr/bin/env python3
import requests
import argparse
import datetime

parser = argparse.ArgumentParser(description='Enter Wordpress data')
parser.add_argument('-f', '--filename', type=str,  
                    help='''Enter the filename or a "-"''')
parser.add_argument('action', type=str,  default='read',
                    help='''Enter either "read" or "write"''')

args = parser.parse_args()
wordpress_file = args.filename
wordpress_action = args.action
blog_timestamp = datetime.datetime.now().isoformat(timespec = 'seconds')

def read_input_file(wordpress_file):
    with open(wordpress_file) as blog:
        blog_title = blog.readline().strip('\n')
        content = blog.readlines()
        blog_content = content[1:]
    return blog_title, blog_content


def get_newest_blog():
    """Returns the latest wordpress post"""
    response = requests.get(f'http://13.59.180.96:8088/wp-json/wp/v2/posts')
    data = response.json()
    blog_title = data[0]['title']['rendered']
    blog_content = data[0]['content']['rendered']
    print(blog_title)
    print(blog_content)
    return data


def post_blog(blog_title, blog_content):
    user='prequel'
    password='sequel'
    url1='http://13.59.180.96:8088/wp-login.php'
    url2='http://13.59.180.96:8088/wp-admin/post-new.php'
    headerauth= {'Cookie':'wordpress_test_cookie=WP Cookie check'}
    dataauth = {'log':user, 'pwd':password, 'wp-submit':'Log In'}
    # dataupload = {'post_id': '0', '_wp_http_referer': '/wp-admin/post-new.php', 'action': 'upload_attachement', 'html-upload': 'Upload'}
    # data to be sent to api
    data = {'title':blog_title, 'status':'publish', 'slug':'test-post', 'content':blog_content, 'date':blog_timestamp}
    # response = requests.post(url = 'http://13.59.180.96:8088/wp-json/wp/v2/posts', data = data)
    # extracting response text
    
    session1=requests.session()
    r1 = session1.post(url1, headers=headerauth, data=dataauth)
    r2 = session1.get(url2)
    r3 = session1.post(url2, json=data)
    return r1, r2, r3
    

if __name__ == '__main__':
    if wordpress_action == 'read' and wordpress_file == '':
        get_newest_blog()
    elif wordpress_action == 'write' and wordpress_file != '':
        blog_title, blog_content = read_input_file(wordpress_file)
        r1, r2, r3 = post_blog(blog_title, blog_content)
        print(r1, r2, r3)
    else:
        print('Invalid action entered.  Please try again!')