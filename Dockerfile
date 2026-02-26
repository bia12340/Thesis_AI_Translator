Spaces
Hugging Face's logo
Bia12340
/
translator-backend 

like
0


🐳 Get started with your Docker Space!
Your new Space has been created, follow these steps to get started (or read the full documentation)

Start by cloning this repo by using:

Use an access token as git password/credential


# When prompted for a password, use an access token with write permissions.
# Generate one from your settings: https://huggingface.co/settings/tokens
git clone https://huggingface.co/spaces/Bia12340/translator-backend

# Make sure the hf CLI is installed
powershell -ExecutionPolicy ByPass -c "irm https://hf.co/cli/install.ps1 | iex"

# Download the Space
hf download Bia12340/translator-backend --repo-type=space
Let's create a simple Python app using FastAPI:

requirements.txt


fastapi
uvicorn[standard]
Hint You can also create the requirements file file directly in your browser.
app.py


from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def greet_json():
    return {"Hello": "World!"}
Hint You can also create the app file file directly in your browser.
Create your Dockerfile:


# Read the doc: https://huggingface.co/docs/hub/spaces-sdks-docker
# you will also find guides on how best to write your Dockerfile

FROM python:3.9

RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY --chown=user . /app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
Hint Alternatively, you can create the Dockerfile file directly in your browser.
Then commit and push:


git add requirements.txt app.py Dockerfile
git commit -m "Add application file"
git push
Finally, your Space should be running on this page after a few moments!

App port

Your Docker Space needs to listen on port 7860.

Personalize your Space

Make your Space stand out by customizing its emoji, colors, and description by editing metadata in its README.md file.

Documentation

Read the full documentation for Docker Spaces here.

