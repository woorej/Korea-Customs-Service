import json
import os
import random
import math


class DataHandler():
    def __init__(self, path: str, main_category: str, want_items: list = None, option=None):

        self.main_category = main_category
        self.path = path
        self.want_item = want_items

        self.second_category_list = self.get_second_category(self.path, self.main_category)
        self.third_category_list = self.get_third_category(self.path, self.main_category, self.second_category_list)
        self.ImageID = self.get_json(self.path, self.main_category, self.second_category_list, self.third_category_list)

    def get_ImageID(self):
        print(self.ImageID)

    def get_json(self, path, main_category, second_category_list, third_category_list):
        result = {}
        for i in range(len(second_category_list)):  # 2
            image_id = []
            for j in range(len(third_category_list[i])):
                json_path = path + main_category + '/' + second_category_list[i] + '/' + third_category_list[i][
                    j] + '/' + 'info.json'
                with open(json_path, 'r') as f:
                    json_data = json.load(f)
                    jsonArray = json_data.get("data")
                    for st in jsonArray:
                        image_id.append(st.get("ImageID"))  # 원하는 품목
                        # image_id.append(st.get("Filename")) # 원하는 품목

            result[second_category_list[i]] = image_id

        real_result = {}
        real_result[main_category] = result

        return real_result

    def get_second_category(self, path, main_category):
        root_dir = os.path.join(path, main_category)
        root_under_dir_list = os.listdir(root_dir)

        return root_under_dir_list  # H4131_스피커, H4141_헤드폰

    def get_third_category(self, path, main_category, second_category_list):  # IT ,['H4131_스피커', 'H4141_헤드폰']
        third_catory_list = []
        for i in range(len(second_category_list)):
            root_dir = os.path.join(path + main_category, second_category_list[
                i])  # './ML_Tutorial/data_loader/TTA_sample/IT' + ['H4131_스피커', 'H4141_헤드폰']
            root_under_dir_list = os.listdir(
                root_dir)  # ['스피커_Beosound_Balance', '스피커_ANIMO', '스피커_AXIS_C1410_Network_Mini_Speaker'..]
            third_catory_list.append(root_under_dir_list)

        return third_catory_list


    def get_item(self, want_item, split=False, view_point=False): # registered Number
        result = {}
        for i in range(len(self.second_category_list)):  # 2
            image_id = []
            for j in range(len(self.third_category_list[i])):
                json_path = self.path + self.main_category + '/' + self.second_category_list[i] + '/' + \
                            self.third_category_list[i][j] + '/' + 'info.json'
                with open(json_path, 'r') as f:
                    json_data = json.load(f)
                    jsonArray = json_data.get("data")
                    for st in jsonArray:
                        if view_point is False :
                            image_id.append(st.get(want_item))  # 원하는 품목
                        # image_id.append(st.get("Filename")) # 원하는 품목
                        else :
                            print(st.get('ViewPoint'))
                            if st.get('ViewPoint') in view_point :
                                image_id.append(st.get(want_item))

            result[self.second_category_list[i]] = image_id

        real_result = {}
        real_result[self.main_category] = result

        if split is True:
            ratio = 0.8
            random.seed(42)
            add_second_category_train_dataset = {}
            add_second_category_test_dataset = {}
            for key in result.keys():
                num = math.ceil(ratio * len(result[key]))  # number of train data
                train_data_set = random.sample(result[key], num)
                print(
                    f'{self.main_category}-{key}-Total number: {len(result[key])}, ratio: {ratio}, train_set_number: {len(train_data_set)}',
                    end='')

                # remove picked item
                for i in train_data_set:
                    result[key].remove(i)  # test_data_set

                add_second_category_train_dataset[key] = train_data_set  # 중분류가 입력된 train_dataset
                add_second_category_test_dataset[key] = result[key]  # 중분류가 입력된 test_dataset
                print(f', test_set_number: {len(result[key])}')

            # 대분류 입력
            add_main_category_train_dataset = {}
            add_main_category_train_dataset[self.main_category] = add_second_category_train_dataset

            add_main_category_test_dataset = {}
            add_main_category_test_dataset[self.main_category] = add_second_category_test_dataset

            return add_main_category_train_dataset, add_main_category_test_dataset

        return real_result


# Option
path = './'
main_category = 'IT'
want_lists = ["Filename"]

result = []
DataHandler = DataHandler(path, main_category)

# if you want train, test data split -> get_item(want_list, split=True)
for want_list in want_lists:
    result.append(DataHandler.get_item(want_list, split=False, view_point=[60, 0]))

print(result)
