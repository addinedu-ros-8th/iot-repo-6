# GreenT

> *(KDT) ROS2와 인공지능을 활용한 자율주행 로봇 개발자 양성과정 8기* 교육과정 내에서 Internet of Things를 주제로한 과제입니다.

IoT 센서와 자동화 시스템을 활용한 스마트 농업 자동화 시스템 개발 프로젝트입니다.
하드웨어 컨트롤러 개발과 백엔드 시스템 구축을 주로 담당하였습니다.


## 프로젝트 개요
- **기간**: 2025.02.05 ~ 2025.02.27 (4주)
- **역할**: 하드웨어 컨트롤러 개발 및 시스템 통합 담당
- **팀명**: Druid

### 프로젝트 배경 및 목표

- 기술을 통해 농업을 최적화하기 위해 고안된 스마트팜 프로젝트
- 다양한 IoT 디바이스, 센서, 자동화 시스템을 통합하여 농업 효율성을 높임
  - 환경 조건에 따른 자동 관개 시스템
  - 토양 수분, 온도, 습도 실시간 모니터링
  - 작물 수확량 및 자원 사용량 최적화를 위한 데이터 분석
  - 농장 관리를 위한 사용자 친화적인 인터페이스


### **Druid** 팀원 및 역할

| 역할 | 이름 (GitHub ID) | 주요 업무 요약 |
|------|------------------|----------------------------------------------------------|
| 팀원 | 김연우 ([@yonmilk](https://github.com/yonmilk)) | - 센서 및 액추에이터 연동을 위한 시스템 컨트롤러 개발<br />- PyQt5 GUI와 하드웨어 시스템 간 실시간 통신 구현<br />- MySQL 데이터베이스 통합<br />- GUI 및 통신 설계 |
| 팀원 | 박정배 ([@pjb804](https://github.com/pjb804)) | - 하드웨어 설계 및 구축<br />- 3D 프린터를 활용한 프로토타입 제작<br />- 데이터베이스 설계 및 구현<br />- PyQt5 GUI 개발 및 데이터베이스간 연동 |
| 팀장 | 임동욱 ([@Donguk-popo](https://github.com/Donguk-popo)) | - 시스템 아키텍처 설계<br />- 하드웨어 구축 및 테스트<br />- PyQt5 UI 프로토타입 구축 및 GUI 개발<br />- GUI와 데이터베이스간 연동 및 테스트 |


### 기술 스택

| 분류             | 기술 요소 |
|------------------|------------------------------------------------------------------|
| 언어 | Python, C++ |
| 하드웨어 | Raspberry Pi 4, Arduino, ESP32 |
| 센서 | 토양 수분 센서, 온습도 센서 (DHT), 조도 센서, RFID |
| 액추에이터 | 워터 펌프, 스텝 모터, LED 조명, 선풍기 |
| 통신 | Serial, TCP/IP(서버 간 데이터 전송) |
| GUI | PyQt5 |
| 데이터베이스 | MySQL |
| 영상 처리 | OpenCV, Raspberry Pi Camera |
| 라이브러리 | mysql-connector-python, python-dotenv, pyserial |
| 협업 도구 | Git, Slack, Jira, Confluence |



### 주요 담당 업무

**센서 및 하드웨어 연동**
- 아두이노, Raspberry Pi, 센서 연동을 통한 자동 급수, 출입 제어 시스템 개발
- 토양 수분 센서를 활용한 수분 감지 및 자동 워터 펌프 제어 기능 구현 (아두이노 C++ 라이브러리 활용)
  - DHT: 온습도 센서 제어 및 데이터 수집
  - Servo: 서보모터 출입문 개폐 시스템
  - Stepper: 스텝모터를 이용한 카메라 각도 조절
  - MFRC522: RFID 리더 제어 및 태그 인식
- Raspberry Pi 카메라 영상 스트리밍 구현
- RFID 인식 기반 출입 제어 기능을 시스템 제어 로직에 통합

**시스템 통합 및 데이터 관리**
- GUI 및 통신 설계
- Python 기반 시스템 컨트롤러 개발
- 시리얼 통신을 통한 하드웨어와 소프트웨어 연동
- MySQL 데이터베이스를 활용한 센서 데이터 및 사용자 정보 관리
- PyQt5 GUI와 하드웨어 시스템 간 실시간 통신 구현


## 프로젝트 결과 및 자료

![rfid](https://github.com/user-attachments/assets/4d9c48bb-3b7e-4cfa-b250-1cc47287ff57)


<table>
<tr>
  <td width="33%">
     <img width="712" height="744" alt="FarmProgram-01" src="https://github.com/user-attachments/assets/788ce79c-8211-49e5-b17c-509e612dfff4" /></td>
   <td width="33%">
     <img width="583" height="527" alt="FarmProgram-02-admin" src="https://github.com/user-attachments/assets/c88d0128-002e-4b6a-a779-a1d57074f7b9" /></td>
  <td width="33%">
      <img width="648" height="504" alt="FarmProgram-03-admin" src="https://github.com/user-attachments/assets/1cf743cc-8b6d-4c26-8cc8-55ea5f408a44" /></td>
<tr>
<tr>
   <td width="33%">
      <img width="648" height="560" alt="FarmProgram-04-admin" src="https://github.com/user-attachments/assets/629859c7-4cc3-472b-a50b-809c585a9174" />

   </td>
   <td width="33%">
      <img width="1292" height="870" alt="FarmProgram-05-admin" src="https://github.com/user-attachments/assets/fe8dbca1-305f-4011-a362-7c662fd65c5e" />

   </td>
   <td width="33%">
      <img width="650" height="560" alt="FarmProgram-06-admin" src="https://github.com/user-attachments/assets/9f3c0459-dd28-4731-9bb1-9c48af46c93b" />

   </td>
</tr>

<tr>
   <td width="33%">
      <img width="650" height="558" alt="FarmProgram-07-admin" src="https://github.com/user-attachments/assets/3f6007a7-172e-4d95-93fe-cddab9c89ac6" />
   </td>
   <td width="33%">
      <img width="586" height="529" alt="FarmProgram-08-admin" src="https://github.com/user-attachments/assets/a474a8ff-0cbf-4eec-806c-8347c8e0932e" />
   </td>
   <td width="33%">
      <img width="649" height="560" alt="FarmProgram-09-admin" src="https://github.com/user-attachments/assets/ae4b263a-728c-4805-b541-5d9d7af1917b" />
   </td>
</tr>
<tr>
   <td width="33%"><img width="445" height="300" alt="FarmProgram-10-user" src="https://github.com/user-attachments/assets/7fc6ef4c-5ee0-4e8f-b476-65efbb483298" />
</td>
   <td width="33%"><img width="721" height="756" alt="FarmProgram-11-user-kit-rental" src="https://github.com/user-attachments/assets/04c1dc4a-53ff-4cc0-9cb8-87be9cf3d7e0" />
</td>
   <td width="33%"><img width="641" height="811" alt="FarmProgram-12" src="https://github.com/user-attachments/assets/1e1d6307-42a7-46dd-88eb-884340358207" />
</td>
</tr>
</table>


<img width="1503" height="1287" alt="FarmProgram-13-plant_detail" src="https://github.com/user-attachments/assets/f240a15e-271a-44c2-ab69-0bf65a10c3fc" />


<br/>
<br/>
<br/>

### 프로토타입(3d Modeling)

<img width="3987" height="1654" alt="1 각_부품이_모여서" src="https://github.com/user-attachments/assets/9f46fa83-b50a-480d-8750-14aac404e705" />

<table>
   <tr>
      <td width="33%"><img width="466" height="545" alt="2 하나의_키트를_이루고_1" src="https://github.com/user-attachments/assets/1d8e4c7b-023e-4098-94e8-7fa9cf2b4a59" />
</td>
      <td width="33%"><img width="682" height="784" alt="2 하나의_키트를_이루고_2" src="https://github.com/user-attachments/assets/0484d507-d7cd-45ae-8fbd-77fe31374a96" />
</td>
      <td width="33%"><img width="625" height="534" alt="3 세트가_되며" src="https://github.com/user-attachments/assets/ce8bd633-6e32-475f-9d58-10a1248fa64b" />
</td>
   </tr>
</table>

<img width="896" height="266" alt="4 하나의_스마트팜_완성" src="https://github.com/user-attachments/assets/4660d567-70fa-4076-a0ad-8919459f7f8d" />



<br/>
<br/>
<br/>


### 시스템 구조

- Farm Service(Kit 한 개)
- Farm Controller(하드웨어 제어)
- GreenT Service(Farm Kit 전체)
- Admin Service(관리자 GUI)
- User Service(사용자 GUI)

<img width="972" height="531" alt="sa_hardware_architecture" src="https://github.com/user-attachments/assets/69018be1-917e-4cb4-9ade-3db7b91cfdf7" />


<img width="961" height="523" alt="sa_software_architecture" src="https://github.com/user-attachments/assets/e5016957-c9f5-4287-bd1a-2b324e439c10" />



### 데이터 구조

<img width="961" height="730" alt="데이터베이스_전체" src="https://github.com/user-attachments/assets/664a80fa-7365-4b6e-a485-43bd01aaea5b" />

<table>
   <tr>
      <td width="33%"><img width="483" height="357" alt="데이터베이스_개별_1" src="https://github.com/user-attachments/assets/c5429850-41c4-441e-9282-d8be503e7713" />
</td>
      <td width="33%"><img width="1099" height="557" alt="데이터베이스_개별_2" src="https://github.com/user-attachments/assets/06a69f6d-a2f6-4cb1-832c-3196da01508e" />
</td>
      <td width="33%"><img width="966" height="557" alt="데이터베이스_개별_3" src="https://github.com/user-attachments/assets/a866a9a6-99ff-4fef-99fd-3660773f9139" />
</td>
   </tr>
</table>

