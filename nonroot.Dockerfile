# Use an existing docker image as a base
FROM python

# Change working directory to /usr/data. This is where we'll put the requirements.txt file and the app directory.
WORKDIR /usr/data

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN groupadd appuser &&  useradd -g appuser -d  /usr/data -M appuser 

ENV PATH=$PATH:/usr/data/.local/bin

# Copy the file with the requirements
COPY ./requirements.txt ./

# Copy main.py file
COPY ./ref_letters app

# Install the package dependencies in the requirements file.
RUN pip install -r requirements.txt

# change permission on workdir
RUN chown -R appuser:appuser /usr/data

USER appuser:appuser

EXPOSE 8000/tcp
# Tell what to do when it starts as a container
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
