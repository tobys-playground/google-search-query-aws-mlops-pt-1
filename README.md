# GPT-Neo + AWS MLOps Part 1 (Step Functions)

## Architecture

This part of the MLOps workflow focuses on a CI/CD CodePipeline (shaded in orange) for creating/updating an AWS Step Functions State Machine when there is a change to the code, which was written in the Data Science SDK for Python

## Steps

1) A commit made to the GitHub/CodeCommit repository will trigger the CodePipeline and start the CodeBuild job
2) CodeBuild will create/update the State Machine by running step_function.py
3) The State Machine can then be used by a second CodePipeline (Link to Repo: ) to train the GPT-Neo model and deploy it as an endpoint in SageMaker. If an execution of the State Machine is successful, it should look as below:

![image](https://user-images.githubusercontent.com/81354022/156025192-9a290312-2d6d-4339-b8f8-f5f7d1e025bb.png)
