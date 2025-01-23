FROM python:3.12
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY ./api /code/api
COPY ./core /code/core
COPY main.py /code/main.py

CMD ["python3", "main.py"]


# Python 3.12 이미지를 기반으로 시작
FROM python:3.12

# ARG를 사용하여 빌드 시 필요한 민감한 정보들을 받는다
ARG SECRET_KEY
ARG DATABASE_PASSWORD
ARG KAKAO_CLIENT_SECRET
ARG KAKAO_REST_API_KEY
ARG ACCESS_TOKEN_EXPIRE_MINUTES
ARG REFRESH_TOKEN_EXPIRE_MINUTES

# 환경 변수를 설정하여 애플리케이션에서 사용
ENV SECRET_KEY=${SECRET_KEY}
ENV DATABASE_PASSWORD=${DATABASE_PASSWORD}
ENV KAKAO_CLIENT_SECRET=${KAKAO_CLIENT_SECRET}
ENV KAKAO_REST_API_KEY=${KAKAO_REST_API_KEY}
ENV ACCESS_TOKEN_EXPIRE_MINUTES=${ACCESS_TOKEN_EXPIRE_MINUTES}
ENV REFRESH_TOKEN_EXPIRE_MINUTES=${REFRESH_TOKEN_EXPIRE_MINUTES}

# 작업 디렉토리 설정
WORKDIR /code

# requirements.txt를 복사하고 의존성 설치
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 애플리케이션 코드 복사
COPY ./app /code/app
COPY ./api /code/api
COPY ./core /code/core
COPY main.py /code/main.py

# FastAPI 앱을 실행할 때 사용하는 명령
CMD ["python3", "main.py"]

