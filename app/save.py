import os
from flask import render_template
from threading import Thread

def write_to_file(path, name, msg):
    with open(os.path.join(path, name)+'.html', 'w') as f:
        f.write(msg)

def save_to_file(path, name, template, **kwargs):
    msg = render_template(template, **kwargs) 
    thr = Thread(target=write_to_file, args=[path, name, msg])
    thr.start()
    return thr
