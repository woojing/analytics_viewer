# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk

root = Tk()
root.title("ADB GA log formater")

mainframe = ttk.Frame(root, padding='3 3 3 3')
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(1, weight=1)

filter_string = StringVar()
filter_entry = ttk.Entry(mainframe, textvariable=filter_string)
filter_entry.grid(row=0, columnspan=2, sticky=(W, N))

log_text = Text(mainframe)
log_text.grid(row=1, sticky=(N, W, E, S))
log_text_scrollbar = ttk.Scrollbar(mainframe, orient=VERTICAL, command=log_text.yview)
log_text_scrollbar.grid(column=1, row=1, sticky=(N,S))
log_text['yscrollcommand'] = log_text_scrollbar.set

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

filter_entry.focus()


import queue
import subprocess
import threading
import sys
from helper import parse_params, map_params
from pprint import pprint, pformat
import datetime


class AsynchronousFileReader(threading.Thread):
    '''
    Helper class to implement asynchronous reading of a file
    in a separate thread. Pushes read lines on a queue to
    be consumed in another thread.
    '''

    def __init__(self, fd, queue_):
        assert isinstance(queue_, queue.Queue)
        assert callable(fd.readline)
        threading.Thread.__init__(self)
        self._fd = fd
        self._queue = queue_

    def run(self):
        '''The body of the tread: read lines and put them on the queue.'''
        for line in iter(self._fd.readline, None):
            if line == b'': break
            # self._queue.put(line.decode('utf-8').strip())
            parsed_dict = map_params(parse_params(line.decode('utf-8').strip()))
            if parsed_dict == {}: continue
            log_text.insert(END, "\n" + pformat(datetime.datetime.now()) + "\n")
            log_text.insert(END, pformat(parsed_dict) + "\n")
            log_text.see(END)

    def eof(self):
        '''Check whether there is no more content to expect.'''
        return not self.is_alive() and self._queue.empty()


# You'll need to add any command line arguments here.
process = subprocess.Popen(['adb', "logcat", "-s", "GAv4"], stdout=subprocess.PIPE)

# Launch the asynchronous readers of the process' stdout.
stdout_queue = queue.Queue()
stdout_reader = AsynchronousFileReader(process.stdout, stdout_queue)
stdout_reader.start()

# Check the queues if we received some output (until there is nothing more to get).
# try:
#     while not stdout_reader.eof():
#         while not stdout_queue.empty():
#             line = stdout_queue.get()
#             print(datetime.datetime.now())
#             pprint(map_params(parse_params(line)))
# except (KeyboardInterrupt, SystemExit):
#     process.kill()
#     stdout_reader.join()
#     sys.exit()

root.mainloop()
process.kill()
