FROM python:3.9

WORKDIR /home/user

RUN apt-get update && apt-get install -y curl git pkg-config cmake

RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    && echo "$SNIPPET" >> "/root/.bashrc"

RUN python -m ensurepip --upgrade
RUN pip install --upgrade pip
RUN pip install pigar

COPY requirements.txt /home/user/blockchain/

RUN pip install -r /home/user/blockchain/requirements.txt

COPY src /home/user/blockchain/src
