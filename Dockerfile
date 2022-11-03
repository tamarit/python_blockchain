FROM python:3.9

WORKDIR /home/user

RUN apt-get update && apt-get install -y curl git pkg-config cmake

RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    && echo "$SNIPPET" >> "/root/.bashrc"

# RUN apt-get clean && apt-get update
# RUN apt-get install -y zbar-tools 
# RUN apt-get install -y apt-transport-https
# RUN apt-get install -y ffmpeg libsm6 libxext6 
# RUN apt-get install -y poppler-utils
RUN python -m ensurepip --upgrade
RUN pip install --upgrade pip
RUN pip install pigar

COPY requirements.txt /home/user/blockchain/

RUN pip install -r /home/user/blockchain/requirements.txt

COPY src /home/user/blockchain/src