FROM python:3.10

WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Streamlit config
RUN mkdir -p /root/.streamlit
RUN echo "\
[server]\n\
headless = true\n\
port = 7860\n\
enableCORS = false\n\
" > /root/.streamlit/config.toml

# Expose port
EXPOSE 7860

# Run app
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]