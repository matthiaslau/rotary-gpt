ARG PYTHON_VERSION=3.11

FROM python:${PYTHON_VERSION}

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-setuptools \
    python3-wheel \
    ffmpeg

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .


EXPOSE 5060 5004

# replace APP_NAME with module name
CMD ["python", "rotarygpt.py"]
