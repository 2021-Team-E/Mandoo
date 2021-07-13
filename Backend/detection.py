from imageai.Detection.Custom import CustomObjectDetection

def get_img(image):

    detector = CustomObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath("./detection_model-ex-025--loss-0018.418.h5") # 가중치 모델 경로
    detector.setJsonPath("./detection_config.json") # json 파일 경로
    detector.loadModel()

    image_path="./upload/"+image #input 이미지 경로
    result_path="./result/"+image #test output 이미지 경로 (크롭 x, 결과확인용)

    detections = detector.detectObjectsFromImage(input_image=image_path, output_image_path=result_path ,minimum_percentage_probability=80)
    for detection in detections:
        print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])

    title="test"
    choices=[1122,2222,3232,4224,5225]
    answer=1222
    script="script"
    image="image"
    return title, choices, answer, script, image