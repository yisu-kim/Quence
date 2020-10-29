# Quence

Sequence to Sequence 모델을 사용한 인공지능 시 짓기 체험 웹페이지

## 요구사항

- Linux 환경 (Ubuntu)
- python 3.6
- python3-pip
- python3-venv
- tensorflow 1.4.0
- Java 8
- git-lfs

## 환경 변수 설정

- SECRET_KEY

  .profile 파일에 `export SECRET_KEY='본인의 고유 비밀 키'`

## 설치 방법

1. 요구사항 사전 설치

2. Seq2Seq 모델 다운로드

   ```
   git lfs install
   git lfs pull
   ```

3. 가상환경 설정

   ```
   python3 -m venv myvenv
   ```

4. 가상환경 activate

   ```
   source myvenv/bin/activate
   ```

5. tensorflow 1.4.0 설치

   ```
   python3 -m pip3 install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.4.0-py3-none-any.wh
   ```

6. requirements의 패키지 설치

   ```
   pip3 install -r requirements.txt
   ```

7. migrate

   ```
   python3.6 manage.py migrate
   ```

8. static 설정

   ```
   python3.6 manage.py collectstatic
   ```

9. 서버 실행

   ```
   python3.6 manage.py runserver
   ```

## 사용 방법

1. `+` 버튼을 눌러 새롭게 시를 작성할 수 있다. 사용자는 시의 첫 행을 입력해야 한다.

   ![1](./images/1.png)

2. `한 줄 쓰기` 버튼을 누르면 사용자의 입력이 인공지능 모델에 전달된다. 이 모델은 사용자가 입력한 문장에 어울리는 다음 행을 3가지 생성한다.

   ![2](./images/2.png)

3. 사용자는 추천된 3가지 중 원하는 행을 선택할 수 있다. 선택된 행이 다음 행으로 저장된다.

   ![3](./images/3.png)

4. 계속 시 짓기를 원하면 `만들기` 버튼을 누른다. 모델은 이전 행을 입력으로 받아 다시 3가지 추천 결과를 생성한다.

   ![4](./images/4.png)

5. 사용자는 다시 원하는 행을 선택할 수 있다.

   ![5](./images/5.png)

6. 시가 완성되었다면 `출판하기` 버튼을 누른다. 이제 시작 페이지에서 완성된 시를 확인할 수 있다.

   ![6](./images/6.png)
