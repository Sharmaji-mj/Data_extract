FROM python:3.13

# Install system dependencies and Chromium
RUN apt-get update && apt-get install -y \
    wget curl gnupg \
    chromium chromium-driver \
    unzip libnss3 libgconf-2-4 libxi6 libxcursor1 \
    libxss1 libxcomposite1 libasound2 libxtst6 \
    libatk1.0-0 libcups2 libxrandr2 libgtk-3-0 \
    fonts-liberation libappindicator3-1 xdg-utils git \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

RUN apt install git

# Point Selenium at the Chromium binary
ENV CHROME_BIN=/usr/bin/chromium

WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["tail","-f","/dev/null"]
