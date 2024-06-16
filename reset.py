import libtmux
import os
import time
import requests
def checkServer():
        url = "http://vietanhnd.site:8080/captcha"

        payload = {'captcha': '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',
        'key': 'f1a00870-6c07-485a-a74d-7f09bc6aaef1',
        'data': 'A0u0efZROjGqbK8EdDRXi9pKAxebhFf5WQJs0K+cfB2fZx5I2hs0/u6vbpguCMQZ2bWJQQMQkYKnt8dL37IoDbshZv9fbjdCkyJz6ldzmShYpSypb2ssK6KoYdGQ8arwTv3zc7ktCLK+EgCZlocUSH2p/0ABXW1mvQOKi51sAM4=',
        '': ''}
        files=[]
        headers = {}
        try:
            response = requests.request("POST", url, headers=headers, data=payload,files=files)
            print(response.status_code)
        except:
            return 508
        return response.status_code
def kill_tmux_session(session_name):
    try:
        server = libtmux.Server()
        session = server.find_where({"session_name": session_name})

        if session is not None:
            session.kill_session()
    except:
        pass
def create_tmux_session(session_name):
    try:
        server = libtmux.Server()
        session = server.new_session(session_name)
    except:
        pass
# Specify the name of the tmux session you want to create
session_name = 'my_tmux_session'

# Call the function to create the session
#create_tmux_session(session_name)
# Specify the name of the tmux session you want to kill
session_name = 'test'

# Call the function to kill the session
#kill_tmux_session(session_name)
def run_command_in_tmux(session_name, command, working_directory):
    try:
        server = libtmux.Server()
        session = server.find_where({"session_name": session_name})

        if session is not None:
            window = session.windows[0]

            if window is not None:
                pane = window.attached_pane

                if pane is not None:
                    # Change the current working directory
                    pane.send_keys("cd {}".format(working_directory), enter=False)
                    pane.send_keys("C-m")

                    # Run the command in the updated working directory
                    pane.send_keys(command)
    except:
        pass

# Specify the details of the tmux session, window, command, and working director                                                                                                                                                                                                                                                                                                             y
session_name = '1'
command = 'python3 app.py'
working_directory = '/root/captchaServer'

delta=5*60*60
lastTime=int(time.time())
while True:
    currentTime=int(time.time())
    response=checkServer()
    if(response!=200):
        kill_tmux_session(session_name)
        create_tmux_session(session_name)
        run_command_in_tmux(session_name,command,working_directory)
    if(currentTime-lastTime>delta):
        print("run oke")
        lastTime=currentTime
        kill_tmux_session(session_name)
        create_tmux_session(session_name)
# Call the ifunction to change directory and run the command within the tmux ses                                                                                                                                                                                                                                                                                                             sion
        run_command_in_tmux(session_name, command, working_directory)
    time.sleep(300)
