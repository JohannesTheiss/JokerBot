FROM python:3.10-alpine

# Install packages
RUN apk add --update --no-cache musl-dev linux-headers g++ build-base py-pip jpeg-dev zlib-dev

# Upgrade pip
RUN python3 -m pip install --upgrade pip

# Setup app
RUN mkdir -p /app

# Switch working environment
WORKDIR /app

# Add application
COPY . .

# Install requirements
RUN pip install -r requirements.txt

# Start the bot
CMD [ "python", "run.py" ]
