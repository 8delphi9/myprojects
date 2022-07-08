<div align="center">

  # 과제 02 - LabQ

</div>


## 목차
- [F팀 멤버 소개](#-team-f-member)  
- [개발 기간](#--개발-기간--)  
- [프로젝트 설명 분석](#-Project)
- [개발 조건](#-개발--조건)
- [실행방법](#-실행방법)
- [배포](#-배포)
- [API 명세서(Swagger)](#api-명세서)  
- [테스트 케이스](#테스트-케이스)  
- [기술 스택](#사용된-기술-스택) 

<div align="center">  
## 👨‍👨‍👦‍👦 Team "F" member  

|                이승민                 |                 임혁                  |                 전재완                  |                 정용수                 |
| :-----------------------------------: | :-----------------------------------: | :-------------------------------------: | :------------------------------------: |
| [Github](https://github.com/SMin1620) | [Github](https://github.com/Cat-Nile) | [Github](https://github.com/iamjaewhan) | [Github](https://github.com/blueknarr) |

  <br>

| <img height="200" width="380" src="https://retaintechnologies.com/wp-content/uploads/2020/04/Project-Management-Mantenimiento-1.jpg"> | <img height="200" width="330" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGElLjafMUhHglmqwh9lRh_sVzOCQyBiPNfQ&usqp=CAU"> |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
| 💻 [**Team work**](https://www.notion.so/Team-F-3f553f413ee14b389da0641d8bb4d99e) | 📒 [**Project page**](https://www.notion.so/21776eb6eb77429b9c9b4e65509c6aa5) |
|        공지사항, 컨벤션 공유 등<br> 우리 팀을 위한 룰        | 요구사항 분석, 정보 공유 및<br> 원할한 프로젝트를 위해 사용  |

  </div> 

  <h2> ⌛ 개발 기간  </h2> 
 2022/07/04  ~ 2022/07/07

  </div> 


# 💻 Project
  ### 프로젝트 설명
  - 고객은 본인의 소비 내역을 기록/관리하고 싶습니다. 
  - 아래의 요구사항을 만족하는 DB 테이블과 REST API를 만들어주세요.

    - 고객은 이메일과 비밀번호 입력을 통해서 회원가입을 할 수 있습니다.
    - 고객은 회원 가입이후, 로그인과 로그아웃을 할 수 있습니다.
    - 고객은 로그인 이후 가계부 관련 아래의 행동을 할 수 있습니다
      - 가계부에 오늘 사용한 돈의 금액과 관련된 메모를 남길 수 있습니다.
      - 가계부에서 수정을 원하는 내역은 금액과 메모를 수정 할 수 있습니다.
      - 가계부에서 삭제를 원하는 내역은 삭제 할 수 있습니다.
      - 삭제한 내역은 언제든지 다시 복구 할 수 있어야 합니다.
      - 가계부에서 이제까지 기록한 상세한 세부 내역을 볼 수 있습니다.
      - 가계부에서 상세한 세부 내역을 볼 수 있습니다.
    - 로그인하지 않은 고객은 가계부 내역에 대한 접근 제한 처리가 되어야 합니다.



  ### 프로젝트 분석

  - simple-jwt로 Access Token, Refresh Token 발급 
  - Permissions로 API 접근 권한 설정
  - BlackList 관리 - 로그아웃 할 때 Access Token을 blacklist에 저장
  - DB - 유저와 가계부 테이블 사용
      - 유저: 이메일, 닉네임, 패스워드
      - 가계부: 금액, 용도, 지급방식, 메모, 날짜
  -  삭제한 가계부 내역을 복구하기 위해 Model 소프트 삭제 구현



### API 명세서

| ID   | URI                           | METHOD | 기능                       |
| ---- | ----------------------------- | ------ | -------------------------- |
| 1    | /api/user/signup/             | POST   | 회원가입                   |
| 2    | /api/user/login/              | POST   | 로그인                     |
| 3    | /api/user/logout/             | POST   | 로그아웃                   |
| 4    | /api/user/                    | PATCH  | 회원정보 수정              |
| 5    | /api/user/                    | DELETE | 회원 탈퇴                  |
| 6    | /api/admin/user/              | GET    | 관리자 계정 조회           |
| 7    | /api/admin/user/<int:user_id> | GET    | 관리자 계정 상세 조회      |
| 8    | /api/ledgers/<int:id>         | GET    | 가계부 기록 조회           |
| 9    | /api/ledgers/<int:id>         | DELETE | 가계부 기록 삭제           |
| 10   | /api/ledgers/<int:id>         | PATCH  | 가계부 기록 수정           |
| 11   | /api/ledgers/                 | GET    | 가계부 상세 조회           |
| 12   | /api/bin/                     | GET    | 가계부 삭제 내역 조회      |
| 13   | /api/bin/<int:id>             | GET    | 가계부 삭제 내역 상세 조회 |
| 14   | /api/bin/<int:id>             | PUT    | 가계부 삭제 내역 복구      |



### ERD

사진

</div>




  ### 🚥 개발 조건 

  #### 🙆‍♂️ 필수사항  
    - Python, Django, MySQL 5.7
    - REST API 구현
    - DDL
    - 토큰을 이용한 인증 제어 방식
  #### 🔥 선택사항
    - Docker
    - Unit test codes  
    - REST API Documentation (Swagger UI)  





## 실행 방법

```
📌 Dependency

# 로컬에서 바로 서버 구동
pip install -r requirements.txt
python manage.py runserver

# 도커 실행
pip install docker
pip install docker-compose
docker-compose up -d
```





## 🔥 배포

docker를 이용해 프로젝트 api를 컨테이너화 하여 GCP에 배포했습니다  

[API Link]()

GCP 배포, 테스트 및 동작을 확인하였으며, 비용 등의 이유로 현재는 접속불가할 수 있습니다.





## API 명세서  

[API 명세서 (Swagger)]()
![image]()






## 테스트 케이스

Pytest-Django로 구현 된 28개의 테스트 구현

- 성공 케이스: 25개 (통과)
- 실패 케이스: 3개 (통과)





## 사용된 기술 스택

> - Back-End :  <img src="https://img.shields.io/badge/Python 3.10-3776AB?style=flat&logo=Python&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Django 4.0.4-092E20?style=flat&logo=Django&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Django-DRF 3.13.1-009287?style=flat&logo=Django&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Docker 20.10.14-2496ED?style=flat&logo=docker&logoColor=white"/>&nsbp
>
> - ETC　　　:  <img src="https://img.shields.io/badge/Git-F05032?style=flat-badge&logo=Git&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Github-181717?style=flat-badge&logo=Github&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Swagger-FF6C37?style=flat-badge&logo=Swagger&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white"/>