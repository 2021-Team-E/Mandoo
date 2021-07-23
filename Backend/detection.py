from PIL import Image
import os
import boto3
from s3 import AWS_SECRET_KEY, AWS_ACCESS_KEY, BUCKET_NAME, APPKEY
import datetime
import shutil
import re
from pathlib import Path
import cv2
import torch
import tensorflow as tf
from models.experimental import attempt_load
from utils.datasets import LoadImages
from utils.general import check_img_size, non_max_suppression, scale_coords, set_logging,save_one_box
from utils.plots import colors, plot_one_box
from utils.torch_utils import select_device
from kakaoOcr import main

##s3버킷 세팅
s3 = boto3.client('s3', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)
resource = boto3.resource('s3', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)
buckets = resource.Bucket(name=BUCKET_NAME)

##모델 로드 부분
weights1 = 'modelv2.0.pt' # question/content/answer 구분 모델
weights2 = 'choice5_bestweight.pt' # choice 구분 모델



def get_img(image):

    image_png=image+".jpeg"
    imgsz = 416
    save_dir = Path('result')
    save_crop=True 
    
    # Initialize
    set_logging()
    device = select_device('')
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model1 = attempt_load(weights1, map_location=device)  # load FP32 model
    model2 = attempt_load(weights2, map_location=device)  # load FP32 model

    imgsz = check_img_size(imgsz, s=model1.stride.max())  # check img_size

    if half:
        model1.half()  # to FP16
        model2.half()


    # Set Dataloader
    save_img = True
    source = "./upload/"+image_png #input 이미지 경로
    dataset = LoadImages(source, img_size=imgsz)

    # Get names and colors
    names = model1.module.names if hasattr(model1, 'module') else model1.names

    # return 형식
    dict = {"question": [], "content" :[], "answer" : []}

    

    # Run inference
    if device.type != 'cpu':
        model1(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model1.parameters())))  # run once
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        pred = model1(img, augment=False)[0]

        # Apply NMS
        pred = non_max_suppression(pred, 0.5, 0.45, classes=None, agnostic=False)

        # Process detections
        for i, det in enumerate(pred):  # detections per image
            # content안에 객관식 있는 문제의 경우 탐지하기 위해 사용
            isContent = 0
            isQuestion = 0
            isAnswer=0
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
                    
                    label =  f'{names[c]} {conf:.2f}'

                    plot_one_box(xyxy, im0, label=label, color=colors(c, True), line_thickness=3)
                    if save_crop:
                        crop_path = save_dir / 'crops' / names[c] / f'{p.stem}.jpg'
                        save_one_box(xyxy, imc, file=crop_path, BGR=True)
                        

                    if names[c] == "content" : # content로 판별시 이미지 여부 판단 모델 들어가지 않고 이미지 자체를 return 데이터에 담음
                        
                        isContent=1
                        imagefilename ="result/"+ image + "_" + names[c] + "_"+ str(i) + "_" + str(datetime.datetime.now()).replace("\\","/").replace(" ","").replace(":","")+".jpeg"
                        imagefilename.replace(" ","")
                        imagetoupload = open( crop_path , "rb")
                        s3.put_object(Body=imagetoupload, Bucket=BUCKET_NAME, Key=imagefilename, ContentType="image/jpeg")
                        img_url = "https://summer-program.s3.ap-northeast-2.amazonaws.com/"+imagefilename
                        dict[names[c]].append(img_url)

                        text = main(crop_path, APPKEY)
                        text = re.sub(r'[^가-힣a-zA-Zㄱ-ㅎ()0-9.,?![]~%-_/<>\s]:\'\"\+]','', text)
                        if text =="":
                            text = "마우스를 올려 이미지로 확인해주세요"
                        print(text)
                        dict[names[c]].append(text)
                     



                    elif names[c] == "answer":
                        isAnswer=1
                        answerset = LoadImages(crop_path, img_size=imgsz)
                        names2 = model2.module.names if hasattr(model2, 'module') else model2.names
                                   
                        for path, img, im0s, vid_cap in answerset:
                            answerimg = torch.from_numpy(img).to(device)
                            answerimg = answerimg.half() if half else answerimg.float()  # uint8 to fp16/32
                            answerimg /= 255.0  # 0 - 255 to 0.0 - 1.0
                            if answerimg.ndimension() == 3:
                                answerimg = answerimg.unsqueeze(0)

                            # Inference
                            pred2 = model2(answerimg, augment=False)[0]

                            # Apply NMS
                            pred2 = non_max_suppression(pred2, 0.5, 0.45, classes=None, agnostic=False)

                            
                            # Process detections
                            for i, det in enumerate(pred2):  # detections per image
                                p, s, im02, frame = Path(path), '', im0s, getattr(answerset, 'frame', 0)
                                
                                s += '%gx%g ' % answerimg.shape[2:]  # print string
                                gn = torch.tensor(im02.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                                imc2 = im02.copy() if save_crop else im02  # for save_crop
                                if len(det):
                                    # Rescale boxes from img_size to im0 size
                                    det[:, :4] = scale_coords(answerimg.shape[2:], det[:, :4], im02.shape).round()

                                    # Print results
                                    for c in det[:, -1].unique():
                                        n = (det[:, -1] == c).sum()  # detections per class
                                        s += f"{n} {names2[int(c)]}{'s' * (n > 1)}, "  # add to string
                                    
                                    count = 0
                                    n=len(det)
                                    tensor=det
                                    sorted_choice=tensor.numpy()
                                    choice_number=[1,1,1,1,1]

                                    # y축 정렬
                                    for i in range(n):
                                        
                                        for j in range(0, n - i - 1):

                                
                                            if (sorted_choice[j][1] > sorted_choice[j+1][1]):
                                                    
                                                temp= sorted_choice[j + 1].copy() 
                                                
                                                sorted_choice[j + 1] = sorted_choice[j]
                                                    
                                                sorted_choice[j]=temp
                                  
                                    # 같은 선상의 문제들이 대해 x축 정렬
                                    for i in range (n):
                                      
                                        for j in range(0, n - i - 1):
                                       
                                            if (abs(sorted_choice[j][1] - sorted_choice[j+1][1])<5) :

                                                if (sorted_choice[j][0] > sorted_choice[j+1][0]) :

                                                    temp= sorted_choice[j + 1].copy()   
                                                    sorted_choice[j + 1] = sorted_choice[j]
                                                    sorted_choice[j]=temp
                                    # choice 탐지 안된 것들 0으로 표기
                                    for i in range (n-1):
                    
                                        if (abs(sorted_choice[i][1] - sorted_choice[i+1][1])>40) and (abs(sorted_choice[i][0] - sorted_choice[i+1][0])<30): # 중간에 choice 탐지 안 된 경우
                                            
                                            choice_number[i+1]=0
                                    print(choice_number) 

                                    # Write results
                                    for *xyxy, conf, cls in (det):
                                        
                                        c = int(cls)  # integer class
                                        label =  f'{names2[c]} {conf:.2f}'
                                        answer_save_path = str(save_dir / 'crops' / 'answer' /'choice'/ f'{count}{p.stem}.jpg')
                                   
                                        plot_one_box(xyxy, im02, label=label, color=colors(c, True), line_thickness=3)
                                        count = count +1
                                        if save_crop:
                                            save_one_box(xyxy, imc2, file=answer_save_path, BGR=True)
                                   
                                        text = main(answer_save_path, APPKEY)
                                        text = re.sub(r'[^가-힣a-zA-Zㄱ-ㅎ()0-9.,?![]~%-_/<>\s]:\'\"\+]','', text)
                                        if text =="":
                                            text = "마우스를 올려 이미지로 확인해주세요"
                                        print(text)
                                        dict[names[c]].append(text)

                                        imagefilename ="result/"+ image + "_" + "answer" + "_"+ str(i) + "_" + str(datetime.datetime.now()).replace("\\","/").replace(" ","").replace(":","")+".jpeg"
                                        imagefilename.replace(" ","")
                                        imagetoupload = open( answer_save_path , "rb")
                                        s3.put_object(Body=imagetoupload, Bucket=BUCKET_NAME, Key=imagefilename, ContentType="image/jpeg")
                                        img_url = "https://summer-program.s3.ap-northeast-2.amazonaws.com/"+imagefilename
                                        dict[names[c]].append(img_url)   
                                    
                                    for i in range(5):
                                        
                                        if choice_number[i]==0: # choice_number[i] 번째 선지가 탐지가 안된 경우
                                    
                                            dict[names[c]].insert(i*2,"해당 선택지 탐지에 실패하였습니다.")
                                            dict[names[c]].insert(i*2+1,"no exist url")
                                            
                                        
                                # Save results (image with detections)
                                if save_img:
                                    if dataset.mode == 'image':
                                        cv2.imwrite(answer_save_path, im02)
                    elif names[c] == "question":
                        isQuestion = 1
                        text = main(crop_path, APPKEY)
                        text = re.sub(r'[^가-힣a-zA-Zㄱ-ㅎ()0-9.,?![]~%-_/<>\s]:\'\"\+]','', text)
                        if text =="":
                            text = "마우스를 올려 이미지로 확인해주세요"
                        dict[names[c]].append(text)

                        
                        imagefilename ="result/"+ image + "_" + names[c] + "_"+ str(i) + "_" + str(datetime.datetime.now()).replace("\\","/").replace(" ","").replace(":","")+".jpeg"
                        imagefilename.replace(" ","")
                        imagetoupload = open( crop_path , "rb")
                        s3.put_object(Body=imagetoupload, Bucket=BUCKET_NAME, Key=imagefilename, ContentType="image/jpeg")
                        img_url = "https://summer-program.s3.ap-northeast-2.amazonaws.com/"+imagefilename
                        dict[names[c]].append(img_url)
                        
                    

                            
                    

            # Save results (image with detections)
            if save_img:
                if dataset.mode == 'image':
                    cv2.imwrite(save_path, im0)
                    

       
    if isQuestion == 1 and isContent == 1 and isAnswer == 0 :  
                       
        dict["answer"].append("①")
        dict["answer"].append("no exist url")
        dict["answer"].append("②")
        dict["answer"].append("no exist url")
        dict["answer"].append("③")
        dict["answer"].append("no exist url")
        dict["answer"].append("④")
        dict["answer"].append("no exist url")
        dict["answer"].append("⑤")
        dict["answer"].append("no exist url")
    #shutil.rmtree('./result/') # 결과 확인 필요 없을 때 주석 풀고 써주기 (result/ 폴더 삭제해주는 기능)
    print(dict)
    title=dict["question"]
    choices=dict["answer"]
    answer="1"
    script=dict["content"]
    score = "2"       

    return title, choices, answer, script, score
    
