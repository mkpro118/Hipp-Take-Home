# Start from the stable Python 3.11 version
FROM python:3.11

# Update software
RUN apt-get update && apt-get install --no-install-recommends -y \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# The primary directory will be the /src in all apps
RUN mkdir src
WORKDIR /src

COPY . .

# Install dependencies
RUN pip install -r requirements.txt

CMD ["python3", "app.py"]
