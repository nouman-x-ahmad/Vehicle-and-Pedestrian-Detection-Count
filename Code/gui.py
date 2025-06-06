import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk

class VideoSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video ROI Selector")

        self.canvas = tk.Canvas(root)
        self.canvas.pack()

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        tk.Button(self.button_frame, text="Select Video", command=self.select_video).pack(side="left")
        tk.Button(self.button_frame, text="Start", command=self.start_processing).pack(side="left")

        self.rect = None
        self.start_x = self.start_y = self.end_x = self.end_y = 0
        self.roi = None
        self.frame = None

    def select_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
        if not file_path:
            return
        self.cap = cv2.VideoCapture(file_path)
        ret, self.frame = self.cap.read()
        if not ret:
            print("Couldn't read video.")
            return
        self.display_frame(self.frame)
        self.canvas.bind("<ButtonPress-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def display_frame(self, frame):
        self.tk_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        self.canvas.config(width=self.tk_image.width(), height=self.tk_image.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def on_click(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event):
        self.end_x = event.x
        self.end_y = event.y
        self.roi = (min(self.start_x, self.end_x), min(self.start_y, self.end_y),
                    max(self.start_x, self.end_x), max(self.start_y, self.end_y))
        print("ROI selected:", self.roi)

    def start_processing(self):
        if self.roi is None:
            print("Please select ROI first.")
            return
        self.root.destroy()  # Close GUI and continue in main
