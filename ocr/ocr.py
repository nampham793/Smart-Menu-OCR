import sys
sys.path.insert(0, '/Users/nampham/OneDrive - Đại học FPT- FPT University/Intern/Menu 1.2')
sys.path.insert(1, '/Users/nampham/OneDrive - Đại học FPT- FPT University/Intern/Menu 1.2/ocr')
sys.path.insert(2, '/Users/nampham/OneDrive - Đại học FPT- FPT University/Intern/Menu 1.2/vietnamese_font')

import easyocr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
from PIL import Image, ImageDraw, ImageFont

class Detect():
    def read_image(self, image_path):
        reader = easyocr.Reader(['vi'], gpu=True)

        img = cv2.imread(image_path)

        text = reader.readtext(img)

        return text

    def display(self, image_path):
        img = cv2.imread(image_path)
        # instance text detector
        reader = easyocr.Reader(['vi'], gpu=True)
        # detect text on image
        text_ = reader.readtext(img)

        threshold = 0.25
        # Load a TrueType font file that supports Vietnamese characters
        font_path = '/Users/nampham/OneDrive - Đại học FPT- FPT University/Intern/Menu 1.2/vietnamese_font/vi_font.ttf'
        font_size = 40
        font = ImageFont.truetype(font_path, size=font_size)

        # Convert the OpenCV image to a Pillow image
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img)

        # draw bbox and text
        for t_, t in enumerate(text_):
            print(t)

            bbox, text, score = t

            if score > threshold:
                # Extract the coordinates of the top-left and bottom-right corners of the bounding box
                top_left = tuple(map(int, bbox[0]))
                bottom_right = tuple(map(int, bbox[2]))

                # Draw a red rectangle (bounding box)
                draw.rectangle([top_left, bottom_right], outline="red", width=5)

                # Convert Pillow coordinates to OpenCV coordinates
                cv2_coord = (int(bbox[0][0]), int(bbox[0][1] + font_size))

                # Draw text using Pillow
                draw.text(cv2_coord, text, fill=(0, 0, 255), font=font)

        # Convert the Pillow image back to an OpenCV image
        result_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        plt.imshow(result_img)
        plt.show()        

if __name__ =="__main__":
    filepath_test = '/Users/nampham/OneDrive - Đại học FPT- FPT University/Intern/Menu 1.2/sample image/003.jpeg'
    detect = Detect()
    print(detect.read_image(filepath_test))
    detect.display(filepath_test)

