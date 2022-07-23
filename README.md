# Trading bot

### Set up environment

1. Download python 3.9 on your mac using brew: `brew install python@3.9 && brew link --overwrite python@3.9`, you can verify you are now using python 3.9 with `python3 -V`.
2. Set up a python virtual environment named "venv" with python 3.10: `python3 -m venv "venv"`.
3. Activatçe the environment: `source venv/bin/activate`
4. Install dependencies: `pip3 install -r requirements.txt`
5. Install the AWS SAM CLI (ref: [AWS documenation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-mac.html)): `brew install aws-sam-cli`

### Dev workflow

1. Activate the environment: `source venv/bin/activate`
2. Run unit tests using pytest: `python3 -m pytest tests/unit/* `
