from flask_mongoalchemy import *

import re

def video_id_from_url(url):
    """Grabs an video id from a YouTube url to be used in an iframe.
    
    YouTube urls are either in the form
    'https://www.youtube.com/watch?v=<video_id>' or
    'https://youtu.be/<video_id>'. This function can extract the id from either
    type of url.
    """
    if url.find('youtu') >= 0:
        embed = re.split('[/=]', url)[-1]
    else:
        embed = ''
    return embed
