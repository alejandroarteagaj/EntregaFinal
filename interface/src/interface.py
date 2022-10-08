# import the necessary packages
from tkinter import Tk, Button, Label, filedialog
import base64
from tkinter import *
from urllib import response
import PIL
import grpc
from PIL import Image
from PIL import ImageTk
import numpy as np

import backend_pb2
import backend_pb2_grpc


def select_image():
    # grab a reference to the image panels
    global panelA, backend_client,path
    text2.delete(1.0, "end")
    # open a file chooser dialog and allow the user to select an input
    # image
    path = filedialog.askopenfilename(
        initialdir="/",
        title="Select image",   
        filetypes=(
            ("JPEG", "*.jpeg"),
            ("jpg files", "*.jpg"),
            ("png files", "*.png"),
            ),
        )
     
    if path:
          global img1
          global array
          path_message = backend_pb2.img_path(path=path)
          response = backend_client.load_image(path_message)

          img_content = response.img_content
          img_w = response.width
          img_h = response.height
          
          img1 = img_content.resize((250, 250), PIL.Image.ANTIALIAS)
          img1 = ImageTk.PhotoImage(img1)
          text_img1.image_create(END, image=img1)
          
          
          
        
    
    # ensure a file path was selected
   

        



def Modelo():
       path_message = backend_pb2.img_path(path=path)
       response=backend_client.predict(path_message)
       text2.insert(END, response)
        

     
# initialize the window toolkit along with the two image panels
root = Tk()
panelA = None

# Backend client definition
channel = grpc.insecure_channel("backend:50051")
backend_client = backend_pb2_grpc.BackendStub(channel=channel)



# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI
btn = Button(root, text="Select an image", command=select_image)
btn1 = Button(root, text="Predecir", command=Modelo)
text2 = Text(root)
text_img1 = Text(root, width=200, height=100) ##Intento interface

btn.pack(side="right", fill="both", expand="no", padx="10", pady="10")
btn1.pack(side="left",fill="both",expand="no",padx="10",pady="40")
text2.place(x=5, y=10, width=120, height=30)

# kick off the GUI
root.mainloop()
