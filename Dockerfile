FROM python:3.13
 
 
 
# Install dependencies for Chrome
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg \
    libnss3 libgconf-2-4 libxi6 libxcursor1 libxss1 libxcomposite1 libasound2 libxtst6 libatk1.0-0 libcups2 libxrandr2 libgtk-3-0 \
    fonts-liberation libappindicator3-1 xdg-utils \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*
 
RUN apt install git
 
# Install Chromium
RUN apt-get update && apt-get install -y wget gnupg2
 
# Add Google’s signing key & Chrome repo
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
 
# Install specific version (v114)
RUN apt-get update && apt-get install -y \
    google-chrome-stable

# Set environment variable for Chrome binary
ENV CHROME_BIN=/usr/bin/chromium
 
# Set work directory
WORKDIR /app
 
# Copy files
COPY . .
 
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
 
# Run script
CMD ["tail", "-f","/dev/null"]

