import tkinter as tk
from tkinter import ttk
import pickle

LARGEFONT = ("Verdana", 35)

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.attributes('-fullscreen', True)
        self.bind('<Escape>', self.exit_fullscreen)
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Page1, Page2):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Page1)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def exit_fullscreen(self, event=None):
        self.attributes('-fullscreen', False)

# Page 1 -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=4)

        subframe = tk.Frame(self, background="gray")
        subframe.grid_rowconfigure(0, weight=1)
        subframe.grid_columnconfigure(0, weight=1)
        subframe.grid_propagate(False)

        subject = tk.Label(subframe, text="Subject")
        subject.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        subframe.grid(row=0, column=0, sticky="nsew")

        button1 = ttk.Button(subframe, text="Page 2", command=lambda: controller.show_frame(Page2))
        button1.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        subframe2 = tk.Frame(self, background="darkgray")
        message = tk.Label(subframe2, text="Message")
        message.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        subframe2.grid(row=0, column=1, sticky="nsew")

    #Page 1 Functions



# Page 2 -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=4)

        subframe = tk.Frame(self, background="gray")
        subframe.grid_rowconfigure(0, weight=1)
        subframe.grid_columnconfigure(0, weight=1)
        subframe.grid_propagate(False)
        
        subject = tk.Label(subframe, text="Subject")
        subject.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        subframe.grid(row=0, column=0, sticky="nsew")

        button1 = ttk.Button(subframe, text="Page 1", command=lambda: controller.show_frame(Page1))
        button1.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        self.inputtxt = tk.Text(subframe, height=5, width=30, bg="white")
        self.inputtxt.grid(row=1, column=0, padx=10, pady=10, sticky="n")

        self.printButton = tk.Button(subframe, text="Translate", command=self.update_and_draw)
        self.printButton.grid(row=2, column=0, padx=10, pady=10, sticky="n")

        subframe2 = tk.Frame(self, background="darkgray")
        subframe2.grid(row=0, column=1, sticky="nsew")
        subframe2.grid_columnconfigure(0, weight=1)
        subframe2.grid_rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(subframe2, width=750, height=750, bg='white')
        self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.load_data()

    # Page 2 Functions    

    def load_data(self):
        try:
            with open('./data.pickle', 'rb') as f:
                data_dict = pickle.load(f)
                self.data = data_dict['data']
                self.labels = data_dict['labels']
        except FileNotFoundError:
            print("Error: data.pickle file not found.")
        except Exception as e:
            print(f"Error loading data: {e}")

    def drawhand(self):
        print("hand drawn")
        self.canvas.delete("all")
        if hasattr(self, 'data') and hasattr(self, 'labels'):
            if dataint is not None and dataint < len(self.data):
                hand_data = self.data[dataint]

                for i in range(0, len(hand_data), 2):
                    x = hand_data[i] * 500 * 2 + 100
                    y = hand_data[i+1] * 500 * 2 + 100
                    self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="red")

                lines = [(0, 1), (1, 2), (2, 3), (3, 4),
                        (0, 5), (5, 6), (6, 7), (7, 8),
                        (9, 10), (10, 11), (11, 12),
                        (13, 14), (14, 15), (15, 16),
                        (0, 17), (17, 18), (18, 19), (19, 20),
                        (5, 9), (9, 13), (13, 17)]

                for line in lines:
                    x1 = hand_data[line[0]*2] * 500 * 2 + 100
                    y1 = hand_data[line[0]*2+1] * 500 * 2 + 100
                    x2 = hand_data[line[1]*2] * 500 * 2 + 100
                    y2 = hand_data[line[1]*2+1] * 500 * 2 + 100
                    self.canvas.create_line(x1, y1, x2, y2, fill="black", width=15)
            else:
                print("Invalid dataint or data not found.")
        else:
            print("Data or labels not loaded.")

    def update_and_draw(self):
        global dataint
        input_text = self.inputtxt.get("1.0", "end-1c")
        if input_text == "A" or input_text == "a":
            dataint = 1
        elif input_text == "B" or input_text == "b":
            dataint = 980
        elif input_text == "C" or input_text == "c":
            dataint = 7000
        elif input_text == "D" or input_text == "d":
            dataint = 10800
        elif input_text == "E" or input_text == "e":
            dataint = 11200
        elif input_text == "F" or input_text == "f":
            dataint = 12200
        elif input_text == "G" or input_text == "g":
            dataint = 12600
        elif input_text == "H" or input_text == "h":
            dataint = 13000
        elif input_text == "I" or input_text == "i":
            dataint = 13500
        elif input_text == "J" or input_text == "j":
            dataint = None
        elif input_text == "K" or input_text == "k":
            dataint = 1500
        elif input_text == "L" or input_text == "l":
            dataint = 2100
        elif input_text == "M" or input_text == "m":
            dataint = 2500
        elif input_text == "N" or input_text == "n":
            dataint = 3000
        elif input_text == "O" or input_text == "o":
            dataint = 3600
        elif input_text == "P" or input_text == "p":
            dataint = 4500
        elif input_text == "Q" or input_text == "q":
            dataint = 5000
        elif input_text == "R" or input_text == "r":
            dataint = 5600
        elif input_text == "S" or input_text == "s":
            dataint = 6000
        elif input_text == "T" or input_text == "t":
            dataint = 6350
        elif input_text == "U" or input_text == "u":
            dataint = 7500
        elif input_text == "V" or input_text == "v":
            dataint = 8100
        elif input_text == "W" or input_text == "w":
            dataint = 9200
        elif input_text == "X" or input_text == "x":
            dataint = 9500
        elif input_text == "Y" or input_text == "y":
            dataint = 10200
        elif input_text == "Z" or input_text == "z":
            dataint = None
        else:
            dataint = None  
        self.drawhand()
        self.resettxt()

    def resettxt(self):
        self.inputtxt.delete("1.0", "end")
        print("reset")

app = tkinterApp()
app.mainloop()
