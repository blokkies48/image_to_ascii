from PIL import Image, ImageGrab
import tkinter as tk
from tkinter import Text, INSERT, filedialog, Scale, Label
from datetime import datetime


'''
Simply run this script to have ascii fun!
'''
class App:
    size_v = (100, 50)

    image_selected = "cat.png"

    # Gen ascii aglo
    def image_to_ascii(self,file_path):
        # Open the image file
        with Image.open(file_path) as img:
            # Resize the image to a smaller size
            img = img.resize(self.size_v)
            # Convert the image to grayscale
            img = img.convert("L")
            # Define the ASCII characters to use
            characters = "@#123456789htoacsi;:'*^•+=~-,.  "[::-1]
            # Get the pixel values of the image
            pixels = img.getdata()
            # Iterate over the pixels and convert them to ASCII characters
            ascii_image = "".join([characters[pixel // 8] for pixel in pixels])
            # Split the ASCII image into lines
            ascii_image = "\n".join([ascii_image[i:i+img.width] for i in range(0, len(ascii_image), img.width)])
            return ascii_image



    def upload_image(self):

        root.image_selected = filedialog.askopenfilename(initialdir="/Pictures", title="Select a file", filetypes = (('PNG', '*.png'),('JPEG', ('*.jpg', '*.jpeg', '*.jpe')), ("all files", "*.*")))
        self.display_image()

    def display_image(self):
        global text
        text=Text(root,name="text_box", width=self.size_v[0], height=self.size_v[1])
        text.tag_configure("center", justify='center',background='black', foreground='white')

        text.insert(INSERT, self.image_to_ascii(root.image_selected))
        text.pack()

        # Add the tag from start to end text
        text.tag_add("center", 1.0, "end")
        

    def save_pic(self):

        # Use for saving the image name
        now = datetime.now().strftime("%H%M%S")
        # Save image type
        result = filedialog.asksaveasfilename(initialdir="/Pictures", title="Select file",
        initialfile=f"{now}.jpeg",
        filetypes=(
            ('JPEG', ('*.jpg', '*.jpeg', '*.jpe')), ('PNG', '*.png'), ('BMP', ('*.bmp', '*.jdib')), ('GIF', '*.gif')))

        # Save image
        if result:
            x = text.winfo_rootx()
            y = text.winfo_rooty()
            height = text.winfo_height() + y
            width = text.winfo_width() + x

            ImageGrab.grab().crop((x, y, width, height)).save(result)

    def resize(self):
        self.size_v = (scale_1.get(), scale_2.get())
        self.display_image()
        
root: tk = tk.Tk()
root.title("Image to ascii conversion")
root.configure(bg='black')
root.geometry("1000x900")

tk.Button(root,text="Save",command=App().save_pic, height=2, width= 1000).pack()

root.image_selected = "cat.png"

tk.Button(root,text="Upload",command=App().upload_image, height=2, width= 1000).pack()
tk.Button(root,text="Resize",command=App().resize, height=2, width= 1000).pack()

scale_1 = Scale(root, from_=0, to=100, orient='horizontal')
scale_1.pack()
scale_2 = Scale(root, from_=0, to=70, orient='horizontal')
scale_2.pack()


root.mainloop()
        