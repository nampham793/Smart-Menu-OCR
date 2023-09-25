import os
import pandas as pd
import json
import sys

sys.path.insert(0, '/Users/nampham/OneDrive - Đại học FPT- FPT University/Intern/Menu 1.2')

class Metric():

    def readFile(self):
        result = pd.read_csv('/Users/nampham/OneDrive - Đại học FPT- FPT University/Intern/Menu 1.2/evaluation_process/FilteredDataframe3.csv', header=None)
        return result
  
    def evaluation(self, result):
    
        dataframe = self.readFile()
        image_name = result['image_name'].split('.')[0]  # Remove the file extension
        dataframe_image = dataframe[dataframe[0] == (image_name+".jpeg")]  # Replace 'image_name' with the actual key in your JSON data

        result_ocr = result['infers']

        precision, recall, f1_score = 0.0, 0.0, 0.0
        tp_count = 0
        tn_count = 0

        for obj in result_ocr:
            dataframe_namevi = None
            
            dataframe_namevi = dataframe_image[dataframe_image[1] == obj["Food"]]
            dataframe_price = dataframe_namevi[dataframe_namevi[2] == obj["Price"]]
            
            if not dataframe_price.empty:
                tp_count += 1
            else:
                tn_count += 1
            
        # Precision
        try:
            precision = 1.0 * tp_count / (tp_count + tn_count)
        except ZeroDivisionError:
            precision = 0.0

        # Recall
        fn_count = dataframe_image.shape[0] - tp_count
        try:
            recall = 1.0 * tp_count / (tp_count + fn_count)
        except ZeroDivisionError:
            recall = 0.0

        # F1 score
        try:
            f1_score = 2.0 * (precision * recall) / (precision + recall)  
        except ZeroDivisionError:
            pass
        
        return f1_score

if __name__ == "__main__":
          
    evaluation = Metric()

    FOLDER_PATH = "/Users/nampham/OneDrive - Đại học FPT- FPT University/Intern/Menu 1.2/Results"

    list_scored = []
    for file in os.listdir(FOLDER_PATH):
        file_path = os.path.join(FOLDER_PATH, file)
        with open(file_path, 'r') as json_file:
            json_data = json.load(json_file)
        result = {'image_name': file, 'infers': json_data}  # Include 'image_name' key

        f1_score = evaluation.evaluation(result)
        list_scored.append(f1_score)
        average_f1 = sum(list_scored)/len(list_scored)
    print("-------------------------------")
    print("F1 score list:", list_scored)
    print(f"Average F1 score of {len(list_scored)} images:",average_f1)
    print("-------------------------------")
