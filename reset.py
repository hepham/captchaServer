import libtmux
import os
import time
def kill_tmux_session(session_name):
    server = libtmux.Server()
    session = server.find_where({"session_name": session_name})
    
    if session is not None:
        session.kill_session()
def create_tmux_session(session_name):
    server = libtmux.Server()
    session = server.new_session(session_name)

# Specify the name of the tmux session you want to create
session_name = 'my_tmux_session'

# Call the function to create the session
#create_tmux_session(session_name)
# Specify the name of the tmux session you want to kill
session_name = 'test'

# Call the function to kill the session
#kill_tmux_session(session_name)
def run_command_in_tmux(session_name, command, working_directory):
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

# Specify the details of the tmux session, window, command, and working directory
session_name = '1'
command = 'python3 app.py'
working_directory = '/root/captchaServer'

delta=5*60*60
lastTime=int(time.time())
while True:
    currentTime=int(time.time())
    if(currentTime-lastTime>delta):
        print("run oke")
        lastTime=currentTime
        kill_tmux_session(session_name)
        create_tmux_session(session_name)
# Call the ifunction to change directory and run the command within the tmux session
        run_command_in_tmux(session_name, command, working_directory)
    time.sleep(300)
