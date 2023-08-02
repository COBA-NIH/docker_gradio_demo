# bethcimini/docker-gradio-demo:latest
# docker build -t bethcimini/docker-gradio-demo:latest . 
# docker run -it --rm -p 127.0.0.1:8000:8000 bethcimini/docker-gradio-demo:latest
# docker push bethcimini/docker-gradio-demo:latest

# Define an image to start from. 
FROM python:3.9-slim

# Install the dependencies for the gradio app
RUN python -m pip install gradio==3.25.0 gradio_client==0.1.3 scipy==1.9.1 scikit-image==0.20.0

# Add app.py from the directory where `docker build` was run and add it into the
# workspace directory within the container
ADD app.py /workspace/

# Expose port 8000. You CAN do this from the command line, but it makes it possible to run entirely in the app
EXPOSE 8000

# Run the app. Will be accessible at http://localhost:8000/
CMD [ "python3" , "/workspace/app.py" ]
