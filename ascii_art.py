from PIL import Image, ImageGrab
import tkinter as tk
from tkinter import Text, INSERT, filedialog, Scale
from datetime import datetime
from dropbox_save import SaveToDropbox


'''
Simply run this script to have ascii fun!
'''
class App:
    size_v:tuple = (100, 50)

    image_selected:str = ""
    text:str = ''

    # Gen ascii aglo
    def image_to_ascii(self,file_path):
        '''
        :param: str - Takes a file path where ascii will be saved
        '''

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
        '''
        Runs when select upload to get image from pc
        '''
        root.image_selected = filedialog.askopenfilename(initialdir="/Pictures", title="Select a file", filetypes = (('PNG', '*.png'),('JPEG', ('*.jpg', '*.jpeg', '*.jpe')), ("all files", "*.*")))
        self.display_image()

    def display_image(self):
        '''
        Runs algo on image then returns ascii text of image
        '''
        global text # Do not like using global but works here

        text=Text(root,name="text_box", width=self.size_v[0], height=self.size_v[1])
        text.tag_configure("center", justify='center',background='black', foreground='white')

        text.insert(INSERT, self.image_to_ascii(root.image_selected))
        text.pack()

        # Add the tag from start to end text
        text.tag_add("center", 1.0, "end")
        

    # Save to pc
    def save_pic(self):

        # Use for saving the image name gets unique name every time
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

    # Saves to dropbox
    def save_to_dropbox(self):
        now = datetime.now().strftime("%H%M%S")
        with open(str(now) + ".txt", 'w') as f:
            f.write(text.get(1.0, "end-1c"))
        # Calls on dropbox script 
        SaveToDropbox(str(now) + ".txt","/" + str(now) + ".txt")

    # Used to resize the image
    def resize(self):
        self.size_v = (scale_1.get(), scale_2.get())
        self.display_image()

# main UI
if __name__ == "__main__":
    # UI setup
    root: tk = tk.Tk()
    root.title("Image to ascii conversion")
    root.configure(bg='black')
    root.geometry("1000x1000")

    # UI interfaces setup
    tk.Button(root,text="Save to pc",command=App().save_pic, height=2, width= 1000).pack()
    tk.Button(root,text="Save to dropbox",command=App().save_to_dropbox, height=2, width= 1000).pack()

    tk.Button(root,text="Upload",command=App().upload_image, height=2, width= 1000).pack()
    tk.Button(root,text="Resize",command=App().resize, height=2, width= 1000).pack()
    scale_1 = Scale(root, from_=0, to=250, orient='horizontal')
    scale_1.pack()
    scale_2 = Scale(root, from_=0, to=100, orient='horizontal')
    scale_2.pack()

    root.mainloop()


   