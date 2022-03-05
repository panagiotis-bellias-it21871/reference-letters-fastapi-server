# Use an existing docker image as a base
FROM python:3.9-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the current working directory to /code. This is where we'll put the requirements.txt file and the app directory.
WORKDIR /code

RUN groupadd appuser &&  useradd -g appuser -d  /code -M appuser

# change permission on workdir
RUN chown -R appuser:appuser /code

USER appuser:appuser
ENV PATH=$PATH:/code/.local/bin
#Change working directory

# Copy the file with the requirements to the /code directory.
COPY ./requirements.txt /code/requirements.txt

# Install the package dependencies in the requirements file.
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the ./app directory inside the /code directory.
COPY ./app /code/app

USER root
RUN chown -R appuser:appuser /code

USER appuser:appuser
# static files?
EXPOSE 8000/tcp

# Set the command to run the uvicorn server.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
