FROM python:3

WORKDIR /usr/src/app
COPY requirements.txt .
RUN python3 -m venv venv
RUN . venv/bin/activate
RUN pip install -r requirements.txt
COPY . .

EXPOSE 6060
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]