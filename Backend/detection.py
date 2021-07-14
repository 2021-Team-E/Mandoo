from imageai.Detection.Custom import CustomObjectDetection
from imageai.Classification.Custom import CustomImageClassification
import os
import pytesseract 
from PIL import ImageEnhance, ImageFilter, Image

def get_img(image):

    # detector = CustomObjectDetection()
    # detector.setModelTypeAsYOLOv3()
    # detector.setModelPath("./detection_model-ex-025--loss-0018.418.h5") # 가중치 모델 경로
    # detector.setJsonPath("./detection_config.json") # json 파일 경로
    # detector.loadModel()

    # image_path="./upload/"+image #input 이미지 경로
    # result_path="./result/"+image #test output 이미지 경로 (크롭 x, 결과확인용)

    # detections = detector.detectObjectsFromImage(input_image=image_path, output_image_path=result_path , extract_detected_objects=True,  minimum_percentage_probability=80)
    # for eachObject in detections:
    #     print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])

    #execution_path = os.getcwd()
    #
    #prediction = CustomImageClassification()
    #prediction.setModelTypeAsInceptionV3()
    #
    #prediction.setModelPath(os.path.join(execution_path,"가중치 모델"))
    #prediction.setJsonPath(os.path.join(execution_path, "./model_class.json"))
    #prediction.loadModel(num_objects=2)
    #imageTrial_path = "사진주소"
    #
    #predictions, probabilities = prediction.classifyImage(os.path.join(execution_path, imageTrial_path), result_count=2)
    #text = pytesseract.image_to_string(Image.open(imageTrial_path), lang='kor+eng')

    #if probabilities[0] > probabilities[1]:
        #print("This is a(n) " + predictions[0])
    #else:
        #print("This is a(n) " + predictions[1])
    #if predictions[0] == "text":
        #print(text)
    # The below is just to check the likelihood
    # for eachPrediction, eachProbability in zip(predictions, probabilities):
        #print(eachPrediction , " : " , eachProbability)
    

    title="test"
    choices=[1122,2222,3232,4224,5225]
    answer=1222
    script="script"
    image="image"
    return title, choices, answer, script, image