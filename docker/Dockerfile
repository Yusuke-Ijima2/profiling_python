FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt ./
RUN apt-get update && apt-get install -y --no-install-recommends gcc g++ python3-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove gcc g++ python3-dev


COPY . .

CMD [ "python", "./script/line_line_profiler.py" ]
