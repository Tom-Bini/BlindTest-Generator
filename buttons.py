import tkinter as tk

class CircleButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=50, height=50, 
                 padding=4, color="#282828", fg="white", hover_color="#383838", font=('Helvetica', 14)):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bg='#121212', bd=0)
        
        self.command = command
        self.color = color
        self.hover_color = hover_color
        self.disabled = False
        self.disabled_color = "#1a1a1a"
        self.disabled_fg = "#666666"
        self.normal_fg = fg
        self.font = font
        
        # Dessiner le cercle
        self.button = self.create_oval(padding, padding, 
                                     width-padding, height-padding, 
                                     fill=color, outline="")
        
        # Ajouter le texte
        self.text = self.create_text(width/2, height/2, text=text, 
                                   fill=fg, font=font)
        
        # Lier les événements
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.bind("<ButtonRelease-1>", self.on_release)
        
    def set_text(self, text):
        self.itemconfig(self.text, text=text)
        
    def config(self, **kwargs):
        if 'state' in kwargs:
            self.disabled = kwargs['state'] == 'disabled'
            if self.disabled:
                self.itemconfig(self.button, fill=self.disabled_color)
                self.itemconfig(self.text, fill=self.disabled_fg)
            else:
                self.itemconfig(self.button, fill=self.color)
                self.itemconfig(self.text, fill=self.normal_fg)
        elif 'text' in kwargs:
            self.itemconfig(self.text, text=kwargs['text'])
                
    def on_enter(self, e):
        if not self.disabled:
            self.itemconfig(self.button, fill=self.hover_color)
        
    def on_leave(self, e):
        if not self.disabled:
            self.itemconfig(self.button, fill=self.color)
        
    def on_click(self, e):
        if not self.disabled:
            self.itemconfig(self.button, fill=self.color)
        
    def on_release(self, e):
        if not self.disabled and self.command:
            self.itemconfig(self.button, fill=self.hover_color)
            self.command()

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=50, height=50, corner_radius=10, 
                 padding=8, color="#282828", fg="white", hover_color="#383838", font=('Helvetica', 14)):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bg='#000000', bd=0)
        
        self.command = command
        self.color = color
        self.hover_color = hover_color
        self.corner_radius = corner_radius
        self.disabled = False
        self.disabled_color = "#1a1a1a"
        self.disabled_fg = "#666666"
        self.normal_fg = fg
        
        # Dessiner le bouton arrondi
        self.button = self.create_rounded_rect(padding, padding, 
                                             width-padding, height-padding, 
                                             corner_radius, fill=color, outline="")
        
        # Ajouter le texte
        self.text = self.create_text(width/2, height/2, text=text, 
                                   fill=fg, font=font)
        
        # Lier les événements
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.bind("<ButtonRelease-1>", self.on_release)
        
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
        
    def config(self, **kwargs):
        if 'state' in kwargs:
            self.disabled = kwargs['state'] == 'disabled'
            if self.disabled:
                self.itemconfig(self.button, fill=self.disabled_color)
                self.itemconfig(self.text, fill=self.disabled_fg)
            else:
                self.itemconfig(self.button, fill=self.color)
                self.itemconfig(self.text, fill=self.normal_fg)
                
    def on_enter(self, e):
        if not self.disabled:
            self.itemconfig(self.button, fill=self.hover_color)
        
    def on_leave(self, e):
        if not self.disabled:
            self.itemconfig(self.button, fill=self.color)
        
    def on_click(self, e):
        if not self.disabled:
            self.itemconfig(self.button, fill=self.color)
        
    def on_release(self, e):
        if not self.disabled and self.command:
            self.itemconfig(self.button, fill=self.hover_color)
            self.command() 