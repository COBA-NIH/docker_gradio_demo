# ctromanscoia/docker-gradio-demo:0.1
# docker build -t ctromanscoia/docker-gradio-demo:0.1 . 
# docker run --user $(id -u):$(id -g) --rm=true -it -v $(pwd):/scratch -w /scratch ctromanscoia/docker-gradio-demo:0.1 /bin/bash
# docker push ctromanscoia/docker-gradio-demo:0.1

# Define an image to start from. 
FROM python:3.9-slim

# Install the dependencies for the gradio app
RUN python -m pip install gradio scipy scikit-image

# Add app.py from the directory where `docker build` was run and add it into the
# workspace directory within the container
ADD app.py /workspace/

# Run the app. Will be accessible at http://localhost:8000/
CMD [ "python3" , "/workspace/app.py" ]

# docker run -it --rm -p 127.0.0.1:8000:8000 ctromanscoia/docker-gradio-demo:0.1