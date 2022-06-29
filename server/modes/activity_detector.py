#!/usr/bin/python3
from tkinter import ACTIVE
# from pynput.mouse import Controller
from pynput import mouse, keyboard
import time

# mouse = Controller()

# before = mouse.position

# threshold = 20
# active = time.time()
# now = time.time()

# while True:
#     now = time.time()
#     current = mouse.position
#     if before != current:
#         active = time.time()
#         print('Movement detected')
    
#     if (now - active) > threshold:
#         print('Inactive for ', now-ACTIVE, 'seconds')

#     before = current




def on_move(x, y):
    print('Movement detected')

def on_click(x, y, button, pressed):
    print('Click detected')
    

def on_scroll(x, y, dx, dy):
    print('Scroll detected')

# Collect events until released
with mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll) as listener:
    listener.join()

# # ...or, in a non-blocking fashion:
# listener = mouse.Listener(
#     on_move=on_move,
#     on_click=on_click,
#     on_scroll=on_scroll)

# listener.start()
    


