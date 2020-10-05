FROM python

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app/
RUN ["chmod", "+x", "/usr/src/app/wait-for-it.sh"]