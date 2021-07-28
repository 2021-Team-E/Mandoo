[한국어](README.md) | English

<br>

# **✍ f(Quiz)**

> This project was carried out for building a prototype for "Handshaker."

- f(Quiz) is a platform with a user-friendly interface designed to upload and view workbook problems via classifying different components of the question from a problem image and saving them to a database.

1️⃣ The user uploads the image of the problem.

<p>
 <img width="700" alt="quizrix_imageupload" src="https://user-images.githubusercontent.com/52441923/126748956-5bf7503e-575a-4008-83e1-9632de129c2c.png">
 </p>

2️⃣ The components of the problem are classified through a deep-learning model.

<p>
 <img width="700" alt="quizrix_imageupload" src="https://user-images.githubusercontent.com/52441923/126749134-2e804fb4-e62b-4e68-a1aa-4cdc033409c3.png">
</p>

<br>

     최종본 gif 추가

## **📌System Architecture**

<p align="center">  
  <img src="https://user-images.githubusercontent.com/52441923/126756283-16c5dd0b-8f84-4aab-81f1-b7e4ea4cc171.jpg">
</p>

<br>

## **🛠 Tech Stack**

<br>

| Category         | Tools/Frameworks                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| :------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Dev. Environment     | ![NHN](https://img.shields.io/badge/NHN_Cloud_Ubuntu-20.04-blue?logo=ubuntu) ![S3](https://img.shields.io/badge/S3-gray?logo=AmazonS3) ![Docker](https://img.shields.io/badge/docker-gray?logo=docker)                                                                                                                                                                                                                                                                                     |
| Front-end     | ![react](https://img.shields.io/badge/react-gray?logo=react) ![Javascript](https://img.shields.io/badge/javascript-ES6+-yellow?logo=javascript) ![Bootstrap](https://img.shields.io/badge/bootstrap-gray?logo=bootstrap) ![axios](https://img.shields.io/badge/axios-gray?logo=axios) ![Styled-components](https://img.shields.io/badge/styled_components-gray?logo=styled-components)                                                                                                     |
| Back-end      | ![Flask](https://img.shields.io/badge/flask-1.1.2-green?logo=flask) ![Python](https://img.shields.io/badge/python-3.7.6-skyblue?logo=python) ![Gunicorn](https://img.shields.io/badge/gunicorn-gray?logo=gunicorn) ![Postman](https://img.shields.io/badge/postman-gray?logo=postman) ![Swagger](https://img.shields.io/badge/swagger-gray?logo=swagger)                                                                                                                                   |
| DB            | ![MongoDB](https://img.shields.io/badge/mongodb-gray?logo=mongodb)                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Deep learning | ![Pytorch](https://img.shields.io/badge/pytorch-gray?logo=pytorch) ![Colab](https://img.shields.io/badge/colab-gray?logo=GoogleColab) ![Yolov5](https://img.shields.io/badge/yolov5-gray?logo=yolov5)                                                                                                                                                                                                                                                                                      |
| Etc           | ![Nginx](https://img.shields.io/badge/Nginx-gray?logo=nginx) ![github](https://img.shields.io/badge/github-gray?logo=github) ![VScode](https://img.shields.io/badge/VScode-gray?logo=visual-studio-code) ![AWS](https://img.shields.io/badge/AWS-EC2_instance-orange?logo=aws) ![Prometheus](https://img.shields.io/badge/Prometheus-gray?logo=Prometheus) ![Grafana](https://img.shields.io/badge/Grafana-gray?logo=Grafana) ![Redis](https://img.shields.io/badge/Redis-gray?logo=redis) |

<br>

## **🧿 PORTS**

| Name             | Port       | Description                                                                                                                                   |
| ---------------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Nginx            | 80         | HTTP Server and porxy that is simple but produces high performance.             |
| React(on Nginx)  | 80, 3000   | Provides a UI for uploading, viewing, and saving data provided by the classification model.|
| Flask + Gunicorn | 8000, 5000 | It is the main server for QUIZRIX and it connects web, Cloud Storage, and database in the center.                                                 |
| Mongo DB         | 27017      | Database                                                                                                                                      |
| Grafana          | 3001       | Provides a visual dashboard from the metrics data provided by cAdvisorm Prometheus, and NodeExporter. |
| cAdvisor         | 8080       | Measures resource usage by the docker containers and returns it as a time series data.         |
| Prometheus       | 9090       | Monitors and alerts based on the time series data collected from cAdvisor and NodeExporter  |
| Node Exporter    | 9100       | Collects host-related data such as, CPU, memory, disk, and network, and reveals it to the API.          |
<br>

## **🦾 AI**

### ✔flow

<p align="center">
<img alt="flow" src="https://user-images.githubusercontent.com/80239146/126985473-cae4a4f7-6e58-4a26-b7d5-538a32a361d1.PNG">
</p>

<br>
<br>

### ✔Results

- Model 1

  <img width="532" alt="model1" src="https://user-images.githubusercontent.com/80239146/126751834-81adeca3-36f7-48c4-9ea4-e360042f7551.PNG">

- Model 2

  <img width="571" alt="model2" src="https://user-images.githubusercontent.com/80239146/126751880-3cc7c43f-ee20-4f38-a72e-87b80769dfa7.PNG">

<br>

## **📋 File Tree**

```
📦Mandoo
┣ 📂alertmanager
┃ ┗ 📜config.yml
┣ 📂backend
┃ ┣ 📂models
┃ ┃ ┣ 📂hub
┃ ┣ 📂utils
┃ ┃ ┣ 📂aws
┃ ┃ ┣ 📂flask_rest_api
┃ ┃ ┣ 📂google_app_engine
┃ ┃ ┣ 📂wandb_logging
┃ ┣ 📜Dockerfile
┃ ┣ 📜README.md
┃ ┣ 📜app.py
┃ ┣ 📜choice5_bestweight.pt
┃ ┣ 📜detection.py
┃ ┣ 📜development.py
┃ ┣ 📜kakaoOcr.py
┃ ┣ 📜modelv2.0.pt
┃ ┗ 📜requirements.txt
┣ 📂frontend
┃ ┣ 📂node_modules
┃ ┣ 📂public
┃ ┣ 📂src
┃ ┃ ┣ 📂components
┃ ┃ ┃ ┣ 📂Modals
┃ ┃ ┃ ┃ ┣ 📜Modal.css
┃ ┃ ┃ ┃ ┗ 📜Modal.js
┃ ┃ ┃ ┣ 📜BlankTop.js
┃ ┃ ┃ ┣ 📜Button.js
┃ ┃ ┃ ┣ 📜Header.css
┃ ┃ ┃ ┣ 📜Header.js
┃ ┃ ┃ ┣ 📜logo.PNG
┃ ┃ ┃ ┣ 📜Search.js
┃ ┃ ┃ ┗ 📜Table.js
┃ ┃ ┣ 📂pages
┃ ┃ ┃ ┣ 📜imgIcon.png
┃ ┃ ┃ ┣ 📜Loader.js
┃ ┃ ┃ ┣ 📜Login.js
┃ ┃ ┃ ┣ 📜loginLogo.PNG
┃ ┃ ┃ ┣ 📜MainPage.js
┃ ┃ ┃ ┣ 📜noLogin.PNG
┃ ┃ ┃ ┗ 📜Signup.js
┃ ┃ ┃ ┣ 📜App.js
┃ ┃ ┃ ┣ 📜config.js
┃ ┃ ┣ 📜index.css
┃ ┃ ┗ 📜index.js
┃ ┣ 📜Dockerfile
┃ ┗ 📜README.md
┣ 📂grafana
┃ ┣ 📂provisioning
┃ ┃ ┣ 📂dashboards
┃ ┃ ┃ ┣ 📜dashboard.yml
┃ ┃ ┃ ┣ 📜Docker Prometheus Monitoring.json
┃ ┃ ┃ ┗ 📜FlaskApp_Monitoring.json
┃ ┃ ┗ 📂datasources
┃ ┃ ┃ ┗ 📜datasource.yml
┃ ┗ 📜config.monitoring
┣ 📂nginx
┃ ┗ 📜nginx.conf
┣ 📂prometheus
┃ ┣ 📜alert.rules
┃ ┗ 📜prometheus.yml
┣ 📜.gitignore
┣ 📜docker-compose.yml
┣ 📜LICENSE
┣ 📜README.md
┗ 📜README_en.md
```

<br>

## **🔑 Installation**

> ### Deploy

### **🎡 Github**

- Clone Repository

  ```bash
  git clone https://github.com/2021-Team-E/Mandoo.git
  ```

<br>

### **❄ Front-end** setting

- package.json

  ```json
  {
    ...

    "proxy": "http://<ip>:<server_port>",

    ...
  }
  ```

- config.js

  ```javascript
  export const USER_SERVER = "http://<ip>:<server_port>";
  ```

<br>

### **🌶 Back-end** Setting

- app.py

  ```python
  mongo = MongoClient('mongo_db', 27017)
  ```

- detection.py

  ```python
  #서버 환경에서의 tesseract.exe 경로로 설정
  pytesseract.pytesseract.tesseract_cmd="/usr/bin/tesseract"
  ```

- requirements.txt  
  Libraries installed separately by Dockerfile is commented

  ```
  # requirements.txt

  ...

  # tesseract-ocr
  # pytesseract

  …
  ```

- s3.py <— Make new file name 's3.py' in ./Backend

  ```python
  AWS_ACCESS_KEY = <AWS ACCESS KEY>
  AWS_SECRET_KEY = <AWS SECRET KEY>
  BUCKET_NAME = <AWS S3 bucket name>
  APPKEY = <Kakao API>
  ```

### **🐳 Docker**

```bash
docker-compose up —-build
```

<br>

## **📑 Swagger**

<p align="center">
<img alt="swagger" src="https://user-images.githubusercontent.com/80239146/127004473-8f2d92cf-6903-4540-9775-58ce8b196d93.PNG">
</p>
<br>

## **🎡 Git Convention**

### Git-Flow

- master : Branch for final product version
- develop : Branch for next version of the product
- feature : Branch for adding features
- release : Branch for preparing the release of current version
- hotfix : Branch for fixing issues in current version

### Process

- The following rules are applied whem creating a  `feature` branch for new features.
- `feature` branch is created from the last `develop` branch.
- The `develop` branch is `pulled` before creating the new branch.

### Branches name example

- feature-user (feature branch for user related features)  
  <br>

### **✔Commit message**

The following rules are applied when creating a commit message.

### 1. Commit Message Structure

Commit messages are typically in title/ content/ footer structure.

```xml
type : subject

body

```

### 2. Commit Type

- feat : add new feature
- fix : fix features and bugs
- docs : fix document
- refactor : refactoring codes (ex. changing variable name)
- test : test code or adding refactoring codes
- style : change code styles. Use comment form if the code itself is not changed.
- remove : remove code file and/or resources
- resource : adding image resources or other resources unrelated to prefab.

### 3. Subject

- Keep it less than 50 characters followed by a capital letter. Do not add a period in the end.
- Do not use past tense and keep it as a command sentence.

Example:

```xml
feat : Add translation to missing strings
feat : Disable publishing
feat : Sort list context menu
feat : Resize minimize/delete handle icons so they take up the entire topbar
fix : Fix typo in cleanup.sh file
```

### 4. Body

- It is optional to include a body and a commit may not include a body.
- A body is included when explaning the reason for a commit is necessary.
- Include a space to differentiate from the title.
- Each line should now exceed 72 characters.
- **DOES NOT HAVE TO WRITTEN IN ENGLISH**

### **✔git rebase**

Cleans the project's history beofore requesting a pull from the remote server. 
Before running `rebase`, `pull` from the `develop` branch to apply the commits done in the remote server.

```bash
git checkout develop
git pull
```

### Rebase the currently working feature branch into the develop branch.

```bash
git rebase develop feature/feature1
```

💡 **Caution**

Do not rebase commits that has already been pushed into the remote server.

Rebase creates a new commit with same content, not using the existing commit.
<br>

## **👪 Members**

| Name       | Developement Field                           | Skills in Charge                                        | Personal Bio                                        |
| ---------- | ---------------------------------- | -------------------------------------------- | -------------------------------------------------- |
| 🦦Laura Yoonjae Choi   | Front-end, Back-end, Deep learning | Web development,API Design, Data Engineering | [Move to Personal Bio](https://github.com/yunyun3599)  |
| 🐥Julia CheLim Lee   | Front-end, Devops                  | Web development, Docker                      | [Move to Personal Bio](https://github.com/leecr1215)   |
| 🦩Claire ShinYoung Park   | Front-end, Deep learning           | Web development, Algorithm                   | [Move to Personal Bio](https://github.com/shxnyoung)   |
| 🐹Julie Hayoung Lee   | Back-end, Deep learning            | API Design, Data Engineering                 | [Move to Personal Bio](https://github.com/hayoung1214) |
| 🦉Ryan H. Lee | Deep learning                      | Algorithm                                    | [Move to Personal Bio](https://github.com/printSANO)   |
| 🐢Kenny Geunwoo Park   | Devops                             | Cloud, Docker, Data Monitoring               | [Move to Personal Bio](https://github.com/Gnu-Kenny)   |

