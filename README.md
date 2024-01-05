# Note this application is for fun and development purposes ***only***

# ai-image-classification

This repo contains the code to build an image classification app powered by AI. The application has been built to run using Docker locally or EKS in AWS. The application also uses Python, PyTorch, Flask, and ResNet.

## Prerequisites for a local run:
- Python
- Pip
- Docker
- GitHub account
- Basic understanding of git

## Prerequisities for a deployment to EKS:
- AWS account
- AWS CLI
- Terraform Cloud account with an organization
- GitHub account
- Python
- Pip
- Docker
- Basic understanding of git and Terraform

## To use this application locally without deploying to EKS, follow the steps below:

1. Clone this repo

2. Open the terminal and navigate to the root of the repo

3. Run: 
```docker build -t ai-image-classification -f docker/Dockerfile .```
```docker run -p 4000:5000 ai-image-classification```

4. Open your browser and go to http://localhost:4000

5. Upload a png or jpeg image


## To deploy this application to EKS, follow the steps below:

1. In GitHub, [Fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) this repo

2. In AWS:
    - Create an AWS S3 bucket to serve as the Terraform backend. 
        - The Terraform state files will be stored here
    - Create an AWS IAM user to be used by GitHub to deploy the IaC to AWS. 
        - On step two of user creation, in the Permissions Options box select: Attach policies directly
        - In the Permissions policies box, click 'Create Policy':
        - Select JSON in the Policy editor box
        - Copy and paste the policy found at this path in the forked repo: resources/ci-cd-user-perms.json **(Update lines 26-27 with the name of the bucket you created for the Terraform files)**. 
    - Create and export AWS access keys for a third-party purpose with CLI access only.
    

3. Create a workspace in Terraform Cloud for this project and select API driven workflow.

4. In the Terraform Cloud workspace, go to Settings > Variables > Workspace Settings. 
    - Create entries for AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
    - For the values, use the values from the AWS IAM user created earlier

5. In Terraform Cloud, from the Projects and Workspaces page, go to Settings > Teams 
    - Generate an API token with the Description 'GitHub Actions' that will expire in 30 days.
    - Save the token securely as it will later be added to GitHub

6. In GitHub, go to the forked repository > Settings > Secrets and variables > Actions 
    - Create a secret named TF_API_TOKEN and enter the Terraform API Token
    - Create a secret named AWS_ACCESS_KEY_ID and enter the associated value
    - Create a secret named AWS_SECRET_ACCESS_KEY and enter the associated value
    - Create a secret named BUCKET_TF_STATE and enter the name of the AWS S3 bucket created earlier

7. Clone the repo to your local machine.

8. Navigate to infra/main.tf.
    - Update the cluster name.
        - Note that if you change the version of the Terraform provided modules, you may experience Terraform versioning errors.
    - Create a new branch.
    - Commit and push your changes to the branch.

9. Open a PR from the new branch to the main branch, and merge once builds have passed.

10. Once resources are deployed to AWS, build the Dockerfile.
    - Run ```aws configure```
        - Use the values from the IAM user created earlier.
    - Navigate to the AWS console
        - Go to ECR > the newly creates repository > view push commands
        - See the section below if you are not using a machine with amd64 architecture. Otherwise, continue.
        - The commands will be slighlty modified (update the account number and region as necessary):
            - ```aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com```
            - ```docker build -t k8s-ai-image-processer -f docker/Dockerfile .```
            - ```docker tag k8s-ai-image-processer:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/k8s-ai-image-processer:latest```
            - ```docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/k8s-ai-image-processer:latest```
    - If you are not using a machine with amd64 architecture, the file will need to be built using buildx
        - In Docker Desktop, go to Settings > Docker Engine 
        - Change the "experimental" value to true.
        - Click Apply & Restart.
        - Run the following commands (they may take some time to run):
            - ```aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com```
            - ```docker buildx create --use --name dkr-builder``` # optional: choose a different name 
            - ```docker buildx inspect --bootstrap```
            - ```docker buildx build --platform linux/amd64 -t 123456789012.dkr.ecr.us-east-1.amazonaws.com/k8s-ai-image-processer:latest -f docker/Dockerfile . --push```

11. Navigate to the AWS Console > ECR > the newly creates repository > click the image just pushed
    - Copy the URL that includes the sha value. 
    - Paste the value on line 29 in kubernetes/deployment.yaml.
    - Run the following commands:
        - ```kubectl create ns ai-process```
        - ```kubectl apply -f kubernetes/deployment.yaml```
            - Wait for the pod to be in a running status: ```kubectl get pods -n=ai-process```
        - ```kubectl apply -f kubernetes/service.yaml```
        - ```kubectl get service ai-lb-service -n=ai-process``` # this may take some time to provision
            - Once the public endpoint is available, navigate to your browser and paste the endpoint.
            - Upload a jpeg or png image and submit it.
        - Clean up the Kubernetes deployment and service
            - ```kubectl delete service ai-lb-service -n=ai-process```
            - ```kubectl delete deployment ai-processing-app -n=ai-process```

12. On your local machine, navigate to the infra folder in the cloned repo:
    - Comment out the contents in the following files:
        - ecr.tf
        - eks.tf
        - networking.tf
    - Commit and push the changes to the repo.
    - Create a pull request. Analyze the plan.
    - Merge the changes to delete the created resources.

13. In AWS:
    - Empty the S3 bucket
    - Delete the bucket
    - Delete the IAM user

# Awesome job deploying an AI image classification app to AWS EKS! 



