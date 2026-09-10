🚀 KubeMind AI --- AWS DevOps CI/CD Hands-On Lab

End-to-end hands-on project: GitHub → GitHub Actions → OIDC → AWS
IAM → ECR → ECS Fargate → ALB → Flask

Region: ap-south-1 (Mumbai)
Repository: Alamgir00/kubemind-aws-devops

Table of Contents

Project Overview

Architecture

Technology Stack

Repository Structure

Prerequisites

Phase 1 --- Application

Phase 2 --- Docker

Phase 3 --- Tests

Phase 4 --- ECR

Phase 5 --- Terraform Backend

Phase 6 --- Terraform
Infrastructure

Phase 7 --- ECS Verification

Phase 8 --- GitHub Repository

Phase 9 --- GitHub OIDC

Phase 10 --- GitHub Actions

Phase 11 --- End-to-End
Verification

IAM Security Model

Troubleshooting

Useful Commands

Production Hardening Roadmap

Lessons Learned

Final Checklist

1. Project Overview

KubeMind AI is a hands-on DevOps laboratory that builds a containerized
Flask application and deploys it to AWS using Infrastructure as Code and
automated CI/CD.

The final deployment provides:

Terraform-managed AWS infrastructure

Docker containerization

Amazon ECR image registry

Amazon ECS Fargate

Application Load Balancer

Private ECS subnets

CloudWatch logs

GitHub Actions CI/CD

GitHub OIDC authentication

Short-lived AWS credentials

Git-SHA image tagging

Automated tests before deployment

The final runtime was validated with 2/2 ECS tasks running, an
ACTIVE ECS service, a healthy ALB target group, / returning the
application message, and /health returning {"status":"healthy"}.

2. Architecture

Application/runtime architecture

                         INTERNET
                            |
                         HTTP :80
                            |
                            v
                 +----------------------+
                 | Application Load     |
                 | Balancer             |
                 +----------+-----------+
                            |
                         HTTP :8080
                            |
                            v
                 +----------------------+
                 | Target Group         |
                 +----------+-----------+
                            |
              +-------------+-------------+
              |                           |
              v                           v
      +------------------+        +------------------+
      | ECS Fargate      |        | ECS Fargate      |
      | Task 1           |        | Task 2           |
      | Private Subnet A |        | Private Subnet B |
      | :8080            |        | :8080            |
      +------------------+        +------------------+

CI/CD architecture

Developer
   |
   | git push main
   v
GitHub Repository
   |
   v
GitHub Actions
   |
   +--> pytest
   |
   +--> GitHub OIDC
   |       |
   |       v
   |   AWS STS / IAM
   |
   +--> Docker Build
   |
   +--> Docker Push
           |
           v
       Amazon ECR
           |
           v
       ECS Task Definition
           |
           v
       ECS Fargate
           |
           v
          ALB
           |
           v
     KubeMind AI

3. Technology Stack

Layer            Technology

Application      Python 3.12 / Flask
Server           Gunicorn
Testing          Pytest
Container        Docker
IaC              Terraform
Cloud            AWS
Registry         Amazon ECR
Compute          Amazon ECS Fargate
Load Balancer    Application Load Balancer
Network          Amazon VPC
Logs             CloudWatch
CI/CD            GitHub Actions
Authentication   GitHub OIDC
State            Amazon S3
Source Control   GitHub

4. Repository Structure

kubemind-aws-devops/
├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── src/
│   │   └── app.py
│   └── tests/
│       └── test_app.py
├── terraform/
│   ├── backend.tf
│   ├── providers.tf
│   ├── versions.tf
│   ├── variables.tf
│   ├── main.tf
│   ├── outputs.tf
│   ├── security_groups.tf
│   ├── alb.tf
│   ├── iam.tf
│   ├── ecs.tf
│   ├── task_definition.tf
│   ├── ecs_service.tf
│   ├── github-actions-trust-policy.json
│   └── github-actions-permissions-policy.json
├── .github/
│   └── workflows/
│       └── deploy.yml
├── .gitignore
└── README.md

5. Prerequisites

Install:

git --version
docker --version
python3 --version
terraform version
aws --version

Verify AWS identity:

aws sts get-caller-identity

This lab used an EC2 IAM role for AWS CLI/Terraform access instead of
static AWS access keys.

Set the region:

export AWS_DEFAULT_REGION=ap-south-1
aws configure set region ap-south-1

6. Phase 1 --- Application

Create the project:

mkdir -p /home/ec2-user/.alamgir/kubemind-aws-devops
cd /home/ec2-user/.alamgir/kubemind-aws-devops

mkdir -p app/src app/tests terraform .github/workflows

app/src/app.py

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 KubeMind AI is running!"

@app.route("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

app/requirements.txt

Flask
gunicorn

7. Phase 2 --- Docker

app/Dockerfile

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]

Build:

cd app
docker build -t kubemind-app:latest .

Run:

docker run -d \
  --name kubemind-app \
  -p 8080:8080 \
  kubemind-app:latest

Test:

curl http://localhost:8080/
curl http://localhost:8080/health

Expected:

🚀 KubeMind AI is running!

and:

{"status":"healthy"}

Clean up:

docker stop kubemind-app
docker rm kubemind-app

8. Phase 3 --- Tests

app/tests/test_app.py

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app

def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert "KubeMind AI is running" in response.get_data(as_text=True)

def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}

Run:

cd app
python3 -m pip install -r requirements.txt
python3 -m pip install pytest
pytest -v

Expected:

2 passed

9. Phase 4 --- ECR

Create the ECR repository:

aws ecr create-repository \
  --repository-name kubemind-app \
  --region ap-south-1

Get the URI:

aws ecr describe-repositories \
  --repository-names kubemind-app \
  --region ap-south-1 \
  --query 'repositories[0].repositoryUri' \
  --output text

Login:

aws ecr get-login-password --region ap-south-1 |
docker login \
  --username AWS \
  --password-stdin ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com

Build:

cd app
docker build -t kubemind-app:latest .

Tag:

docker tag \
  kubemind-app:latest \
  ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/kubemind-app:v1

Push:

docker push \
  ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/kubemind-app:v1

Verify:

aws ecr describe-images \
  --repository-name kubemind-app \
  --region ap-south-1

10. Phase 5 --- Terraform Backend

Terraform state should not be committed to Git.

The lab uses an S3 backend with encryption, versioning, and the native
Terraform S3 lockfile.

terraform/backend.tf

terraform {
  backend "s3" {
    bucket       = "kubemind-terraform-state-ACCOUNT_ID-ap-south-1"
    key          = "env/dev/terraform.tfstate"
    region       = "ap-south-1"
    encrypt      = true
    use_lockfile = true
  }
}

Initialize:

cd terraform
terraform init

Format:

terraform fmt -recursive

Validate:

terraform validate

Plan:

terraform plan

Apply:

terraform apply

Review the plan before confirming.

11. Phase 6 --- Terraform Infrastructure

The Terraform layer provisions:

VPC 10.0.0.0/16
|
+-- Public Subnet A 10.0.0.0/24
|     +-- NAT Gateway
|     +-- ALB
|
+-- Public Subnet B 10.0.1.0/24
|
+-- Private Subnet A 10.0.10.0/24
|     +-- ECS Fargate
|
+-- Private Subnet B 10.0.11.0/24
      +-- ECS Fargate

Additional resources:

Internet Gateway

Route tables

NAT gateway

ALB security group

ECS security group

Application Load Balancer

Target group on port 8080

Health check /health

ECS cluster

ECS service

ECS task definition

CloudWatch log group

ECS execution role

Security model:

Internet
   |
   | TCP 80
   v
ALB Security Group
   |
   | TCP 8080
   v
ECS Security Group
   |
   v
Fargate Tasks

The ECS security group accepts application traffic only from the ALB
security group.

12. Phase 7 --- ECS Verification

Check the cluster:

aws ecs describe-clusters \
  --clusters kubemind-dev-cluster

Check the service:

aws ecs describe-services \
  --cluster kubemind-dev-cluster \
  --services kubemind-dev-service

Expected:

Desired = 2
Running = 2
Pending = 0
Status  = ACTIVE

List tasks:

aws ecs list-tasks \
  --cluster kubemind-dev-cluster \
  --service-name kubemind-dev-service

Check target health:

aws elbv2 describe-target-health \
  --target-group-arn TARGET_GROUP_ARN

Expected:

healthy
healthy

13. Phase 8 --- GitHub Repository

Repository:

https://github.com/Alamgir00/kubemind-aws-devops

Initialize:

cd /home/ec2-user/.alamgir/kubemind-aws-devops
git init

Add remote:

git remote add origin \
https://github.com/Alamgir00/kubemind-aws-devops.git

.gitignore

# Terraform
.terraform/
*.tfstate
*.tfstate.*
crash.log
crash.*.log
*.tfplan
tfplan
.terraform.tfstate.lock.info

# Python
__pycache__/
*.py[cod]
.pytest_cache/
.venv/
venv/

# Docker
*.log

# OS
.DS_Store
Thumbs.db

Commit:

git add .
git commit -m "Add KubeMind AWS DevOps platform"

Push:

git branch -M main
git push -u origin main

14. Phase 9 --- GitHub OIDC

Why OIDC?

The deployment does not store long-lived AWS access keys in GitHub.

GitHub Actions
      |
      | OIDC JWT
      v
GitHub OIDC Provider
      |
      v
AWS STS
      |
      | AssumeRoleWithWebIdentity
      v
IAM Role
      |
      v
Temporary AWS credentials

GitHub recommends OIDC for obtaining short-lived AWS credentials instead
of storing long-lived AWS credentials as secrets.

OIDC provider

Provider URL:

https://token.actions.githubusercontent.com

Audience:

sts.amazonaws.com

Repository IDs

The lab repository returned:

{
  "owner_id": 46954227,
  "repo_id": 1364813519,
  "full_name": "Alamgir00/kubemind-aws-devops"
}

Command:

curl -s \
  https://api.github.com/repos/Alamgir00/kubemind-aws-devops |
jq '{owner_id: .owner.id, repo_id: .id, full_name: .full_name}'

Trust policy

File:

terraform/github-actions-trust-policy.json

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:Alamgir00@46954227/kubemind-aws-devops@1364813519:ref:refs/heads/main"
        }
      }
    }
  ]
}

Apply:

aws iam update-assume-role-policy \
  --role-name kubemind-github-actions-role \
  --policy-document file://terraform/github-actions-trust-policy.json

Verify:

aws iam get-role \
  --role-name kubemind-github-actions-role \
  --query 'Role.AssumeRolePolicyDocument' \
  --output json

The trust policy is deliberately restricted to the repository and main
branch.

15. Phase 10 --- GitHub Actions

File:

.github/workflows/deploy.yml

name: KubeMind AI CI/CD

on:
  push:
    branches:
      - main

permissions:
  id-token: write
  contents: read

env:
  AWS_REGION: ap-south-1
  ECR_REPOSITORY: kubemind-app
  ECS_CLUSTER: kubemind-dev-cluster
  ECS_SERVICE: kubemind-dev-service
  CONTAINER_NAME: kubemind-app

jobs:
  deploy:
    name: Test, Build and Deploy
    runs-on: ubuntu-latest

    steps:
      - name: Checkout source
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        working-directory: app
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest

      - name: Run tests
        working-directory: app
        run: |
          pytest -v

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v5
        with:
          role-to-assume: arn:aws:iam::ACCOUNT_ID:role/kubemind-github-actions-role
          aws-region: ${{ env.AWS_REGION }}

      - name: Verify AWS identity
        run: |
          aws sts get-caller-identity

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build Docker image
        working-directory: app
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build \
            -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG \
            .

      - name: Push Docker image
        working-directory: app
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker push \
            $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG

      - name: Download current task definition
        run: |
          aws ecs describe-task-definition \
            --task-definition kubemind-dev-app \
            --query taskDefinition \
            --output json > task-definition.json

      - name: Clean task definition
        run: |
          python3 - <<'PY'
          import json

          with open("task-definition.json") as f:
              data = json.load(f)

          for key in [
              "taskDefinitionArn",
              "revision",
              "status",
              "requiresAttributes",
              "compatibilities",
              "registeredAt",
              "registeredBy"
          ]:
              data.pop(key, None)

          with open("task-definition.json", "w") as f:
              json.dump(data, f)
          PY

      - name: Render new task definition
        id: task-def
        uses: aws-actions/amazon-ecs-render-task-definition@v1
        with:
          task-definition: task-definition.json
          container-name: ${{ env.CONTAINER_NAME }}
          image: ${{ steps.login-ecr.outputs.registry }}/${{ env.ECR_REPOSITORY }}:${{ github.sha }}

      - name: Deploy to Amazon ECS
        uses: aws-actions/amazon-ecs-deploy-task-definition@v2
        with:
          task-definition: ${{ steps.task-def.outputs.task-definition }}
          service: ${{ env.ECS_SERVICE }}
          cluster: ${{ env.ECS_CLUSTER }}
          wait-for-service-stability: true

Pipeline stages

Checkout
   ↓
Python setup
   ↓
Install dependencies
   ↓
pytest
   ↓
OIDC → AWS IAM
   ↓
Verify identity
   ↓
ECR login
   ↓
Docker build
   ↓
Docker push
   ↓
Download ECS task definition
   ↓
Render new image
   ↓
Deploy ECS
   ↓
Wait for stability

The Docker image is tagged with:

${{ github.sha }}

This gives traceability:

Git Commit
    ↕
Docker Image
    ↕
ECS Task Definition

16. Phase 11 --- End-to-End Verification

Get the ALB DNS:

cd /home/ec2-user/.alamgir/kubemind-aws-devops/terraform

terraform output -raw alb_dns_name

Test application:

curl http://$(terraform output -raw alb_dns_name)/

Expected:

🚀 KubeMind AI is running!

Test health:

curl http://$(terraform output -raw alb_dns_name)/health

Expected:

{"status":"healthy"}

Verify ECS:

aws ecs describe-services \
  --cluster kubemind-dev-cluster \
  --services kubemind-dev-service \
  --query 'services[0].{Desired:desiredCount,Running:runningCount,Pending:pendingCount,Status:status,TaskDefinition:taskDefinition}' \
  --output table

Expected:

Desired   Pending   Running   Status
2         0         2         ACTIVE

A successful CI/CD deployment produced:

kubemind-dev-app:2

meaning the ECS task definition advanced from the initial revision.

17. IAM Security Model

There are two important roles.

ECS execution role

kubemind-dev-ecs-task-execution-role

Used by ECS to:

pull private images from ECR

write application logs to CloudWatch

GitHub Actions deployment role

kubemind-github-actions-role

Used by GitHub Actions to:

assume AWS through OIDC

push images to ECR

read ECS task definitions

register new task definitions

update ECS services

describe ECS resources

pass the ECS execution role

The deployment role is not a full Terraform administrator role.

Keep infrastructure provisioning permissions separate from application
deployment permissions.

18. Troubleshooting

OIDC error

Error:

Could not assume role with OIDC:
Not authorized to perform sts:AssumeRoleWithWebIdentity

Check:

aws iam get-role \
  --role-name kubemind-github-actions-role \
  --query 'Role.AssumeRolePolicyDocument'

Verify:

aud = sts.amazonaws.com

and:

repo:Alamgir00@46954227/kubemind-aws-devops@1364813519:ref:refs/heads/main

ECR AccessDenied

Inspect the deployment role policy:

aws iam get-role-policy \
  --role-name kubemind-github-actions-role \
  --policy-name KubeMindGitHubActionsDeploymentPolicy

Required ECR actions include:

ecr:GetAuthorizationToken
ecr:BatchCheckLayerAvailability
ecr:CompleteLayerUpload
ecr:InitiateLayerUpload
ecr:PutImage
ecr:UploadLayerPart
ecr:BatchGetImage
ecr:GetDownloadUrlForLayer

ECS deployment failure

aws ecs describe-services \
  --cluster kubemind-dev-cluster \
  --services kubemind-dev-service

List tasks:

aws ecs list-tasks \
  --cluster kubemind-dev-cluster \
  --service-name kubemind-dev-service

Describe a task:

aws ecs describe-tasks \
  --cluster kubemind-dev-cluster \
  --tasks TASK_ARN

Stopped ECS task

aws ecs describe-tasks \
  --cluster kubemind-dev-cluster \
  --tasks TASK_ARN \
  --query 'tasks[0].{StopCode:stopCode,StoppedReason:stoppedReason}'

Container details:

aws ecs describe-tasks \
  --cluster kubemind-dev-cluster \
  --tasks TASK_ARN \
  --query 'tasks[0].containers[].{Name:name,Reason:reason,ExitCode:exitCode}'

ALB returns 503

Check:

aws elbv2 describe-target-health \
  --target-group-arn TARGET_GROUP_ARN

Expected:

healthy
healthy

Verify:

ALB listener = 80
Target = 8080
Health path = /health
Container = 8080

Terraform output is empty

Run Terraform commands from:

/home/ec2-user/.alamgir/kubemind-aws-devops/terraform

Correct:

cd /home/ec2-user/.alamgir/kubemind-aws-devops/terraform
terraform output -raw alb_dns_name

19. Useful Commands

AWS

aws sts get-caller-identity

aws ecr describe-repositories \
  --region ap-south-1

aws ecr describe-images \
  --repository-name kubemind-app \
  --region ap-south-1

aws ecs list-clusters

aws ecs describe-services \
  --cluster kubemind-dev-cluster \
  --services kubemind-dev-service

aws ecs list-tasks \
  --cluster kubemind-dev-cluster \
  --service-name kubemind-dev-service

aws ecs describe-task-definition \
  --task-definition kubemind-dev-app

Terraform

terraform init
terraform fmt -recursive
terraform validate
terraform plan
terraform apply
terraform output
terraform output -raw alb_dns_name
terraform state list
terraform state show RESOURCE
terraform destroy

Git

git status
git log --oneline --graph --decorate --all
git add .
git commit -m "Update application"
git push origin main
git pull origin main
git remote -v

20. Production Hardening Roadmap

The core deployment is working. The next production-grade improvements
are:

20.1 Separate CI and CD

Pull Request
   |
   v
CI
├── Lint
├── Unit tests
├── Security scans
└── Docker build test

main
 |
 v
CD
├── Build
├── Push ECR
├── Deploy ECS
└── Verify

20.2 Terraform CI/CD

Use separate OIDC roles:

GitHub Terraform Plan Role
GitHub Terraform Apply Role
GitHub Application Deployment Role

Pipeline:

PR
 |
 +--> terraform fmt -check
 +--> terraform validate
 +--> terraform plan
 |
 v
Approval
 |
 v
terraform apply

20.3 Security

Add:

Trivy
CodeQL
Dependabot
Secret scanning
IaC scanning
Container vulnerability scanning

20.4 Deployment strategies

Current:

Rolling deployment

Future:

Blue/Green
Canary
Progressive delivery
Automatic rollback

20.5 Observability

Add:

CloudWatch
├── Logs
├── Metrics
└── Alarms

ALB
├── 4xx
├── 5xx
└── Latency

ECS
├── CPU
├── Memory
└── Running task count

20.6 Secrets

Do not put credentials in:

Git
Dockerfile
Terraform source
README
Workflow YAML

Use:

AWS Secrets Manager
AWS Systems Manager Parameter Store
GitHub encrypted secrets

21. Lessons Learned

Terraform

Terraform manages the infrastructure lifecycle:

Terraform
   |
   +--> VPC
   +--> Networking
   +--> ALB
   +--> IAM
   +--> ECS
   +--> CloudWatch

Docker

Docker packages:

Application
+
Dependencies
+
Runtime
=
Container Image

ECR

Docker Build
     |
     v
Docker Image
     |
     v
Amazon ECR

ECS

ECR Image
    |
    v
Task Definition
    |
    v
Fargate Task

ALB

Internet
   |
   v
ALB
   |
   v
Target Group
   |
   v
ECS Tasks

OIDC

GitHub
  |
  | short-lived token
  v
AWS STS
  |
  v
Temporary credentials

No long-lived AWS access key is required for the GitHub deployment
workflow.

Immutable image tagging

Instead of:

latest

the workflow uses:

github.sha

so a deployment can be traced back to the exact Git commit.

22. Final Checklist

[✓] GitHub repository
[✓] Flask application
[✓] /health endpoint
[✓] Unit tests
[✓] Docker image
[✓] Local container test
[✓] ECR repository
[✓] Initial ECR image
[✓] Terraform S3 backend
[✓] Terraform initialization
[✓] VPC
[✓] Public subnets
[✓] Private subnets
[✓] NAT Gateway
[✓] Internet Gateway
[✓] ALB
[✓] Target Group
[✓] Security Groups
[✓] ECS Cluster
[✓] ECS Service
[✓] Fargate tasks
[✓] CloudWatch logs
[✓] ECS execution role
[✓] GitHub OIDC provider
[✓] GitHub Actions IAM role
[✓] Restricted OIDC trust policy
[✓] OIDC authentication
[✓] ECR login
[✓] Docker build
[✓] Docker push
[✓] ECS task definition update
[✓] ECS deployment
[✓] ECS stability
[✓] 2/2 tasks running
[✓] ALB endpoint
[✓] /health endpoint

🏁 Final Result

                    KUBEMIND AI
                 AWS DEVOPS LAB

Developer
    |
    | git push
    v
GitHub
    |
    v
GitHub Actions
    |
    +---- pytest ------------------+
    |                              |
    +---- OIDC ----------------+   |
    |                          |   |
    v                          v   |
AWS STS / IAM              ECR <---+
    |                          |
    |                          | Docker image
    |                          v
    |                       ECS
    |                          |
    |                     Fargate x2
    |                          |
    +--------------------------+
                               |
                               v
                              ALB
                               |
                               v
                      🚀 KubeMind AI

End-to-end CI/CD status: SUCCESSFUL

The completed lab demonstrates GitHub Actions → OIDC → AWS IAM → ECR →
ECS Fargate → ALB with Terraform-managed infrastructure.

Official References

GitHub README:
https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes

GitHub OIDC + AWS:
https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws

AWS OIDC federation:
https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_oidc.html

GitHub ECS deployment:
https://docs.github.com/en/actions/how-tos/deploy/deploy-to-third-party-platforms/amazon-elastic-container-service

AWS ECR with ECS:
https://docs.aws.amazon.com/AmazonECR/latest/userguide/ECR_on_ECS.html

Author: SK Alamgir Ali
Project: KubeMind AI --- AWS DevOps & Cloud Architecture
Track: Terraform + Docker + AWS + GitHub Actions + ECS Fargate
Status: End-to-End CI/CD Successfully Deployed 🚀
