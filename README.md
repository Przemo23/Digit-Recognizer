# Digit-Recognizer
Python script for digit recognition in an image.



## Preparation before running the script

### Python and pip
Firstly make sure you have Python and pip installed on your machine.
You can check it by typing into the console:

```
> python --version
Python 3.8.x
> pip --version
pip x.x.x from ... (python 3.8)
```

### Cloning the repo
Clone the repository to a directory of your choice
```
git clone https://github.com/Przemo23/Digit-Recognizer.git
```

### Creating an virtual enviroment
Next step is to create an virtualenv. If you don't have virtualenv just run:
```
pip install virtualenv
```
Then you have to create the venv
```
> python -m venv digit-recognizer
```
To activate it run:
Windows:
```
> .\digit-recognizer\Scripts\activate
```
Linux:
```
> source digit-recognizer/bin/activate
```

### Installing the necessary libraries:
```
(digit-recognizer) > pip install -r requirements.txt
```
### Installing tesseract and ghostcript:
Tesseract:
  For Windows
    Download pytesseract from here:
    https://github.com/UB-Mannheim/tesseract/wiki
    If you don't have Visual C++ for Python compiler make sure to install it as well
  For Linux:
    sudo apt-get install tesseract-ocr

Ghostscript:
  Download the right version from your OS here
  https://www.ghostscript.com/download/gsdnld.html
  
For Windows users:
Open the config.py file and set up the paths to both pytesseract and ghostscript scripts
They should look somewhat like that, but you might have installed them elsewhere:
```
pytesseract_path = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
gs_path = 'C:/Program Files/gs/gs9.53.3/bin/gswin64c'
```
## Running the script
To use the script run the command:
```
(digit-recognizer) > python digit-recognizer.py -i <input_file_path>
```
### Additional options:
-o <output_file> - to save the result to a file use this flag. The file should have .PNG extension.
-p - turn off the PLAIN_DIGIT mode. Use this flag if the input image contains other characters besides
letters or if the digits are clustered inside other contours. It reduces performance, but may produce better
results in those cases.


