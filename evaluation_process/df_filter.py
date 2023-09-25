import os
import pandas as pd

 

class Retrive():
    def __init__(self, folderpath):
        self.folder_path = folderpath

    def get_image_names(self):
        image_names = []
        for file_name in os.listdir(self.folder_path):
            image_names.append(file_name)
        return image_names
    
    def retrieve_data(self, list_name, main_df_path):
        columns = ['ImageName', 'VietnameseName', 'Price']
        label_df = pd.read_excel(main_df_path)
        filtered_df = label_df[label_df['ImageName'].isin(list_name)]
        filtered_df = filtered_df[columns]
        return filtered_df

if __name__ == "__main__":
    FOLDER_PATH = "/Users/nampham/OneDrive - Đại học FPT- FPT University/Intern/Menu 1.2/sample image"
    LABEL_PATH = "/Users/nampham/OneDrive - Đại học FPT- FPT University/Intern/Menu 1.2/label data/labels.xlsx"
    SAVE_PATH = "/Users/nampham/OneDrive - Đại học FPT- FPT University/Intern/Menu 1.2/evaluation_process/FilteredDataframe3.csv"
    
    Retrive = Retrive(FOLDER_PATH)
    list_name = Retrive.get_image_names()
    filtered_df = Retrive.retrieve_data(list_name, LABEL_PATH)

    filtered_df.to_csv(SAVE_PATH, index = False)
    print("Succesfully saved the dataframe!\n")

    print(filtered_df)
    