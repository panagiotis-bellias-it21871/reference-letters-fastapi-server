# Use an existing docker image as a base
FROM python:3.7-buster

# Change working directory to /code. This is where we'll put the requirements.txt file and the app directory.
WORKDIR /app

# Copy the file with the requirements
COPY ./requirements.txt ./

# Copy main.py file
COPY ./app ./



# set user:group
RUN groupadd appuser && \
    useradd -g appuser -d /app -M appuser
# change permission on workdir
RUN chown -R appuser:appuser /app

USER appuser:appuser
ENV PATH=$PATH:/app/.local/bin

# Install the package dependencies in the requirements file.
RUN pip install -r requirements.txt

# Tell what to do when it starts as a container
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]