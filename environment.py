from os import path
import os

def content(*paths):
    root = os.environ.get('CONTENT_ROOT', '/content')
    return path.join(root, *paths)

def drive(*paths):
    return content('drive', *paths)
