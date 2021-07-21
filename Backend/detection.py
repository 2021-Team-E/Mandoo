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

from models.experimental import attempt_load
from utils.datasets import LoadImages
from utils.general import check_img_size, non_max_suppression, scale_coords, set_logging,save_one_box
from utils.plots import colors, plot_one_box
from utils.torch_utils import select_device

pytesseract.pytesseract.tesseract_cmd="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
#pytesseract.pytesseract.tesseract_cmd="/usr/bin/tesseract"    #서버 환경에서의 경로
s3 = boto3.client('s3', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)
resource = boto3.resource('s3', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)
buckets = resource.Bucket(name=BUCKET_NAME)

##모델 로드 부분
weights1 = 'modelv2.0.pt'
weights2 = 'choice5_bestweight.pt'
#weights3 = ''
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
    #model3 = attempt_load(weights3, map_location=device)  # load FP32 model

    imgsz = check_img_size(imgsz, s=model1.stride.max())  # check img_size
    if half:
        model1.half()  # to FP16
        model2.half()
        #model3.half()

    # Set Dataloader
    save_img = True
    source = "./upload/"+image_png #input 이미지 경로
    dataset = LoadImages(source, img_size=imgsz)

    # Get names and colors
    names = model1.module.names if hasattr(model1, 'module') else model1.names
    labels= []
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
            print(i)
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

                    labels.append(names[c])
                    print(labels)
                
                    plot_one_box(xyxy, im0, label=label, color=colors(c, True), line_thickness=3)
                    if save_crop:
                        crop_path = save_dir / 'crops' / names[c] / f'{p.stem}.jpg'
                        save_one_box(xyxy, imc, file=crop_path, BGR=True)
                        print(crop_path)
                        print({p.stem})

                    if names[c] == "content" : # content로 판별시 이미지 여부 판단 모델 들어가지 않고 이미지 자체를 return 데이터에 담음
                        imagefilename ="result/"+ image + "_" + names[c] + "_"+ str(i) + "_" + str(datetime.datetime.now()).replace("\\","/").replace(" ","").replace(":","")+".jpeg"
                        imagefilename.replace(" ","")
                        imagetoupload = open( crop_path , "rb")
                        s3.put_object(Body=imagetoupload, Bucket=BUCKET_NAME, Key=imagefilename, ContentType="image/jpeg")
                        img_url = "https://summer-program.s3.ap-northeast-2.amazonaws.com/"+imagefilename
                        dict[names[c]].append(img_url)

                        
                        continue



                    elif names[c] == "answer":
                        answerset = LoadImages(crop_path, img_size=imgsz)
                        names2 = model2.module.names if hasattr(model2, 'module') else model2.names
                        flag_for_choice = 0 # 첫번째 choice의 image/text 구분을 하는 순간 1로 변화시킴 
                        flag_for_choice_result = 0 # choice detection 결과 text이면 1, image이면 2

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
                                    # Write results
                                    for *xyxy, conf, cls in reversed(det):
                                        c = int(cls)  # integer class
                                        label =  f'{names2[c]} {conf:.2f}'
                                        answer_save_path = str(save_dir / 'crops' / 'answer' /'choice'/ f'{count}{p.stem}.jpg')
                                   
                                        plot_one_box(xyxy, im02, label=label, color=colors(c, True), line_thickness=3)
                                        count = count +1
                                        if save_crop:
                                            save_one_box(xyxy, imc2, file=answer_save_path, BGR=True)
                                    det2 = det    
                                    ###이미지/텍스트 분류 모델 들어가야함 --> 첫 choice만 detect하도록
                                        
                                    # choiceset = LoadImages(answer_save_path, img_size=imgsz)
                                    # names3 = model3.module.names if hasattr(model3, 'module') else model3.names
                            
                                    # for path, img, im0s, vid_cap in choiceset:
                                    #     if flag_for_choice == 1 : # 첫 choice만 가지고 나머지 choice도 판별
                                    #         break
                                    #     choiceimg = torch.from_numpy(img).to(device)
                                    #     choiceimg = choiceimg.half() if half else choiceimg.float()  # uint8 to fp16/32
                                    #     choiceimg /= 255.0  # 0 - 255 to 0.0 - 1.0
                                    #     if choiceimg.ndimension() == 3:
                                    #         choiceimg = choiceimg.unsqueeze(0)

                                    #     # Inference
                                    #     pred3 = model3(choiceimg, augment=False)[0]

                                    #     # Apply NMS
                                    #     pred3 = non_max_suppression(pred3, 0.5, 0.45, classes=None, agnostic=False)

                                    #     # Process detections
                                    #     for i, det in enumerate(pred3):  # detections per image
                                    #         p, s, im03, frame = Path(path), '', im0s, getattr(choiceset, 'frame', 0)

                                    #         s += '%gx%g ' % choiceimg.shape[2:]  # print string
                                    #         gn = torch.tensor(im03.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                                    #         imc3 = im03.copy() if save_crop else im03  # for save_crop
                                    #         if len(det):
                                    #             flag_for_choice = 1
                                    #             # Rescale boxes from img_size to im0 size
                                    #             det[:, :4] = scale_coords(choiceimg.shape[2:], det[:, :4], im03.shape).round()

                                    #             # Print results
                                    #             for c in det[:, -1].unique():
                                    #                 n = (det[:, -1] == c).sum()  # detections per class
                                    #                 s += f"{n} {names3[int(c)]}{'s' * (n > 1)}, "  # add to string

                                    #             # Write results
                                    #             for *xyxy, conf, cls in reversed(det):
                                    #                 c = int(cls)  # integer class
                                    #                 label =  f'{names3[c]} {conf:.2f}'
                                    #                 choice_save_path = str(save_dir / 'crops' / 'answer' / 'choice' /names3[c] / f'{i}{p.stem}.jpg')
                                    #                 plot_one_box(xyxy, im03, label=label, color=colors(c, True), line_thickness=3)
                                                    

                                    #                 if names3[c] == "text": # 텍스트인 경우   
                                    #                     flag_for_choice_result = 1
                                    #                 elif names3[c] == "image": # 이미지인 경우
                                    #                     flag_for_choice_result = 2

                                    #                 if save_crop:
                                    #                     save_one_box(xyxy, imc3, file=choice_save_path, BGR=True)

                                    #         # Save results (image with detections) question detection 결과 저장
                                    #         if save_img:
                                    #             if dataset.mode == 'image':
                                    #                 cv2.imwrite(choice_save_path, im03)
                                    #                 print(choice_save_path)

                                   
                                    # for i in range (0,len(det2)):

                                    #     choice_result_save_path=str(save_dir / 'crops' / 'answer' /'choice'/ f'{i}{p.stem}.jpg')
                                       
                                    #     # 아래 코드는 text일 경우임
                                    #     if flag_for_choice_result == 1: # choice가 텍스트인 경우            
                                    #         text = pytesseract.image_to_string(Image.open(choice_result_save_path), lang='kor+eng')
                                    #         print(text)
                                    #         dict[names[c]].append(text)

                                    #     elif flag_for_choice_result == 2 : # choice가 이미지인 경우
                                    #         imagefilename ="result/"+ image + "_" + "answer" + "_"+ str(i) + "_" + str(datetime.datetime.now()).replace("\\","/").replace(" ","").replace(":","")+".jpeg"
                                    #         imagefilename.replace(" ","")
                                    #         imagetoupload = open( choice_result_save_path , "rb")
                                    #         s3.put_object(Body=imagetoupload, Bucket=BUCKET_NAME, Key=imagefilename, ContentType="image/jpeg")
                                    #         img_url = "https://summer-program.s3.ap-northeast-2.amazonaws.com/"+imagefilename
                                    #         dict[names[c]].append(img_url)    
                                        
        

                    # elif names[c] == "question":
                        # questionset = LoadImages(crop_path, img_size=imgsz)
                        # names3 = model3.module.names if hasattr(model3, 'module') else model3.names
               
                        # for path, img, im0s, vid_cap in questionset:
                        #     questionimg = torch.from_numpy(img).to(device)
                        #     questionimg = answerimg.half() if half else answerimg.float()  # uint8 to fp16/32
                        #     questionimg /= 255.0  # 0 - 255 to 0.0 - 1.0
                        #     if questionimg.ndimension() == 3:
                        #         questionimg = questionimg.unsqueeze(0)

                        #     # Inference
                        #     pred3 = model3(questionimg, augment=False)[0]

                        #     # Apply NMS
                        #     pred3 = non_max_suppression(pred3, 0.5, 0.45, classes=None, agnostic=False)

                        #     # Process detections
                        #     for i, det in enumerate(pred3):  # detections per image
                        #         p, s, im03, frame = Path(path), '', im0s, getattr(questionset, 'frame', 0)

                        #         s += '%gx%g ' % questionimg.shape[2:]  # print string
                        #         gn = torch.tensor(im03.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                        #         imc3 = im03.copy() if save_crop else im03  # for save_crop
                        #         if len(det):
                        #             # Rescale boxes from img_size to im0 size
                        #             det[:, :4] = scale_coords(questionimg.shape[2:], det[:, :4], im03.shape).round()

                        #             # Print results
                        #             for c in det[:, -1].unique():
                        #                 n = (det[:, -1] == c).sum()  # detections per class
                        #                 s += f"{n} {names3[int(c)]}{'s' * (n > 1)}, "  # add to string

                        #             # Write results
                        #             for *xyxy, conf, cls in reversed(det):
                        #                 c = int(cls)  # integer class
                        #                 label =  f'{names3[c]} {conf:.2f}'
                        #                 question_save_path = str(save_dir / 'crops' / 'question' / names3[c] / f'{i}{p.stem}.jpg')
                        #                 plot_one_box(xyxy, im03, label=label, color=colors(c, True), line_thickness=3)

                        #                 if save_crop:
                        #                     save_one_box(xyxy, imc3, file=question_save_path, BGR=True)
                                     
            
                        #                 # 아래 코드는 text일 경우임
                        #                 if names3[c] == "text": #텍스트인 경우            
                            #                 text = pytesseract.image_to_string(Image.open(questionset), lang='kor+eng')
                            #                 print(text)
                            #                 dict[names[c]].append(text)

                        #                 elif names3[c] == "image": #이미지인 경우
                        #                     imagefilename ="result/"+ image + "_" + names[c] + "_"+ str(i) + "_" + str(datetime.datetime.now()).replace("\\","/").replace(" ","").replace(":","")+".jpeg"
                        #                     imagefilename.replace(" ","")
                        #                     imagetoupload = open( crop_path , "rb")
                        #                     s3.put_object(Body=imagetoupload, Bucket=BUCKET_NAME, Key=imagefilename, ContentType="image/jpeg")
                        #                     img_url = "https://summer-program.s3.ap-northeast-2.amazonaws.com/"+imagefilename
                        #                     dict[names[c]].append(img_url)


                        #         # Save results (image with detections) question detection 결과 저장
                        #         if save_img:
                        #             if dataset.mode == 'image':
                        #                 cv2.imwrite(question_save_path, im03)
                        #                 print(question_save_path)
                   
            # Save results (image with detections)
            if save_img:
                if dataset.mode == 'image':
                    cv2.imwrite(save_path, im0)
                    print(save_path)

       

    #shutil.rmtree('./result/') # 결과 확인 필요 없을 때 주석 풀고 써주기 (result/ 폴더 삭제해주는 기능)
    print(dict)
    title=dict["question"]
    choices=dict["answer"]
    answer="1"
    script=dict["content"]
    score = "2"       

    return title, choices, answer, script, score
    
