import tkinter as tk
import math
import time
import threading

class FadeAnimation:
    def __init__(self, widget, duration=0.3, steps=20):
        self.widget = widget
        self.duration = duration
        self.steps = steps
        self.is_running = False
        self.thread = None
        
    def fade_out(self, callback=None):
        if self.is_running:
            return
            
        self.is_running = True
        self.thread = threading.Thread(target=self._fade_out_animation, args=(callback,))
        self.thread.start()
        
    def fade_in(self, callback=None):
        if self.is_running:
            return
            
        self.is_running = True
        self.thread = threading.Thread(target=self._fade_in_animation, args=(callback,))
        self.thread.start()
        
    def _fade_out_animation(self, callback):
        for i in range(self.steps):
            if not self.is_running:
                break
            alpha = 1 - (i / self.steps)
            self.widget.attributes('-alpha', alpha)
            time.sleep(self.duration / self.steps)
        self.is_running = False
        if callback:
            callback()
            
    def _fade_in_animation(self, callback):
        for i in range(self.steps):
            if not self.is_running:
                break
            alpha = i / self.steps
            self.widget.attributes('-alpha', alpha)
            time.sleep(self.duration / self.steps)
        self.is_running = False
        if callback:
            callback()
            
    def stop(self):
        self.is_running = False
        if self.thread:
            self.thread.join()

class SlideAnimation:
    def __init__(self, widget, direction='left', duration=0.3, steps=20):
        self.widget = widget
        self.direction = direction
        self.duration = duration
        self.steps = steps
        self.is_running = False
        self.thread = None
        self.original_x = widget.winfo_x()
        self.original_y = widget.winfo_y()
        
    def slide_out(self, callback=None):
        if self.is_running:
            return
            
        self.is_running = True
        self.thread = threading.Thread(target=self._slide_out_animation, args=(callback,))
        self.thread.start()
        
    def slide_in(self, callback=None):
        if self.is_running:
            return
            
        self.is_running = True
        self.thread = threading.Thread(target=self._slide_in_animation, args=(callback,))
        self.thread.start()
        
    def _slide_out_animation(self, callback):
        start_x = self.original_x
        end_x = start_x - 100 if self.direction == 'left' else start_x + 100
        
        for i in range(self.steps):
            if not self.is_running:
                break
            progress = i / self.steps
            current_x = start_x + (end_x - start_x) * progress
            self.widget.place(x=current_x, y=self.original_y)
            time.sleep(self.duration / self.steps)
            
        self.is_running = False
        if callback:
            callback()
            
    def _slide_in_animation(self, callback):
        start_x = self.original_x - 100 if self.direction == 'left' else self.original_x + 100
        end_x = self.original_x
        
        for i in range(self.steps):
            if not self.is_running:
                break
            progress = i / self.steps
            current_x = start_x + (end_x - start_x) * progress
            self.widget.place(x=current_x, y=self.original_y)
            time.sleep(self.duration / self.steps)
            
        self.is_running = False
        if callback:
            callback()
            
    def stop(self):
        self.is_running = False
        if self.thread:
            self.thread.join() 