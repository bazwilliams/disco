FROM python:3.6
RUN pip3 install phue rgbxy paho-mqtt
ADD app.py /app/
CMD python3 /app/app.py
