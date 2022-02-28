from stepfunctions.steps import (Chain, TrainingStep, ModelStep, EndpointConfigStep, EndpointStep)
from stepfunctions.workflow import Workflow
from stepfunctions.inputs import ExecutionInput
from sagemaker.estimator import Estimator 
import os
import uuid

workflow_execution_role = os.environ['WORKFLOW_EXECUTION_ROLE']
training_instance = os.environ['TRAINING_INSTANCE']       
image_uri = os.environ['IMAGE_URI']
estimator_role = os.environ['ESTIMATOR_ROLE']  
hosting_instance = os.environ['HOSTING_INSTANCE']  

hyperparameters={
                 'epoch' : 1
                 }

gptneo = Estimator(
        image_uri = image_uri,
        instance_type = training_instance,
        instance_count = 1,
        role = estimator_role,
        use_spot_instances = True,
        max_run = 300,
        max_wait = 360,
        hyperparameters = hyperparameters
)              

execution_input = ExecutionInput(schema ={
    'JobName': str, 
    'ModelName': str,
    'ArtifactLocation' : str,
    'EndpointName': str,
    'DataLocation': str
    
})

train_step = TrainingStep(
    'Training Model', 
    estimator=gptneo,
    data=execution_input['DataLocation'],
    job_name=execution_input['JobName'],
    output_data_config_path = execution_input['ArtifactLocation']
)

model_step = ModelStep(
    'Saving model',
    model=train_step.get_expected_model(),
    model_name=execution_input['ModelName'],
    instance_type=training_instance
)

endpoint_config_step = EndpointConfigStep(
    'Creating Endpoint Config',
    endpoint_config_name=execution_input['ModelName'],
    model_name=execution_input['ModelName'],
    initial_instance_count=1,
    instance_type=hosting_instance
)

endpoint_step = EndpointStep(
    'Creating Endpoint',
    endpoint_name=execution_input['EndpointName'],
    endpoint_config_name=execution_input['ModelName']
)

workflow_definition = Chain([
    train_step,
    model_step,
    endpoint_config_step,
    endpoint_step
])

workflow = Workflow(
    name='Workflow-GPTNeo-BYOC-{}'.format(uuid.uuid1().hex),
    definition=workflow_definition,
    role=workflow_execution_role
)

workflow.create()