## **📋 File Tree**

```
📦backend
 ┣ 📂models
 ┃ ┣ 📂hub
 ┣ 📂utils
 ┃ ┣ 📂aws
 ┃ ┣ 📂flask_rest_api
 ┃ ┣ 📂google_app_engine
 ┃ ┣ 📂wandb_logging
 ┣ 📜Dockerfile
 ┣ 📜README.md
 ┣ 📜app.py
 ┣ 📜choice5_bestweight.pt
 ┣ 📜detection.py
 ┣ 📜development.py
 ┣ 📜kakaoOcr.py
 ┣ 📜modelv2.0.pt
 ┗ 📜requirements.txt
```

## **how to start**

```bash
cd backend
```

가상환경 설정

```bash
python -m venv venv
cd venv
.\Scripts\activate
```

install

```bash
(venv) cd ../backend/
(venv) pip install -r requirements.txt
```

run

```bash
(venv) python app.py
```

## **API** (자세하게 설명)
   
<br>

> - 회원(User) 관련 API
> 
>   |  Method |  Path  |  Permission |  목적 |
>   | --- | --- | --- | --- |
>   |**POST** |/api/v1/user/signup | None |하나의 User 생성|
>   |**POST** |/api/v1/user/login | None |하나의 User 접속|
>   |**GET** |/api/v1/user/logout | Jwt Token |하나의 User 로그아웃|

<br>

> - 문제(Quiz) 관련 API
> 
>   |  Method |  Path  |  Permission |  목적 |
>   | --- | --- | --- | --- |
>   |**POST** |/api/v1/quiz/imageupload | Jwt Token |퀴즈 이미지 업로드|
>   |**GET** |/api/v1/quiz/show | Jwt Token |User의 퀴즈 호출|
>   |**DELETE** |/api/v1/quiz/delete | Jwt Token |퀴즈 삭제|
>   |**PUT** |/api/v1/quiz/modify | Jwt Token |퀴즈 수정|
