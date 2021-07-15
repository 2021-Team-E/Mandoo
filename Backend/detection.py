
from imageai.Detection.Custom import CustomObjectDetection
from imageai.Classification.Custom import CustomImageClassification
import pytesseract 
from PIL import ImageEnhance, ImageFilter, Image
import os
import boto3
from s3 import BUCKET_NAME
import shutil

pytesseract.pytesseract.tesseract_cmd="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
resource = boto3.resource('s3')
buckets = resource.Bucket(name=BUCKET_NAME)

file_path = 'model_ex-024_acc-1.000000.h5'  # 내 서버에 저장하는 것 (텍스트 추출 모델)--이미지 판단 모델인듯
key_name = "model_ex-024_acc-1.000000.h5"   # s3버킷 저장되어있는 이름
buckets.download_file(key_name, file_path)

file_path = 'detection_config.json'  
key_name = 'detection_config.json'  
buckets.download_file(key_name, file_path)

def get_img(image):
    image_png=image+".png"
    detector = CustomObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath("./detection_model-ex-025--loss-0018.418-85per.h5") # 가중치 모델 경로 (3구분 모델)
    detector.setJsonPath("./detection_config.json") # json 파일 경로
    detector.loadModel()

    image_path="./upload/"+image_png #input 이미지 경로
    result_path="./result/"+image_png #test output 이미지 경로 (크롭 x, 결과확인용)

    detections = detector.detectObjectsFromImage(input_image=image_path, output_image_path=result_path , extract_detected_objects=True,  minimum_percentage_probability=80)
    
    label= []
    dict = {"question": [], "content" :[], "answer" : []}
    result_label = []

    for detection in detections:   
        print(detection)
        print("\n")

    for detection in detections[0]:  #eachObject
        print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])
        label.append(detection["name"])
    print(label)
    # distri_image = detections[1]

    #텍스트 추출 부분
    execution_path = os.getcwd()    
    print(execution_path)

    prediction = CustomImageClassification()
    prediction.setModelTypeAsInceptionV3()
    
    prediction.setModelPath('./model_ex-024_acc-1.000000.h5') #"model_ex-024_acc-1.000000.h5"
    prediction.setJsonPath("./model_class.json")
    prediction.loadModel(num_objects=2)
    
    #imageTrial_path = "./result/"+image+"-objects/answer-00001.jpg" #"구분된 사진주소"
    
    for index,detection in enumerate(detections[1]): #index로 몇번째 인지 접근 가능
        print(index, detection)
        predictions, probabilities = prediction.classifyImage(detection, result_count=2)
        text = pytesseract.image_to_string(Image.open(detection), lang='kor+eng')
        
        this_labelname=label[index]
        print(this_labelname)
        print(dict[this_labelname])
        if probabilities[0] > probabilities[1]: # 텍스트인 경우인가요....?
            print("This is a(n) 텍스트" + predictions[0])

        else:                                   # 이미지 포함한 경우인 경우인가요....?
            print("This is a(n) 이미지" + predictions[1])
            # dict[this_labelname].append("imageurl")

        if predictions[0] == "text":
            print(text)
            dict[this_labelname].append(text)
        if predictions[0] == "image":
         
            dict[this_labelname].append("imageurl")
        print("\n\n")

        #The below is just to check the likelihood
        for eachPrediction, eachProbability in zip(predictions, probabilities):
            print(eachPrediction , " : " , eachProbability)

    #shutil.rmtree('./result/') # 결과 확인 필요 없을 때 주석 풀고 써주기 (result/ 폴더 삭제해주는 기능)
    print(dict)
    title=dict["question"]
    choices=dict["answer"]
    answer="1"
    script=dict["content"]
    image="image"
    score = "2"
    
    return title, choices, answer, script, image, score
