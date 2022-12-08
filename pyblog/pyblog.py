#!/usr/bin/env python3
import requests
import argparse
import datetime
import os
import fileinput

parser = argparse.ArgumentParser(description='''Gets Wordpress action of "read" or "upload", and if "upload", 
                                gets the filename''')
parser.add_argument('-f', '--filename', type=str,  
                    help='''Enter the local filepath/name you want to upload to a blog''')
parser.add_argument('action', type=str, help='''Enter either "read" or "upload"''')

args = parser.parse_args()
wordpress_file = args.filename
wordpress_action = args.action
blog_timestamp = datetime.datetime.now().isoformat(timespec = 'seconds')
wordpress_api_id = os.environ.get('WORDPRESS_USER')
wordpress_api_pw = os.environ.get('WORDPRESS_PWD')
wordpress_site = os.environ.get('WORDPRESS_URL')

def get_newest_blog():
    # Returns the latest wordpress blog post and sends it to standard output.
    response = requests.get(f'{wordpress_site}/wp-json/wp/v2/posts')
    data = response.json()
    blog_title = data[0]['title']['rendered']
    blog_content = data[0]['content']['rendered']
    print(blog_title)
    print(blog_content)
    return data
    
def read_std_input():
    # Reads the contents of the file that is being uploaded.
    # The first line of the file becomes the title, and the rest is the blog contents.
    with fileinput.input(files=(wordpress_file)) as f:
        for line in f:
            if fileinput.isfirstline() == True:
                blog_title = line
            else:
                lines = []
                lines.append(line)
                blog_content = '\n'.join(lines)
    return blog_title, blog_content

def post_blog(blog_title, blog_content):
    # Posts the blog title and contents gathered from the previous function to the wordpress site.
    data = {'title':blog_title, 'status':'publish', 'content':blog_content, 'date':blog_timestamp}
    response = requests.post(url = f'{wordpress_site}/wp-json/wp/v2/posts', 
    auth=(wordpress_api_id, wordpress_api_pw), data = data)
    return response

if __name__ == '__main__':
    if wordpress_action == 'read' and wordpress_file == None:
        get_newest_blog()
    elif wordpress_action == 'read' and wordpress_file != None:
        print('ERROR -- you cannot enter both "read" and a filename to upload')
    elif wordpress_action == 'upload' and wordpress_file == None:
        print('ERROR -- you cannot enter "upload" and not enter a filename')
    elif wordpress_action == 'upload' and wordpress_file != None:
        try:
            blog_title, blog_content = read_std_input()
            try:
                response = post_blog(blog_title, blog_content)
                if response.status_code == 201:
                    print('SUCCESS -- Your file was successfully uploaded to the blog!')
                else:
                    print('ERROR -- Unable to post blog due to an HTTP/Server error:', response)
            except Exception as e2:
                print('ERROR -- Unable to reach blog due to a connection error:', e2)
        except Exception as e1:
            print("ERROR -- No such file or directory found.")      
    else:
        print('ERROR -- invalid action entered.  Please enter either "read" or "upload -f", followed by a filename!')