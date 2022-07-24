# Trading bot

### App Architecture

![Imgur](https://i.imgur.com/DatEUXu.png)

TODO

### Pipeline Architecture

TODO

### Set up environment

1. Download python 3.9 on your mac using brew: `brew install python@3.9 && brew link --overwrite python@3.9`, you can verify you are now using python 3.9 with `python3 -V`.
2. Set up a python virtual environment named "venv" with python 3.9: `python3 -m venv "venv"`.
3. Activate the environment: `source venv/bin/activate`
4. Install dependencies: `pip3 install -r requirements.txt`
5. (Optional) Install the AWS SAM CLI (ref: [AWS documenation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-mac.html)): `brew install aws-sam-cli`

### Dev workflow

1. Activate the environment: `source venv/bin/activate`
2. Run unit tests using pytest: `python3 -m pytest tests/unit/*`

### TODO + Improvements:

- Migrate app to SAM (Serverless Application Model). Refs:
  - [Tutorial: Deploying a Hello World application](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html)
  - [API Gateway to Lambda to DynamoDB example](https://serverlessland.com/patterns/apigw-lambda-dynamodb)
  - [Github Serveless App examples](https://github.com/amazon-archives/serverless-app-examples/tree/master/python)
- Migrate pipeline to SAM. Refs:
  - [Tutorial: Create a pipeline that publishes your serverless application to the AWS Serverless Application Repository](https://docs.aws.amazon.com/codepipeline/latest/userguide/tutorials-serverlessrepo-auto-publish.html)
  - [Github Action: AWS CodePipeline SAR Auto-Publish](https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:077246666028:applications~aws-serverless-codepipeline-serverlessrepo-publish)
- Add pipeline to CloudFormation template (propably can be done as part of SAM migration).
- Add integration test ran in pipeline.
