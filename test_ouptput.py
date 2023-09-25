import os
import json
from app import Extractor
from evaluation_process.evaluation import Metric
from spellcheck import SpellChecker
import re

def main():
    INPUT_FOLDER = "/Users/nampham/OneDrive - Đại học FPT- FPT University/Intern/Menu 1.2/sample image"
    ONEGRAM_PATH = "/Users/nampham/OneDrive - Đại học FPT- FPT University/Intern/Menu 1.2/Food Vocab/one_gram.txt"
    BIGGRAMS_PATH = "/Users/nampham/OneDrive - Đại học FPT- FPT University/Intern/Menu 1.2/Food Vocab/big_grams.txt"

    correct_spell = SpellChecker(ONEGRAM_PATH, BIGGRAMS_PATH)
    extractor = Extractor()
    metric = Metric()
    
    for file in os.listdir(INPUT_FOLDER):
        file_path = os.path.join(INPUT_FOLDER, file)

        pairs = extractor.extract_menu(file_path)
        menu_data = []

        for item in pairs:
            food = item[0]
            price = item[1]
            
            words = food.split(' ')
            new_food_name = []
            
            for word in words:
                corrected_word = correct_spell.correct_spell(word)
                new_food_name.append(corrected_word)
            
            menu_data.append({'Food': ' '.join(new_food_name).upper(), 'Price': price})

        # Save the menu data to a JSON file
        output_file = f'/Users/nampham/OneDrive - Đại học FPT- FPT University/Intern/Menu 1.2/Results/{file[-8:-5]}.json'
        
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(menu_data, json_file, ensure_ascii=False, indent=4)

    print("Save Finished")

if __name__ == "__main__":
    main()
