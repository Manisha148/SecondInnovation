
FROM python:3.9
WORKDIR /app
COPY . /app
ARG OPENAI_API_KEY

# Set the OpenAI API key as an environment variable
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install openai
# Make port 80 available to the world outside this container
EXPOSE 88

CMD ["python", "app.py"]



