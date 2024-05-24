import os
import sys
import subprocess
import re
import threading
import keyboard
import queue

stdout_lines = []
stderr_lines = []
progress = []
directory_queue = queue.Queue()
discovered_directories = set()
ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
directory_pattern = re.compile(r'[2]0+')

def get_args():
    args = []
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            args.append(sys.argv[i])
    else:
        print("No Arguments provided")
    return args

def process_lines(stream, storage_list, event, host):
    try:
        for line in iter(stream.readline, ''):
            clean_line = ansi_escape.sub('', line)
            if "Progress:" in clean_line:
                progress.append(clean_line)
                continue
            print(clean_line, end='')  
            storage_list.append(clean_line)  

            dir_match = directory_pattern.search(clean_line)
            if dir_match:
                directory = clean_line.split(' ')[0]
                if directory not in discovered_directories:
                    discovered_directories.add(host + directory)
                    directory_queue.put(host + directory)
    finally:
        event.set()
        

def process_spacebar():
    global progress
    while True:
        keyboard.wait('space')
        if progress:
            print(progress[-1])

def gobuster(command, host):

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)

    stdout_event = threading.Event()
    stderr_event = threading.Event()

    try: 
        stdout_thread = threading.Thread(target=process_lines, args=(process.stdout, stdout_lines, stdout_event, host))
        stderr_thread = threading.Thread(target=process_lines, args=(process.stderr, stderr_lines, stderr_event, host))

        stdout_thread.start()
        stderr_thread.start()

        stdout_event.wait()
        stderr_event.wait()
        process.wait()

    except KeyboardInterrupt:
        process.terminate()
        stdout_thread.join()
        stderr_thread.join()
        response = input('\nPress x to exit or Enter to continue to the next directory')
        if response == 'x':
            exit()
        
if __name__ == '__main__':

    args = get_args()
    host = args[args.index('-u') + 1]
    if (host[-1] == '/'):
        host = host[:-1]
    directory_queue.put(host)

    spacebar_thread = threading.Thread(target=process_spacebar, daemon=True)
    spacebar_thread.start()
    while not directory_queue.empty():
        stdout_lines = []
        new_url = directory_queue.get()
        base_url_index = args.index('-u') + 1
        args[base_url_index] = new_url
        command = ['gobuster'] + args
        print(f"Scanning directory: {command}")
        gobuster(command, args[base_url_index])
        os.makedirs('GobusterBuster/', exist_ok=True)
        stdout_output = ''.join(stdout_lines)
        host_file = args[base_url_index].replace('http://', '').replace('https://', '').replace('/', '_')
        with open('GobusterBuster/' + host_file, 'w') as f:
            f.write(stdout_output)
        
