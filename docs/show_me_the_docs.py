import webbrowser
import subprocess
import time
import os

# change the directory to the current path's directory
path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

time.sleep(3.0)

p = subprocess.Popen(['mkdocs', 'serve'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

# wait until the server has time to start before opening he web browser

time.sleep(5.0)

if p:
    url = 'http://127.0.0.1:8000'
    webbrowser.open_new(url=url)

# wait forever
p.wait()
