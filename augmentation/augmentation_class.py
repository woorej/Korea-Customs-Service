import cv2
import os
import shutil
from typing import List
from tqdm import tqdm
import numpy as np
import re

class Augmentation() :
    def __init__(self, collections: List, folder_path: str) :
        self.collections: List = collections
        self.aug_folder_list: List = self.get_augfolder_list(folder_path)

    def get_augfolder_list(self, folder_path: str) -> List :
        aug_folder_list : List = []
        assert os.path.isdir(folder_path), "folder_path is Not a directory"
        for root, dirs, files in os.walk(folder_path) :
            for dir in dirs :
                if os.path.exists(os.path.join(root, dir)) :
                    aug_folder_path :str = os.path.join(root+"_aug", dir)
                    aug_folder_list.append(aug_folder_path)
        return aug_folder_list
        
        
    def make_augfolder_structure(self) -> None :
        for aug_folder_path in self.aug_folder_list :
            os.makedirs(aug_folder_path, exist_ok=True)
     
     
    def copy_paste_image_to_augfolder(self) -> None :
    # aug_folder -> _aug 폴더의 경로
        for aug_folder in tqdm(self.aug_folder_list, desc="copy_paste_image_to_augfolder", ncols=110,ascii = ' =', position=0) :
            assert os.path.exists(aug_folder), f"{aug_folder} does not exist" 
            # aug경로를 통해 원본 경로로 변경한다.
            start_idx = aug_folder.find('_aug')
            rhs, lhs = aug_folder[start_idx+4:], aug_folder[:start_idx]
            folder_path = lhs+rhs # 원본폴더의 경로 추출
            folder_files = os.listdir(folder_path) # 원본 폴더의 경로를 통해서 이미지 이름만 가져오기
            
            for i, folder_file in enumerate(tqdm(folder_files, ncols=110,ascii = ' =', position=1, leave=False)) :
                # 원볼폴더 경로 + 이미지 이름을 합쳐 최종경로 추출
                folder_path_with_file = os.path.join(folder_path, folder_file)
                #_, ext = os.path.splitext(folder_file)
                
                if self.collections == "crawling" :
                    aug_file_name = f"100_000_000_000_{i+1:03}"+".jpg" # 100_100_000_000_001.jpg
                elif self.collections == "ai" :
                    aug_file_name = f"300_000_000_000_{i+1:03}"+".jpg" # 100_100_000_000_001.jpg
                else :
                    raise f"There is no option for {self.collections} collections"
                # aug_file_name -> 파일이름 변경
                aug_folder_wtih_file = os.path.join(aug_folder,aug_file_name)
                shutil.copyfile(folder_path_with_file, aug_folder_wtih_file)
                
    # '''
    # 원본에서 복사해온 이미지 삭제
    # '''
    # def delete_prvious_image(self) -> None :
    # # 정규 표현식 XXX_XXX_XXX_XXX_XXX.jpg
    #     crawling_pattern = r'^10\{1}_\d{3}_\d{3}_\d{3}_\d{3}\.jpg$' # 100_000_000_000_000.jpg의 이미지를 가질 확률이 이음.
    #     for aug_folder in tqdm(self.aug_folder_list, desc="delete_prvious_image", ncols=110, ascii = ' =', position=0)  :
    #         folder_files = os.listdir(aug_folder)
    #         for folder_file in tqdm(folder_files, ncols=110,ascii = ' =', position=1, leave=False) :
    #             if not re.match(crawling_pattern, folder_file):
    #                 #print(f"{os.path.join(aug_folder, folder_file)} Deleted")
    #                 os.remove(os.path.join(aug_folder, folder_file))

    '''
    이미지 조도 조절
    '''
    def adjust_illuminance_image(self, illuminance_ratioes: List) -> None :
        # 이미지 경로 추출
        for aug_folder in tqdm(self.aug_folder_list, desc="adjust_illuminance_image", ncols=110, ascii = ' =', position=0)  :
            folder_files = os.listdir(aug_folder)
            for folder_file in tqdm(folder_files, ncols=110,ascii = ' =', position=1, leave=False) :
                # aug_folder_path_with_image -> _aug 경로 + 이미지 이름을 합쳐 최종경로 추출
                aug_folder_path_with_image = os.path.join(aug_folder, folder_file)
                image = cv2.imread(aug_folder_path_with_image, cv2.IMREAD_COLOR)
                if image is None  :
                    print(f"Error: Image not loaded {aug_folder_path_with_image}")
                    #os.remove(aug_folder_path_with_image)
                    continue
                # 조도 조절
                for illuminance_ratio in illuminance_ratioes :
                    output_image = image.astype(np.float32)
                    output_image *= illuminance_ratio
                    output_image = np.clip(output_image, 0, 255).astype(np.uint8)
                    # 조도 이름 설정
                    if illuminance_ratio == 0.5 : # 어두움
                        illumin = 100
                    elif illuminance_ratio == 1 : # 보통
                        illumin = 300
                    elif illuminance_ratio == 1.25 : #밝음
                        illumin = 500
                    else :
                        raise f"There is no option for {illuminance_ratio} illuminance"
                    # 조도에 따른 이미지 이름 변경
                    image_name = aug_folder_path_with_image.split("/")[-1] # 100_100_000_000_001.jpg
                    lhs, rhs = image_name[:4], image_name[7:]
                    new_image_name = f"{lhs}{illumin:03}{rhs}" # 이미지 이름
                    image_path_with_name = os.path.join("/".join(aug_folder_path_with_image.split('/')[:-1]), new_image_name) # 최종 경로 만들기
                    cv2.imwrite(image_path_with_name, output_image) 
                #원본이미지 삭제
                if os.path.isfile(aug_folder_path_with_image):
                    os.remove(aug_folder_path_with_image)
                # else :
                #     print(f"{aug_folder_path_with_image} can not remove")
                #     cv2.imshow("1", output_image)
                #     cv2.waitKey(0)
                #     cv2.destroyAllWindows()
    
    '''
    이미지 회전
    '''
    def rotate_image(self, rotates:List) -> None :
        for aug_folder in tqdm(self.aug_folder_list, desc="rotate_image", ncols=110, ascii = ' =', position=0)  :
            folder_files = os.listdir(aug_folder)
            for folder_file in tqdm(folder_files, ncols=110,ascii = ' =', position=1, leave=False) :
                aug_folder_path_with_image = os.path.join(aug_folder, folder_file)
                image = cv2.imread(aug_folder_path_with_image, cv2.IMREAD_COLOR)
                if image is None  :
                    print(f"Error: Image not loaded {aug_folder_path_with_image}")
                    #os.remove(aug_folder_path_with_image)
                    continue
                
                # 회전 조절
                for rotate in rotates :
                    if rotate not in [0, 45, 90, 135, 180, 225, 270, 315] :
                        raise f"There is no option for {rotate} rotate"
                    processed_image = image.copy()
                    # 이미지 회전각도에 대한 회전 행렬을 구한다
                    M = cv2.getRotationMatrix2D((processed_image.shape[1] // 2, processed_image.shape[0] // 2), rotate,
                                                1.0)
                    # 이미지와 회전행렬곱을 통해 회전시킨다.
                    output_image = cv2.warpAffine(processed_image, M, (processed_image.shape[1], processed_image.shape[0]),
                                                        borderMode=cv2.BORDER_REPLICATE)
                    # 회전에 대한 이미지 이름을 수정하기                                
                    image_name = aug_folder_path_with_image.split("/")[-1] # 100_100_000_000_001.jpg
                    lhs, rhs = image_name[:12], image_name[15:]
                    # 회전각도에 따른 이름 변경
                    new_image_name = f"{lhs}{rotate:03}{rhs}"
                    image_path_with_name = os.path.join("/".join(aug_folder_path_with_image.split('/')[:-1]), new_image_name)
                    cv2.imwrite(image_path_with_name, output_image) 
                
                
    '''
    이미지 마스킹
    '''
    def mask_image(self, masks:List) -> None :
        for aug_folder in tqdm(self.aug_folder_list, desc="mask_image", ncols=110, ascii = ' =', position=0)  :
            folder_files = os.listdir(aug_folder)
            for folder_file in tqdm(folder_files, ncols=110,ascii = ' =', position=1, leave=False) :
                aug_folder_path_with_image = os.path.join(aug_folder, folder_file)
                image = cv2.imread(aug_folder_path_with_image, cv2.IMREAD_COLOR)
                if image is None  :
                    print(f"Error: Image not loaded {aug_folder_path_with_image}")
                    #os.remove(aug_folder_path_with_image)
                    continue
                
                # 마스킹 처리
                for mask in masks :
                    output_image = image.copy()
                    _, width, _ = output_image.shape
                    # 좀더 진한 박스색 BGR -> (10, 10, 40)
                    box_color = (14, 14, 50) # 박스생상 BGR
                    if mask == 3:   # 오른쪽 가림
                        output_image[:, width // 2:] = box_color
                    elif mask== 4:  # 왼쪽가림
                        output_image[:, :width // 2] = box_color
                    elif mask != 0: # 안 가림
                        raise f"There is no option for {mask} mask"
                    
                    # 마스킹에 따른 이미지 이름 변경                                
                    image_name = aug_folder_path_with_image.split("/")[-1] 
                    lhs, rhs = image_name[:2], image_name[3:]
                    new_image_name = f"{lhs}{mask}{rhs}"
                    image_path_with_name = os.path.join("/".join(aug_folder_path_with_image.split('/')[:-1]), new_image_name)
                    cv2.imwrite(image_path_with_name, output_image) 
    
if __name__=="__main__" :
    
    target = "crawling"
    
    augmentation_crawling = Augmentation(collections=target,folder_path="./미분류_검수완료" ) # 객체 생성
    augmentation_crawling.make_augfolder_structure() # 폴더구조 만들기
    augmentation_crawling.copy_paste_image_to_augfolder() # 만든 폴더에 이미지 복붙
    augmentation_crawling.adjust_illuminance_image(illuminance_ratioes=[0.5, 1, 1.25]) # 조도 조절 및 원본 이미지 삭제
    augmentation_crawling.rotate_image(rotates=[0, 45, 90, 135, 180, 225, 270, 315]) # 회전
    augmentation_crawling.mask_image(masks=[0, 3, 4]) # 마스킹 처리
    print(f"Finished!!")
    