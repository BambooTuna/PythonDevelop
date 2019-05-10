FROM python:3.6.6

RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "vim"]

ARG project_dir=/bot/bitflyer
WORKDIR $project_dir

COPY ./ $project_dir/PythonDevelop

WORKDIR $project_dir/PythonDevelop
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "python", "Main.py" ]