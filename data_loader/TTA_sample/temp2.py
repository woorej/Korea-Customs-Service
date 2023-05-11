import json
import os
import random

class CustomDataLoader() :
    def __init__(self, path : str, main_category : str, want_items : list = None, option=None) :
        
        self.main_category = main_category
        self.path = path
        self.want_item = want_items

        self.second_category_list = self.get_second_category(self.path, self.main_category)
        self.third_category_list = self.get_third_category(self.path, self.main_category, self.second_category_list)
        self.ImageID = self.get_json(self.path, self.main_category, self.second_category_list, self.third_category_list)

    def get_ImageID(self) :
        print(self.ImageID)

    def get_json(self, path, main_category, second_category_list, third_category_list):
        result = {}
        for i in range(len(second_category_list)): # 2
            image_id = []
            for j in range(len(third_category_list[i])):
                json_path = path + main_category + '/' + second_category_list[i] + '/' + third_category_list[i][j] + '/' + 'info.json'
                with open(json_path, 'r') as f:
                    json_data = json.load(f)
                    jsonArray =  json_data.get("data")
                    for st in jsonArray:
                        image_id.append(st.get("ImageID")) # 원하는 품목
                        #image_id.append(st.get("Filename")) # 원하는 품목
                                    
            result[second_category_list[i]] = image_id

        real_result = {}
        real_result[main_category] = result

        return real_result


    def get_second_category(self, path, main_category):
        root_dir = os.path.join(path, main_category)
        root_under_dir_list = os.listdir(root_dir)

        return root_under_dir_list   # H4131_스피커, H4141_헤드폰


    def get_third_category(self, path, main_category, second_category_list): # IT ,['H4131_스피커', 'H4141_헤드폰']
        third_catory_list = []
        for i in range(len(second_category_list)):
            root_dir = os.path.join(path+main_category,second_category_list[i]) # './ML_Tutorial/data_loader/TTA_sample/IT' + ['H4131_스피커', 'H4141_헤드폰']
            root_under_dir_list = os.listdir(root_dir) #  ['스피커_Beosound_Balance', '스피커_ANIMO', '스피커_AXIS_C1410_Network_Mini_Speaker'..]
            third_catory_list.append(root_under_dir_list)

        return third_catory_list


    def get_item(self, want_item) :
        result = {}
        for i in range(len(self.second_category_list)): # 2
            image_id = []
            for j in range(len(self.third_category_list[i])):
                json_path = self.path + self.main_category + '/' + self.second_category_list[i] + '/' + self.third_category_list[i][j] + '/' + 'info.json'
                with open(json_path, 'r') as f:
                    json_data = json.load(f)
                    jsonArray =  json_data.get("data")
                    for st in jsonArray:
                        image_id.append(st.get(want_item)) # 원하는 품목
                        #print(image_id)
                        #image_id.append(st.get("Filename")) # 원하는 품목

            result[self.second_category_list[i]] = image_id

        real_result = {}
        real_result[self.main_category] = result

        return real_result

# Option
path = './TTA_sample/'
main_category='IT'

want_lists =  ['RegisteredNumber', 'Filename', 'BrandCode']

result = []
DataHandler = CustomDataLoader(path, main_category)

for want_list in want_lists :
    result.append(DataHandler.get_item(want_list))

print(result)



# https://jimmy-ai.tistory.com/147
