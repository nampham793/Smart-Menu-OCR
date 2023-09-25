import sys
sys.path.insert(0, '/Users/nampham/OneDrive - Đại học FPT- FPT University/Intern/Menu 1.2')
sys.path.insert(1, '/Users/nampham/OneDrive - Đại học FPT- FPT University/Intern/Menu 1.2/postprocessing')
sys.path.insert(2, '/Users/nampham/OneDrive - Đại học FPT- FPT University/Intern/Menu 1.2/ocr')

import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

import numpy as np
import pandas as pd
import time
import argparse

from ocr import Detect

import postprocessing.mapping
from postprocessing.post_preprocessing import PostPreprocessor

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()

class Extractor():
    def __init__(self):
        self.reader = Detect()

        self.postprocess = PostPreprocessor(debug=False)

    def extract_menu(self, file_path):
        image_path = file_path
        text = list(self.reader.read_image(image_path))

        menu = self.postprocess.preprocess(text)

        return menu 

@app.post("/extract-menu")
async def upload_image(file: UploadFile):
    try:
        # Save the uploaded image to a temporary location
        image_path = f"/tmp/{file.filename}"
        with open(image_path, "wb") as image_file:
            image_file.write(file.file.read())

        # Extract the menu using the Extractor class
        extract = Extractor()
        data = extract.extract_menu(image_path)
        df = pd.DataFrame(data, columns=["Food", "Price"])
        df['Food'] = df['Food'].str.upper()

        # Return the extracted menu as JSON
        return JSONResponse(content=df.to_dict(orient="records"), media_type="application/json")
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


