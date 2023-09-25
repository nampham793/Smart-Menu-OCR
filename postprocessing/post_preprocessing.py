import logging
import os
from datetime import date
from typing import List

import mapping
from spellcheck import SpellChecker


class PostPreprocessor():
    def __init__(self, debug=False):

        ONEGRAM_PATH = "/Users/nampham/OneDrive - Đại học FPT- FPT University/Intern/Menu 1.2/Food Vocab/one_gram.txt"
        BIGGRAMS_PATH = "/Users/nampham/OneDrive - Đại học FPT- FPT University/Intern/Menu 1.2/Food Vocab/big_grams.txt"

        self.spellchecker = SpellChecker(
            ONEGRAM_PATH,
            BIGGRAMS_PATH
        )

    def preprocess(self, text):
        
        # Clean text
        text = text
        processed_list = []
        for detection in text:
            processed_list.append(detection[1])

        clean_text_list = []
        for text in processed_list:
            cleaned_text = mapping.clean_raw_text(text)
            clean_text_list.append(cleaned_text)

        # Step 1: Classify food and prices
        foods, prices = mapping.get_price_and_food(clean_text_list)

        # # Step 2: Correct spell for food entities
        foods = [self.spellchecker.correct_spell(food, lookup_only=False, include_unknown=True) for food in foods]

        #Get size entities
        size = []
        for detection in text:
            s = mapping.get_size(detection)
            size.append(s)

        # Step 3: Mapping entities
        menu = mapping.map(foods,prices,size)
        menu_cleaned = [[item[0].replace('\n', ' '), item[1]] for item in menu]


        return menu_cleaned

if __name__ == "__main__":
    import sys
    sys.path.insert(0, '/Users/nampham/OneDrive - Đại học FPT- FPT University/Intern/Menu 1.2')
    sys.path.insert(1, '/Users/nampham/OneDrive - Đại học FPT- FPT University/Intern/Menu 1.2/ocr')
    from ocr import Detect

    filepath_test = '/Users/nampham/OneDrive - Đại học FPT- FPT University/Intern/Menu 1.2/sample image/002.jpeg'
    text = Detect().read_image(filepath_test)

    process = PostPreprocessor()
    print(process.preprocess(text))
