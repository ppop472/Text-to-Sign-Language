import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import pickle
import cv2
from PIL import Image, ImageTk
import mediapipe as mp
import numpy as np

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
            frame = F(container, self, root=self)
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
    def __init__(self, parent, controller, root, video_source=0):
        
        style = Style()
        style.configure('TButton', font =
                    ('calibri', 20, 'bold'),
                            borderwidth = '4')
        style.map('TButton', foreground = [('active', '!disabled', 'Blue')],
                            background = [('active', 'black')])
        
        tk.Frame.__init__(self, parent)
        self.root = root
        self.video_source = video_source
        self.controller = controller
        
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

        button1 = ttk.Button(subframe, text="Tekst naar Gebarentaal", command=lambda: controller.show_frame(Page2))
        button1.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        subframe = tk.Frame(self, background="darkgray")
        message = tk.Label(subframe, text="Message")
        message.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        subframe.grid(row=0, column=1, sticky="nsew")

        self.canvas = tk.Canvas(subframe, width=750, height=550, bg='white')
        self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Load the hand recognition model
        self.model_dict = pickle.load(open('./model.p', 'rb'))
        self.model = self.model_dict['model']

        # Set up MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles 
        self.hands = self.mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)
        self.labels_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G',
                            7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N',
                            14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V',
                            22: 'W', 23: 'X', 24: 'Y', 25: 'Z'}

        # Set up the video source
        self.vid = cv2.VideoCapture(video_source)
        self.photo = None
        self.update()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            # Convert the frame to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = self.hands.process(frame_rgb)
            data_aux = []
            x_ = []
            y_ = []
            H, W, _ = frame.shape

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks[:2]:
                    self.mp_drawing.draw_landmarks(
                        frame_rgb, hand_landmarks, self.mp_hands.HAND_CONNECTIONS, 
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style()
                    )

                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        x_.append(x)
                        y_.append(y)

                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        data_aux.append(x - min(x_))
                        data_aux.append(y - min(y_))

                x1 = int(min(x_) * W)
                y1 = int(min(y_) * H)
                x2 = int(max(x_) * W)
                y2 = int(max(y_) * H)

                if len(data_aux) == 42:
                    data_aux.extend([0] * 42)

                if len(data_aux) == 84:
                    prediction = self.model.predict([np.asarray(data_aux)])
                    predicted_character = self.labels_dict[int(prediction[0])]

                    cv2.rectangle(frame_rgb, (x1, y1), (x2, y2), (0, 0, 0), 4)
                    cv2.putText(frame_rgb, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3, cv2.LINE_AA)
                else:
                    print(f"Unexpected feature vector size: {len(data_aux)}")

            # Resize frame to fit the canvas
            frame_rgb = cv2.resize(frame_rgb, (750, 550))
            
            # Convert the image to a format Tkinter can use
            image = Image.fromarray(frame_rgb)
            self.photo = ImageTk.PhotoImage(image)

            # Update the canvas with the new frame
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        # Call update method again after 10 ms
        self.root.after(10, self.update)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
        self.hands.close()

# Page 2 -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Page2(tk.Frame):
    def __init__(self, parent, controller, root=None):
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

        button1 = ttk.Button(subframe, text="Gebarentaal naar Tekst", command=lambda: controller.show_frame(Page1))
        button1.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        self.inputtxt = tk.Text(subframe, height=5, width=30, bg="white")
        self.inputtxt.grid(row=1, column=0, padx=10, pady=10, sticky="n")

        style = Style()
        style.configure('TButton', font =
                    ('calibri', 20, 'bold'),
                            borderwidth = '4')
        style.map('TButton', foreground = [('active', '!disabled', 'Blue')],
                            background = [('active', 'black')])
        

        self.printButton = ttk.Button(subframe, text="Translate", command=self.update_and_draw)
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
            dataint = 11700
        elif input_text == "E" or input_text == "e":
            dataint = 12600
        elif input_text == "F" or input_text == "f":
            dataint = 13000
        elif input_text == "G" or input_text == "g":
            dataint = 13500
        elif input_text == "H" or input_text == "h":
            dataint = 14000
        elif input_text == "I" or input_text == "i":
            dataint = 14500
        elif input_text == "J" or input_text == "j":
            dataint = 15500
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
            dataint = 11200
        else:
            dataint = None  
        self.drawhand()
        self.resettxt()

    def resettxt(self):
        self.inputtxt.delete("1.0", "end")
        print("reset")

app = tkinterApp()
app.mainloop()