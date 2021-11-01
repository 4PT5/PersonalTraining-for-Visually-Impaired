# PersonalTraining for Visually Impaired

![4pt5](https://i.esdrop.com/d/j09wmqn009xs/fRGaFyj08q.png)
<br>
**PersonalTraining for Visually Imapired**은 ***2021 공개SW 개발자 대회***를 위한 프로젝트로, 사회문제형 과제 가운데 사회적 약자를 위한 시스템이다. 해당 프로젝트는 시각 장애인을 위한 퍼스널 트레이닝(PT) 서비스를 제공하기 위해 영상처리와 음성인식만으로도 사용자가 운동할 수 있도록 도움을 주기 위한 목적으로 진행된다.

**PersonalTraining for Visually Imapired** is a project for the ***2021 Open SW Developer Conference*** and is a system for the socially disadvantaged among social problem-type tasks. In order to provide personal training services for visually impaired people, which include low vision, it helps users to exercise only through voice recognition and image processing.

## Table of Contents
* [Getting Started](#getting-started)
* [System Architecture](#system-architecture)
* [Introduction](#introduction)
  + [Project purpose](#project-purpose)
  + [Description](#description)
  + [Operation Process](#operation-process)
* [Tech Skills and Tools](#tech-skills-and-tools)
* [Browser Support](#browser-support)
* [Contributors](#contributors)
* [Demo](#demo)
* [License](#license)

## Getting Started

```
$ git clone https://github.com/4PT5/PersonalTraining-for-Visually-Impaired
```
### Pip
```
$ python3 -m venv django_venv
$ source django_venv/bin/activate
(django_venv) $ pip install -r requirements.txt
(django_venv) $ python manage.py migrate
(django_venv) $ python manage.py createsuperuser
(django_venv) $ python manage.py runserver
# Load the site at http://127.0.0.1:8000/
```
requirements.txt should have the following line:
```
tensorflow==1.15.5
```

## System Architecture
<img src="https://i.esdrop.com/d/j09wmqn009xs/TZtVCFOK9u.png" width="80%" height="60%">

## Introduction
### Project purpose
> AI를 이용한 스마트 헬스케어 산업은 매우 빠른 속도로 성장하고 있다. 하지만 그중 시각 장애인을 위한 상품을 찾기는 쉽지 않다. 그들에게 있어 TV, 스마트폰, 모니터 화면을 보는 것은 어렵거나 혹은 불가능한 일이기 때문에 해당 제품들에 대한 접근성과 공급은 매우 낮을 수 밖에 없다. 본 프로젝트는 시각장애인들이 홈트레이닝을 할 수 있도록 운동을 보조하는 서비스를 제안한다. 영상처리를 통한 운동 자세 교정 서비스는 널리 있지만, 본 프로젝트가 제안하는 서비스의 차별점은 시각장애인 분들을 위해 음성처리를 활용하여 자세 교정을 제공한다는 점이다.

> The smart healthcare industry using AI is developing at a very rapid rate. Among them, however, products for visually impaired people are not easily found. For them, it is difficult or impossible to watch TV, smartphone, or monitor screens, so accessibility and supply for those products are inevitably low.
This project proposes a service to assist the blind in home training. Although the exercise posture correction service through video processing is widely used, the distinction of the service proposed by this project is that it provides posture correction using voice processing for blind people.

### Description
> 1️⃣ **시각장애인을 위한 음성 안내**   
본 프로젝트는 화면 속 영상을 볼 수 없는 시각장애인들은 단순히 운동 영상을 틀어놓고 귀로 듣는 것만으로는 해당 동작을 따라할 수 없다는 점에 집중하였다. 이에 따라 사용자가 눈에 보이는 영상 없이도 정확한 운동 자세를 잡을 수 있도록, 운동 동작에 대한 팔과 다리의 구부리는 정도, 허리를 숙이는 정도, 무릎을 내미는 정도 등 세세한 자세에 대한 설명을 먼저 목소리로 안내할 수 있게 설계했다.    
2️⃣ **운동 자세에 대한 실시간 감지**  
사용자는 안내되는 음성을 통해 각 신체부위에 따라 설명하는 자세를 잡을 수 있고, 이는 웹캠을 통해 입력되어 프로그램 내에서 자세 추정 및 해당 자세에 대한 피드백이 이루어진다.  
3️⃣ **시각장애인을 고려한 단순한 UI**  
또한 본 프로젝트에서는 시각 장애인 가운데 90%가 저시력자인 것을 감안했다. 그래서 저시력자들을 위한 단순한 UI를 제공한다. 웹 페이지는 큰 글씨로 모든 글자들이 작성되어 있고, 눈에 쉽게 띄도록 큰 버튼을 배치했으며, 페이지 이동이 거의 없도록 웹을 구성하여 사용자들이 이용하는 데 어렵지 않도록 구축했다.  

> 1️⃣ **Voice guidance for blind people**  
The project focused on the fact that visually impaired people who cannot see the video on the screen cannot follow the motion simply by playing the exercise video and listening to it with their ears. Accordingly, it is designed to guide the user through detailed explanations such as the degree of bending of arms and legs, bending of waist, and sticking out of knees so that the user can get an accurate exercise position without visible video.  
2️⃣ **Real-time detection of posture**  
The guided voice allows the user to correct the posture described according to each body part, which is inputted through a webcam to provide postural estimation and feedback on the posture within the program.  
3️⃣ **Simple UI**   
The project also considered that 90% of the visually impaired people were low vision. So it provides a simple UI for low vision people. The web page is written in large letters, has large buttons that are easily visible, and has almost no movement between pages so that it is not difficult for users to use.

### Operation Process
> **[음성] 운동 선택 ➡️ [영상] 자세 측정 및 분석 ➡️ [음성] 피드백 ➡️ [영상] 카운팅**   
사용자는 제시되는 운동들 중 원하는 운동을 음성으로 선택하여 운동을 진행할 수 있다.  
프로그램은 자세를 음성으로 설명해준 뒤, 사용자의 자세를 웹캠으로 입력받는다.  
입력 받은 웹캠 영상을 tensorflow-posenet 비전 모델을 통해 딥러닝 하여 추정되는 신체의 17개 특징점을 통해 정확한 자세와 사용자의 자세를 비교하고, 음성으로 실시간 피드백 해준다.   
이 과정을 통해 사용자가 정확한 자세를 잡으면, 이후 운동을 계속해서 진행하고 동작 횟수를 카운팅한다.   
해당 시스템은 웹 페이지에서 구동된다.
  
> **[Voice] Motion Selection ➡️ [Image] Position Measurement and Analysis ➡️ [Voice] Feedback ➡️ [Image] Counting**  
The user can proceed the exercise by selecting the desired exercise in voice among the exercises presented.  
The program explains the posture with voice, and then the user's posture is entered into a webcam.  
Deep learning of inputted webcam images through the tensorflow-posenet vision model allows accurate posture and user posture to be compared through 17 characteristics of the body, and provides real-time feedback in voice.  
Through this process, when the user is in the correct position, the exercise continues and counts the number of movements.  
The system runs on web.

## Tech Skills and Tools
<p align="center">
 <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white"/></a> 
 <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=Django&logoColor=white"/></a> 
 <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=flat-square&logo=TensorFlow&logoColor=white"/></a> 
 <img src="https://img.shields.io/badge/NGINX-009639?style=flat-square&logo=NGINX&logoColor=white"/></a> 
 <img src="https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=HTML5&logoColor=white"/></a> 
 <img src="https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=CSS3&logoColor=white"/></a> 
 <img src="https://img.shields.io/badge/Bootstrap-7952B3?style=flat-square&logo=Bootstrap&logoColor=white"/></a> 
 <img src="https://img.shields.io/badge/Git-F05032?style=flat-square&logo=Git&logoColor=white"/></a> 
 <img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=GitHub&logoColor=white"/></a> 
 <img src="https://img.shields.io/badge/Visual Studio Code-007ACC?style=flat-square&logo=Visual Studio Code&logoColor=white"/></a> 
</p>

*Language:* Python 3.7  
*Framework:* Django 3.2.7  
*STT/TTS:* python-speech-recognition  
*Image Processing:* openCV 3.4.13, tensorflow-posenet 1.15.5 

## Browser Support
![Chrome](https://raw.githubusercontent.com/alrra/browser-logos/master/src/chrome/chrome_48x48.png) | ![IE](https://raw.githubusercontent.com/alrra/browser-logos/master/src/edge/edge_48x48.png) |
--- | --- |
Latest ✔| 10+ ✔ |

## Contributors
All participants in this project are majoring in Computer Science Engieneering, Dongguk University🏫

| Name                  | Email                  | Github                            | Role                          |
|-----------------------|------------------------|-----------------------------------|-------------------------------|
| 👧🏻 DongYeon Kang      | myjjue00@gmail.com     | https://github.com/dongyeon-0822  | Front-end, Speech Recognition |
| 🕵🏼‍♀ MinSeong Kang     | kdsvip5@naver.com      | https://github.com/minnseong      | Back-end, Image Processing    |
| 👱🏻‍♀️ Hyewon Kang       | gpffps369@gmail.com    | https://github.com/HyewonKkang    | Front-end, Speech Recognition |
| 👨🏻‍🦳 Woosung Kim       | woosung0420k@naver.com | https://github.com/WoosungMichael | Back-end, Image Processing    |
| 👩🏻‍💻 Sua Jang (Leader) | sooa9918@dgu.ac.kr     | https://github.com/sua1223        | Back-end, Image Processing    |

## Demo
[Youtube-Link](https://www.youtube.com/watch?v=2aFOzoOaKmU)

## License
PersonalTraining-for-Visually-Impaired is released under the Apache License 2.0.
