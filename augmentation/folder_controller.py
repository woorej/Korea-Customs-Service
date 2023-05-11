import shutil
import os
import collections
#import re

"""
target.txt를 이용해 폴더만드는 부분
"""
def make_folder_structure(text_file_name: str) -> set:
    folder_maps : list = []
    debug = True
    with open("target.txt", "r") as f: 
        readlines = f.readlines()
        for readline in readlines :
            # txt파일에서 엔터키를 제거하고 리스트로 만든다.
            line = readline.replace("\n", "").split()
            #line = re.sub(r"[^a-zA-Z0-9ㄱ-ㅎㅏ-ㅣ가-힣]", "", readline)
            # [대분류, 소분류, 등록번호] 형태의 folder_maps
            folder_maps.append(line)
    # 등록번호 아래에 AI, 크롤링 이라는 폴더를 만들기 위해 리스트를 만든다.
    collections=['AI','크롤링']
    # 대분류/소분류 경로형태로 가지고 있는 집합을만듬
    category_sets = set()
    for folder_map in folder_maps :
        main_category = folder_map[0] # 대분류를 저장
        sub_category = folder_map[1] # 소분류를 저장
        category_sets.add(main_category+"/"+sub_category) # 대분류/소분류 저장
        design_number_category = folder_map[2] # 등록번호 저장
        
        main_category_dir = os.path.abspath(main_category) # 대분류를 절대경로로 변경
        sub_category_dir = os.path.abspath(os.path.join(main_category, sub_category)) # 대분류/소분류를 join하고 절대경로로 저장
        design_number_category_dir = os.path.abspath(os.path.join(main_category, sub_category, design_number_category)) # 대분류/소분류/등록번호를 join하고 절대경로로 저장
        
        # 수집자료형태(AI, 크롤링)의 폴더를 만들어준다.
        for collection in collections :
            design_number_category_collection_dir = os.path.join(design_number_category_dir, collection)
            os.makedirs(design_number_category_collection_dir, exist_ok=True)
            
    return category_sets

"""
만들어둔 폴더에 파일을 이동해주는 부분
"""
def parse_file(category_sets: set, root_path: str) -> None :
    # 모든 등록번호가 저장되어 정리되지 않은 폴더
    root_path = "미분류_검수완료"
    # 절대경로로 변경해준다.
    root_abspath = os.path.abspath(root_path)

    for root, dirs, files in os.walk(root_abspath) :
        for file in files :
            # 모든 파일들을 싹다 읽어온다.
            file_path = os.path.join(root, file)        
            for category_set in category_sets : 
                # 미분류라고 표시된 문자열을 대분류/소분류 replace한 절대경로를 저장
                parsed_file_path = file_path.replace(root_path, category_set)
                # 크롤링의 경로를 붙여준다.
                path = os.path.join("/".join(parsed_file_path.split("/")[:-1]),"크롤링")
                # 경로를 붙여주기 위해 파일이름을 저장한다.
                name = parsed_file_path.split("/")[-1]
                # 크롤링 경로를 붙여주고 파일의 이름을 합쳐서 최종 절대경로를 만든다.
                parsed_file_crawling_path = os.path.join(path, name)
                # 사전에 만든 파일 파일 경로가 존재하면 이동하고 그렇지 않으면 넘긴다.
                if os.path.exists(path) :
                    print(f"{file_path} ---> {parsed_file_crawling_path}")
                    shutil.copyfile(file_path, parsed_file_crawling_path)
                else :
                    print(f"Check File: {file_path}")
                    
"""
각 등록번호의 이미지 개수를 출력하는 부분
"""
def file_counter(category_sets: set) -> None :
    
    

    file_counter_list: list = []

    for category_set in category_sets :
        # 절대경로 만들고
        abs_category_set = os.path.abspath(category_set)
        # category_set에 해당하는 모든 파일다 읽어오기
        for root, dirs, files in os.walk(abs_category_set) :
            for file in files :
                # 경로만들어주고
                source_directory = os.path.join(root, file)
                # 등록번호만 때온다
                dist = source_directory.split("/")[-3]
                # 리스트에 추가해주고
                file_counter_list.append(dist)
                # 갯수 카운팅
                counter = collections.Counter(file_counter_list)
                
    # 기존 텍스트 읽어와서
    with open("target.txt", "r") as f: 
        # 한줄씩 읽고
        readlines = f.readlines()
        for readline in readlines :
            # 엔터 제거
            src = readline.replace("\n", "").split()
            # 등록번호만 저장해두고
            design_number = src[2]
            # 등록번호 뒤에 해당 파일 갯수 저장해준다.
            nomralized_src = " ".join(src)+" "+str(counter[design_number])
            # 확인용 텍스트 파일 만든다.
            with open("target_with_counter.txt", "a") as tc:
                tc.write(f"{nomralized_src}\n")
            # 숫자만 나오게해서 복사 붙여넣기를 편하게한다
            with open("counter.txt","a") as c :
                c.write(f"{str(counter[design_number])}\n")
                

if __name__=="__main__" :
    category_sets = make_folder_structure(text_file_name="target.txt") # 폴더구조 생성
    parse_file(category_sets=category_sets, root_path="미분류_검수완료") # 만든 폴더구조로 이미지 복붙
    file_counter(category_sets=category_sets) # 파일 갯수 카운팅

