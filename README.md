# BYOC GPT-Neo + AWS MLOps Part 1 (Step Functions)

## Architecture

This part of the MLOps workflow focuses on the **first CodePipeline (shaded in orange)** for creating/updating an AWS Step Functions State Machine when there is a change to the code, which was written in the Data Science SDK for Python.

## Steps

1) A commit made to the **GitHub/CodeCommit repository** will trigger the **CodePipeline** and start the **CodeBuild** job
2) **CodeBuild** will create/update the **State Machine** by running **step_function.py**
3) The State Machine can then be used by the second CodePipeline (Link to Repo: ) to train the Bring-Your-Own-Container GPT-Neo model and deploy it as an endpoint in SageMaker. If an execution of the State Machine is successful, it should look as below:

