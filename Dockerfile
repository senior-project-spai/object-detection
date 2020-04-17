FROM tensorflow/tensorflow:1.4.0-py3

WORKDIR /python-app

# FIX open-cv
RUN apt-get update && apt-get install -y libsm6 libxext6 libxrender-dev 

# FIX matplotlib
RUN apt-get install -y python3-tk

# Copy requirement python package
COPY requirements.txt .

# Install python package
RUN python3 -m pip install -r requirements.txt

# Download model
ADD https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5 .

COPY src/ .

CMD ["python3", "./app.py"]