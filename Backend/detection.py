
#from imageai.Detection.Custom import CustomObjectDetection
#from imageai.Classification.Custom import CustomImageClassification
import pytesseract 
from PIL import Image
import os
import boto3
from s3 import AWS_SECRET_KEY, AWS_ACCESS_KEY, BUCKET_NAME
import datetime
import shutil
#############아래는 yolov5 버전 입니다###################

from pathlib import Path

import cv2
import torch
from numpy import random

from models.experimental import attempt_load
from utils.datasets import LoadImages
from utils.general import check_img_size, non_max_suppression, scale_coords, set_logging,save_one_box
from utils.plots import colors, plot_one_box
from utils.torch_utils import select_device

pytesseract.pytesseract.tesseract_cmd="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
# pytesseract.pytesseract.tesseract_cmd="/usr/bin/tesseract"    #서버 환경에서의 경로
s3 = boto3.client('s3', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)
resource = boto3.resource('s3', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)
buckets = resource.Bucket(name=BUCKET_NAME)


##모델 로드 부분
weights = 'modelv2.0.pt'
## s3 버킷에 weights 모델 올리면 사용
# file_path = 'modelv1.0.pt'  # 내 서버에 저장하는 것 이미지 포함 여부 판단 모델
# key_name = 'modelv1.0.pt'   # s3버킷 저장되어있는 이름
# buckets.download_file(key_name, file_path)

# file_path = 'model_ex-024_acc-1.000000.h5'  # 내 서버에 저장하는 것 이미지 포함 여부 판단 모델
# key_name = "model_ex-024_acc-1.000000.h5"   # s3버킷 저장되어있는 이름
# buckets.download_file(key_name, file_path)

# file_path = 'detection_config.json'  
# key_name = 'detection_config.json'  
# buckets.download_file(key_name, file_path)

## imageai 사용 모델 (이전 버전)
# file_path = 'detection_model-ex-025--loss-0018.418-85per.h5'
# key_name = 'detection_model-ex-025--loss-0018.418-85per.h5'
# buckets.download_file(key_name, file_path)


def get_img(image):

    image_png=image+".jpeg"
    imgsz = 640
    save_dir = Path('result')
    save_crop=True 

    # Initialize
    set_logging()
    device = select_device('')
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    imgsz = check_img_size(imgsz, s=model.stride.max())  # check img_size
    if half:
        model.half()  # to FP16

    # Set Dataloader
    save_img = True
    source = "./upload/"+image_png #input 이미지 경로
    dataset = LoadImages(source, img_size=imgsz)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    print(names)
   

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        pred = model(img, augment=False)[0]

        # Apply NMS
        pred = non_max_suppression(pred, 0.5, 0.45, classes=None, agnostic=False)

        # Process detections
        for i, det in enumerate(pred):  # detections per image
            # det = det[det[:, -1] == 1]
            p, s, im0, frame = Path(path), '', im0s, getattr(dataset, 'frame', 0)

            save_path = str(save_dir / p.name)
            s += '%gx%g ' % img.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            imc = im0.copy() if save_crop else im0  # for save_crop
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    c = int(cls)  # integer class
                    print(c)
                    label =  f'{names[c]} {conf:.2f}'
                    print(label)
                    #label = f'{names[int(cls)]} {conf:.2f}'
                    plot_one_box(xyxy, im0, label=label, color=colors(c, True), line_thickness=3)
                    if save_crop:
                            save_one_box(xyxy, imc, file=save_dir / 'crops' / names[c] / f'{p.stem}.jpg', BGR=True)

                result = "True"
            else:
                result = "False"

            # Save results (image with detections)
            if save_img:
                if dataset.mode == 'image':
                    cv2.imwrite(save_path, im0)
                    print(save_path)

    # return result

    # detector = CustomObjectDetection()
    # detector.setModelTypeAsYOLOv3()
    # detector.setModelPath("./detection_model-ex-025--loss-0018.418-85per.h5") # 가중치 모델 경로 (3구분 모델)
    # detector.setJsonPath("./detection_config.json") # json 파일 경로
    # detector.loadModel()

    # image_path="./upload/"+image_png #input 이미지 경로
    # result_path="./result/"+image_png #test output 이미지 경로 (크롭 x, 결과확인용)

    # detections = detector.detectObjectsFromImage(input_image=image_path, output_image_path=result_path , extract_detected_objects=True,  minimum_percentage_probability=50)
    
    # label= []
    # dict = {"question": [], "content" :[], "answer" : []}
   

    # for detection in detections:   
    #     #print(detection)
    #     print("\n")

    # for detection in detections[0]:
    #     print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])
    #     label.append(detection["name"])
    # print(label)
    

    # #텍스트 추출 부분
    # execution_path = os.getcwd()    
    # print(execution_path)

    # prediction = CustomImageClassification()
    # prediction.setModelTypeAsInceptionV3()
    
    # prediction.setModelPath('./model_ex-024_acc-1.000000.h5')
    # prediction.setJsonPath("./model_class.json")
    # prediction.loadModel(num_objects=2)
    
    
    
    # for index,detection in enumerate(detections[1]): #index로 몇번째 인지 접근 가능
    #     print(index, detection)
    #     this_labelname=label[index]
    #     print(this_labelname)
        
    #     if this_labelname == "content" : # content로 판별시 이미지 여부 판단 모델 들어가지 않고 이미지 자체를 return 데이터에 담음
    #         imagefilename ="result/"+ image + "_" + this_labelname + "_"+ str(index) + "_" + str(datetime.datetime.now()).replace("\\","/").replace(" ","").replace(":","")+".jpeg"
    #         imagefilename.replace(" ","")
    #         imagetoupload = open(detection, "rb")
    #         s3.put_object(Body=imagetoupload, Bucket=BUCKET_NAME, Key=imagefilename, ContentType="image/jpeg")
    #         img_url = "https://summer-program.s3.ap-northeast-2.amazonaws.com/"+imagefilename
    #         dict[this_labelname].append(img_url)
    #         continue

    #     predictions, probabilities = prediction.classifyImage(detection, result_count=2)    #predictions[0] : 무조건 퍼센트 높은 아이로 지정됨
        
        
        
    #     if probabilities[0] > probabilities[1]:
    #         print("This is a(n) " + predictions[0])

    #     if predictions[0] == "text": #텍스트인 경우
    #         text = pytesseract.image_to_string(Image.open(detection), lang='kor+eng')
    #         print(text)
    #         dict[this_labelname].append(text)

    #     else :  #이미지 포함한 경우
    #         imagefilename ="result/"+ image + "_" + this_labelname + "_"+ str(index) + "_" + str(datetime.datetime.now())+".jpeg"
    #         imagefilename.replace(" ","")
    #         imagetoupload = open(detection, "rb")
    #         s3.put_object(Body=imagetoupload, Bucket=BUCKET_NAME, Key=imagefilename, ContentType="image/jpeg")
    #         img_url = "https://summer-program.s3.ap-northeast-2.amazonaws.com/"+imagefilename
    #         dict[this_labelname].append(img_url)
    #     print("\n\n")

    #     #The below is just to check the likelihood
    #     for eachPrediction, eachProbability in zip(predictions, probabilities):
    #         print(eachPrediction , " : " , eachProbability)

    # #shutil.rmtree('./result/') # 결과 확인 필요 없을 때 주석 풀고 써주기 (result/ 폴더 삭제해주는 기능)
    # print(dict)
    # title=dict["question"]
    # choices=dict["answer"]
    # answer="1"
    # script=dict["content"]
    # score = "2"

    title=["example question"]
    choices=["example answer"]
    answer="1"
    script=["example content"]
    score = "2"
    
    return title, choices, answer, script, score
