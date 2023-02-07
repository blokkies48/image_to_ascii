# image_to_ascii
## Description
This app takes a image and converts it to ascii, creating interesting results. 
## Recommendations
I have found that the higher the resolution of you monitor is set to, the clearer the ascii image becomes.
## Instructions
This is a standalone project. You will only need three files. 
- main.py
- dropbox_save.py
- requirements.txt 

#### Continue to follow the instructions on "Running the app from the script"
---

## Potential of the app!
![alt text](https://github.com/blokkies48/image_to_ascii/blob/master/Images/162023.jpeg)

## The UI and App
![alt text](https://github.com/blokkies48/image_to_ascii/blob/master/Images/off_the_app.jpg)


### Running the app from the script
- Make sure to have python 3.10 or higher installed.
- Create a virtual environment, not a requirement but recommended.
- On Windows run this in the terminal
```py
pip install -r requirements.txt
```
- Simply run main.py 

### How the app works
Firstly you will have to select 'upload' to upload a image from your pc, preferably a (png) image.
- Save to pc
    - Saves image to your local pc
- Save to dropbox
    - Replace API TOKEN inside of the dropbox_save.py file with your own.
    - Once save to dropbox a text file will be automatically uploaded to the dropbox.
- Upload
    - Opens file explorer to upload the image as mentioned above.
- Resize
    - Two slider options that allows the user to change
        - Length
        - Width
    - Select resize for changes to take affect.

## The app alongside dropbox
![alt text](https://github.com/blokkies48/image_to_ascii/blob/master/Images/browser_dropbox.jpg)

This shows that the image has been uploaded to dropbox as an text file.


## Console output showing image uploaded
![alt text](https://github.com/blokkies48/image_to_ascii/blob/master/Images/console_output.jpg)

What your console output should be if everything worked correctly
