
````markdown
# 🚀 KubeMind AI — Production-Grade AWS DevOps CI/CD

<p align="center">

<b>End-to-End AWS DevOps Hands-On Project</b>

</p>

<p align="center">

GitHub → GitHub Actions → OIDC → AWS IAM → ECR → ECS Fargate → ALB → Flask

</p>

---

## 📌 Project Overview

**KubeMind AI** is an end-to-end AWS DevOps and Cloud Engineering hands-on project.

The project demonstrates how to take a Python Flask application from source code to a production-style containerized deployment on AWS.

The complete platform uses:

- Python
- Flask
- Gunicorn
- Pytest
- Docker
- Terraform
- Amazon VPC
- Amazon ECR
- Amazon ECS
- AWS Fargate
- Application Load Balancer
- Amazon CloudWatch
- AWS IAM
- GitHub
- GitHub Actions
- GitHub OIDC

The final deployment follows this flow:

```text
Developer
    |
    | git push
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    +-----------------------+
    |                       |
    v                       v
Run Tests              GitHub OIDC
                            |
                            v
                        AWS STS
                            |
                            v
                     AWS IAM Role
                            |
                +-----------+-----------+
                |                       |
                v                       v
               ECR                    ECS
                |                       |
                |                 Task Definition
                |                       |
                v                       v
          Docker Image             Fargate Tasks
                                        |
                                        v
                                       ALB
                                        |
                                        v
                                KubeMind AI
````

---

# 🎯 Project Objectives

The main objectives of this project are:

1. Build a Python Flask application.
2. Write automated unit tests.
3. Containerize the application using Docker.
4. Store Docker images in Amazon ECR.
5. Create AWS infrastructure using Terraform.
6. Build a secure VPC architecture.
7. Deploy the application to ECS Fargate.
8. Expose the application through an Application Load Balancer.
9. Configure CloudWatch logging.
10. Configure GitHub OIDC authentication.
11. Remove the need for long-lived AWS credentials in GitHub.
12. Build a GitHub Actions CI/CD pipeline.
13. Automatically test, build, push, and deploy the application.
14. Use Git commit SHA as an immutable Docker image tag.
15. Verify the deployment through the ALB.

---

# 🏗️ Final Architecture

## AWS Runtime Architecture

```text
                         INTERNET
                            |
                            |
                         HTTP :80
                            |
                            v
                 +-----------------------+
                 | Application Load      |
                 | Balancer              |
                 |                       |
                 | kubemind-dev-alb      |
                 +-----------+-----------+
                             |
                             |
                         HTTP :8080
                             |
                             v
                 +-----------------------+
                 | Target Group          |
                 | kubemind-dev-tg       |
                 +-----------+-----------+
                             |
                +------------+------------+
                |                         |
                v                         v
       +------------------+       +------------------+
       | ECS Fargate      |       | ECS Fargate      |
       | Task 1           |       | Task 2           |
       |                  |       |                  |
       | Private Subnet A |       | Private Subnet B |
       | Port 8080        |       | Port 8080        |
       +------------------+       +------------------+
                |                         |
                +------------+------------+
                             |
                             v
                     Docker Container
                             |
                             v
                       Flask + Gunicorn
```

---

# 🔄 CI/CD Architecture

```text
                       DEVELOPER
                           |
                           |
                     git push main
                           |
                           v
                  +----------------+
                  |    GitHub      |
                  |   Repository   |
                  +-------+--------+
                          |
                          v
                 +-------------------+
                 |  GitHub Actions   |
                 +---------+---------+
                           |
             +-------------+-------------+
             |                           |
             v                           v
        Python Tests                GitHub OIDC
             |                           |
             |                           v
             |                       AWS STS
             |                           |
             |                           v
             |                    AWS IAM Role
             |                           |
             |                 +---------+---------+
             |                 |                   |
             |                 v                   v
             |                ECR                 ECS
             |                 |                   |
             |                 |            Task Definition
             |                 |                   |
             |                 +-------------------+
             |                                     |
             |                                     v
             |                              Fargate Tasks
             |                                     |
             +-------------------------------------+
                                                   |
                                                   v
                                                  ALB
                                                   |
                                                   v
                                            KubeMind AI
```

---

# 🧰 Technology Stack

| Layer              | Technology                | Purpose                      |
| ------------------ | ------------------------- | ---------------------------- |
| Application        | Python 3.12 + Flask       | Web application              |
| Application Server | Gunicorn                  | Production WSGI server       |
| Testing            | Pytest                    | Automated testing            |
| Container          | Docker                    | Application containerization |
| Infrastructure     | Terraform                 | Infrastructure as Code       |
| Cloud              | AWS                       | Cloud platform               |
| Registry           | Amazon ECR                | Docker image storage         |
| Compute            | Amazon ECS Fargate        | Serverless container runtime |
| Load Balancer      | Application Load Balancer | HTTP traffic routing         |
| Networking         | Amazon VPC                | Network isolation            |
| Logging            | Amazon CloudWatch         | Application/container logs   |
| Authentication     | GitHub OIDC               | Keyless AWS authentication   |
| IAM                | AWS IAM                   | Access control               |
| CI/CD              | GitHub Actions            | Automated deployment         |
| State              | Amazon S3                 | Terraform remote state       |
| Source Control     | GitHub                    | Source code management       |

---

# 📁 Repository Structure

```text
kubemind-aws-devops/
│
├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   │
│   ├── src/
│   │   └── app.py
│   │
│   └── tests/
│       └── test_app.py
│
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
│
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── .gitignore
└── README.md
```

---

# ☁️ AWS Environment

## AWS Region

```text
ap-south-1
```

AWS Region:

```text
Mumbai
```

---

## VPC

```text
CIDR: 10.0.0.0/16
```

---

## Public Subnets

```text
Public Subnet A
10.0.0.0/24

Public Subnet B
10.0.1.0/24
```

---

## Private Subnets

```text
Private Subnet A
10.0.10.0/24

Private Subnet B
10.0.11.0/24
```

---

## Application

```text
kubemind-app
```

---

## ECR Repository

```text
kubemind-app
```

---

## ECS Cluster

```text
kubemind-dev-cluster
```

---

## ECS Service

```text
kubemind-dev-service
```

---

## ECS Task Definition

```text
kubemind-dev-app
```

---

## CloudWatch Log Group

```text
/ecs/kubemind-dev
```

---

# 🛠️ Prerequisites

Install the following tools:

* Git
* Docker
* Python 3.12
* Terraform
* AWS CLI
* GitHub account
* AWS account

Verify the installations:

```bash
git --version
docker --version
python3 --version
terraform version
aws --version
```

---

# 🔐 AWS Authentication

Verify AWS identity:

```bash
aws sts get-caller-identity
```

Example:

```json
{
    "UserId": "...",
    "Account": "...",
    "Arn": "..."
}
```

Set AWS region:

```bash
export AWS_DEFAULT_REGION=ap-south-1
```

Optional:

```bash
aws configure set region ap-south-1
```

---

# 🚀 Phase 1 — Create the Project

Create the project:

```bash
mkdir -p /home/ec2-user/.alamgir/kubemind-aws-devops
```

Move into the project:

```bash
cd /home/ec2-user/.alamgir/kubemind-aws-devops
```

Create directories:

```bash
mkdir -p app/src
mkdir -p app/tests
mkdir -p terraform
mkdir -p .github/workflows
```

Verify:

```bash
find . -maxdepth 3 -type f
```

---

# 🐍 Phase 2 — Create Flask Application

Create:

```text
app/src/app.py
```

Content:

```python
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
```

---

# 📦 Phase 3 — Python Dependencies

Create:

```text
app/requirements.txt
```

Content:

```text
Flask
gunicorn
```

---

# 🧪 Phase 4 — Automated Tests

Create:

```text
app/tests/test_app.py
```

Content:

```python
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from app import app


def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert "KubeMind AI is running" in response.get_data(
        as_text=True
    )


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "healthy"
    }
```

---

# 📥 Install Python Dependencies

```bash
cd /home/ec2-user/.alamgir/kubemind-aws-devops/app
```

Install:

```bash
python3 -m pip install -r requirements.txt
```

Install pytest:

```bash
python3 -m pip install pytest
```

---

# ✅ Run Tests

```bash
pytest -v
```

Expected:

```text
============================= test session starts =============================

collected 2 items

tests/test_app.py::test_home PASSED
tests/test_app.py::test_health PASSED

============================== 2 passed ==============================
```

---

# 🐳 Phase 5 — Dockerize Application

Create:

```text
app/Dockerfile
```

Content:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
```

---

# 🏗️ Build Docker Image

Move into the application directory:

```bash
cd /home/ec2-user/.alamgir/kubemind-aws-devops/app
```

Build:

```bash
docker build -t kubemind-app:latest .
```

Verify:

```bash
docker images
```

Expected:

```text
kubemind-app
```

---

# ▶️ Run Docker Container

```bash
docker run -d \
  --name kubemind-app \
  -p 8080:8080 \
  kubemind-app:latest
```

Verify:

```bash
docker ps
```

---

# 🧪 Test Docker Container

Test application:

```bash
curl http://localhost:8080/
```

Expected:

```text
🚀 KubeMind AI is running!
```

Test health:

```bash
curl http://localhost:8080/health
```

Expected:

```json
{
  "status": "healthy"
}
```

Stop:

```bash
docker stop kubemind-app
```

Remove:

```bash
docker rm kubemind-app
```

---

# 📦 Phase 6 — Amazon ECR

Create the ECR repository:

```bash
aws ecr create-repository \
  --repository-name kubemind-app \
  --region ap-south-1
```

If the repository already exists, AWS will report that it exists. In that case, continue.

---

# 🔎 Get ECR Repository URI

```bash
aws ecr describe-repositories \
  --repository-names kubemind-app \
  --region ap-south-1 \
  --query 'repositories[0].repositoryUri' \
  --output text
```

Expected format:

```text
ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/kubemind-app
```

---

# 🔐 Login to Amazon ECR

Set your AWS account ID dynamically:

```bash
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity \
  --query Account \
  --output text)
```

Login:

```bash
aws ecr get-login-password \
  --region ap-south-1 |
docker login \
  --username AWS \
  --password-stdin \
  ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com
```

Expected:

```text
Login Succeeded
```

---

# 🏷️ Tag Docker Image

```bash
docker tag \
  kubemind-app:latest \
  ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com/kubemind-app:v1
```

Verify:

```bash
docker images
```

---

# ⬆️ Push Docker Image

```bash
docker push \
  ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com/kubemind-app:v1
```

Verify:

```bash
aws ecr describe-images \
  --repository-name kubemind-app \
  --region ap-south-1
```

---

# 🏗️ Phase 7 — Terraform Infrastructure

Terraform manages the AWS infrastructure.

The infrastructure includes:

```text
VPC
│
├── Internet Gateway
│
├── Public Subnet A
│   ├── NAT Gateway
│   └── Application Load Balancer
│
├── Public Subnet B
│
├── Private Subnet A
│   └── ECS Fargate Task
│
├── Private Subnet B
│   └── ECS Fargate Task
│
├── Route Tables
│
├── Security Groups
│
├── Target Group
│
├── ECS Cluster
│
├── ECS Service
│
├── Task Definition
│
├── IAM Roles
│
└── CloudWatch Logs
```

---

# 💾 Phase 8 — Terraform Remote State

Terraform state is stored in Amazon S3.

Example:

```text
kubemind-terraform-state-ACCOUNT_ID-ap-south-1
```

Terraform backend:

```hcl
terraform {
  backend "s3" {
    bucket       = "kubemind-terraform-state-ACCOUNT_ID-ap-south-1"
    key          = "env/dev/terraform.tfstate"
    region       = "ap-south-1"
    encrypt      = true
    use_lockfile = true
  }
}
```

The state should never be committed to Git.

---

# 🔒 Terraform State Security

The `.gitignore` should include:

```gitignore
.terraform/
*.tfstate
*.tfstate.*
*.tfplan
tfplan
.terraform.tfstate.lock.info
```

The Terraform dependency lock file should remain tracked:

```text
.terraform.lock.hcl
```

---

# ⚙️ Phase 9 — Terraform Initialization

Move into Terraform:

```bash
cd /home/ec2-user/.alamgir/kubemind-aws-devops/terraform
```

Initialize:

```bash
terraform init
```

Expected:

```text
Terraform has been successfully initialized!
```

---

# 🧹 Format Terraform

```bash
terraform fmt -recursive
```

---

# ✅ Validate Terraform

```bash
terraform validate
```

Expected:

```text
Success! The configuration is valid.
```

---

# 📋 Terraform Plan

```bash
terraform plan
```

Review all resources before applying.

---

# 🚀 Terraform Apply

```bash
terraform apply
```

Review the plan.

Enter:

```text
yes
```

when ready.

---

# 🌐 Network Architecture

The project uses:

```text
VPC
10.0.0.0/16
```

Public subnets:

```text
10.0.0.0/24
10.0.1.0/24
```

Private subnets:

```text
10.0.10.0/24
10.0.11.0/24
```

Architecture:

```text
                         INTERNET
                            |
                            v
                    Internet Gateway
                            |
                +-----------+-----------+
                |                       |
                v                       v
        Public Subnet A         Public Subnet B
                |
                |
          +-----+------+
          |            |
          v            v
      NAT Gateway     ALB
                         |
                         |
                    Target Group
                         |
              +----------+----------+
              |                     |
              v                     v
       Private Subnet A      Private Subnet B
              |                     |
              v                     v
       ECS Fargate Task      ECS Fargate Task
```

---

# 🔐 Security Group Architecture

## ALB Security Group

Inbound:

```text
TCP 80
Source: 0.0.0.0/0
```

## ECS Security Group

Inbound:

```text
TCP 8080
Source: ALB Security Group
```

Therefore:

```text
Internet
    |
    | TCP 80
    v
   ALB
    |
    | TCP 8080
    v
   ECS
```

The ECS tasks are not directly exposed to the internet.

---

# 🚢 Phase 10 — Amazon ECS Fargate

ECS Cluster:

```text
kubemind-dev-cluster
```

ECS Service:

```text
kubemind-dev-service
```

Task Definition:

```text
kubemind-dev-app
```

Desired count:

```text
2
```

Architecture:

```text
                 ECS Service
                     |
            +--------+--------+
            |                 |
            v                 v
       Fargate Task 1    Fargate Task 2
       Private AZ-A      Private AZ-B
```

Running two tasks provides basic availability across two Availability Zones.

---

# 🩺 ECS Health Check

Target Group:

```text
Port:
8080

Protocol:
HTTP

Health Check:
 /health

Success Matcher:
200
```

Application response:

```json
{
  "status": "healthy"
}
```

Expected:

```text
Target 1 → healthy
Target 2 → healthy
```

---

# 📊 CloudWatch Logs

CloudWatch log group:

```text
/ecs/kubemind-dev
```

ECS sends container logs to CloudWatch.

Check:

```bash
aws logs describe-log-groups \
  --log-group-name-prefix /ecs/kubemind-dev
```

---

# 🐙 Phase 11 — GitHub Repository

Repository:

```text
Alamgir00/kubemind-aws-devops
```

Initialize Git:

```bash
cd /home/ec2-user/.alamgir/kubemind-aws-devops

git init
```

Add remote:

```bash
git remote add origin \
https://github.com/Alamgir00/kubemind-aws-devops.git
```

Check:

```bash
git remote -v
```

---

# 🚫 `.gitignore`

Create:

```text
.gitignore
```

Content:

```gitignore
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
```

---

# 📤 Push Project to GitHub

Check:

```bash
git status
```

Add:

```bash
git add .
```

Commit:

```bash
git commit -m "Add KubeMind AWS DevOps platform"
```

Set main:

```bash
git branch -M main
```

Push:

```bash
git push -u origin main
```

---

# 🔐 Phase 12 — GitHub OIDC

## Why OIDC?

A traditional GitHub deployment may use AWS access keys:

```text
GitHub Actions
      |
      | AWS Access Key
      v
     AWS
```

This requires storing long-lived credentials.

KubeMind uses OIDC instead:

```text
GitHub Actions
      |
      | OIDC Token
      v
GitHub OIDC Provider
      |
      v
AWS STS
      |
      | AssumeRoleWithWebIdentity
      v
AWS IAM Role
      |
      v
Temporary AWS Credentials
```

Advantages:

* No long-lived AWS access keys
* Short-lived credentials
* Repository-specific trust
* Branch-specific trust
* Reduced credential management
* Better security posture

---

# 🆔 GitHub Repository IDs

For the KubeMind repository:

```text
Owner ID:
46954227

Repository ID:
1364813519
```

Retrieve them:

```bash
curl -s \
  https://api.github.com/repos/Alamgir00/kubemind-aws-devops |
jq '{owner_id: .owner.id, repo_id: .id, full_name: .full_name}'
```

Expected:

```json
{
  "owner_id": 46954227,
  "repo_id": 1364813519,
  "full_name": "Alamgir00/kubemind-aws-devops"
}
```

---

# 🔑 GitHub OIDC Trust Policy

File:

```text
terraform/github-actions-trust-policy.json
```

Content:

```json
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
```

Replace:

```text
ACCOUNT_ID
```

with your AWS account ID.

You can retrieve it:

```bash
aws sts get-caller-identity \
  --query Account \
  --output text
```

---

# 🔄 Apply OIDC Trust Policy

```bash
aws iam update-assume-role-policy \
  --role-name kubemind-github-actions-role \
  --policy-document file://terraform/github-actions-trust-policy.json
```

Expected:

```text
No output
```

No output means the command completed successfully.

---

# 🔎 Verify OIDC Trust Policy

```bash
aws iam get-role \
  --role-name kubemind-github-actions-role \
  --query 'Role.AssumeRolePolicyDocument' \
  --output json
```

Verify that the policy contains:

```text
sts.amazonaws.com
```

and:

```text
repo:Alamgir00@46954227/kubemind-aws-devops@1364813519:ref:refs/heads/main
```

---

# 🛡️ GitHub Actions IAM Permissions

The GitHub Actions deployment role requires permissions for ECR and ECS.

## ECR

```text
ecr:GetAuthorizationToken

ecr:BatchCheckLayerAvailability
ecr:CompleteLayerUpload
ecr:InitiateLayerUpload
ecr:PutImage
ecr:UploadLayerPart

ecr:BatchGetImage
ecr:GetDownloadUrlForLayer
```

## ECS

```text
ecs:DescribeServices
ecs:DescribeTaskDefinition
ecs:DescribeTasks
ecs:ListTasks
ecs:RegisterTaskDefinition
ecs:UpdateService
```

## IAM

```text
iam:PassRole
```

The `iam:PassRole` permission should be restricted to the ECS execution role.

---

# 🔐 IAM Role Separation

There are two major roles.

## ECS Execution Role

```text
kubemind-dev-ecs-task-execution-role
```

Used by ECS to:

```text
Pull image from ECR
        +
Write logs to CloudWatch
```

---

## GitHub Actions Deployment Role

```text
kubemind-github-actions-role
```

Used by GitHub Actions to:

```text
Authenticate through OIDC
        +
Push Docker image to ECR
        +
Read ECS task definition
        +
Register ECS task definition
        +
Update ECS service
```

The GitHub Actions deployment role is not a full Terraform administrator role.

---

# 🔄 Phase 13 — GitHub Actions CI/CD

Workflow file:

```text
.github/workflows/deploy.yml
```

Complete workflow:

```yaml
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
```

Replace:

```text
ACCOUNT_ID
```

with your AWS account ID.

---

# 🔄 CI/CD Pipeline Flow

```text
1. Developer
      |
      | git push
      v
2. GitHub
      |
      v
3. GitHub Actions
      |
      v
4. Checkout source
      |
      v
5. Setup Python
      |
      v
6. Install dependencies
      |
      v
7. Run pytest
      |
      +------ FAIL ------> STOP
      |
      v
8. GitHub OIDC
      |
      v
9. AWS STS
      |
      v
10. IAM Deployment Role
      |
      v
11. Verify AWS identity
      |
      v
12. ECR Login
      |
      v
13. Docker Build
      |
      v
14. Docker Push
      |
      v
15. Download ECS Task Definition
      |
      v
16. Render new image
      |
      v
17. Register new Task Definition
      |
      v
18. Update ECS Service
      |
      v
19. Wait for Stability
      |
      v
20. Fargate Tasks
      |
      v
21. ALB
      |
      v
22. KubeMind AI LIVE
```

---

# 🏷️ Immutable Docker Image Tagging

The pipeline does not deploy using:

```text
latest
```

Instead it uses:

```yaml
IMAGE_TAG: ${{ github.sha }}
```

Example:

```text
kubemind-app:a83f72c...
```

This creates traceability:

```text
Git Commit
     |
     v
GitHub Actions
     |
     v
Docker Image
     |
     v
Amazon ECR
     |
     v
ECS Task Definition
     |
     v
Running Container
```

This allows you to identify exactly which Git commit is running.

---

# 🔍 Phase 14 — GitHub Actions Verification

Open the GitHub Actions page for the repository.

The workflow should show:

```text
Test, Build and Deploy
```

Expected stages:

```text
Checkout source                 ✅
Setup Python                    ✅
Install dependencies            ✅
Run tests                       ✅
Configure AWS credentials       ✅
Verify AWS identity             ✅
Login to Amazon ECR             ✅
Build Docker image              ✅
Push Docker image               ✅
Download task definition        ✅
Clean task definition           ✅
Render new task definition      ✅
Deploy to Amazon ECS            ✅
```

---

# 🔐 Verify OIDC Authentication

The `Configure AWS credentials` step should contain something similar to:

```text
Assuming role with OIDC

Authenticated as assumedRoleId
```

The following step:

```text
Verify AWS identity
```

should return an ARN similar to:

```text
arn:aws:sts::ACCOUNT_ID:assumed-role/kubemind-github-actions-role/...
```

This proves GitHub Actions successfully assumed the AWS IAM role using OIDC.

---

# 🌐 Phase 15 — ALB Verification

Move into Terraform:

```bash
cd /home/ec2-user/.alamgir/kubemind-aws-devops/terraform
```

Get ALB DNS:

```bash
terraform output -raw alb_dns_name
```

Example:

```text
kubemind-dev-alb-xxxxxxxxxx.ap-south-1.elb.amazonaws.com
```

---

# 🧪 Test Application Through ALB

```bash
curl http://$(terraform output -raw alb_dns_name)/
```

Expected:

```text
🚀 KubeMind AI is running!
```

---

# ❤️ Test Health Endpoint

```bash
curl http://$(terraform output -raw alb_dns_name)/health
```

Expected:

```json
{
  "status": "healthy"
}
```

---

# 🚢 Verify ECS Service

Run:

```bash
aws ecs describe-services \
  --cluster kubemind-dev-cluster \
  --services kubemind-dev-service \
  --query 'services[0].{Desired:desiredCount,Running:runningCount,Pending:pendingCount,Status:status,TaskDefinition:taskDefinition}' \
  --output table
```

Expected:

```text
---------------------------------------------------------------
|                    DescribeServices                         |
+----------+---------+---------+--------+---------------------+
| Desired  | Pending | Running | Status | TaskDefinition      |
+----------+---------+---------+--------+---------------------+
| 2        | 0       | 2       | ACTIVE | ...:kubemind-dev-app|
+----------+---------+---------+--------+---------------------+
```

---

# 📋 List ECS Tasks

```bash
aws ecs list-tasks \
  --cluster kubemind-dev-cluster \
  --service-name kubemind-dev-service
```

Expected:

```text
2 running tasks
```

---

# ❤️ Check Target Health

```bash
aws elbv2 describe-target-health \
  --target-group-arn TARGET_GROUP_ARN
```

Expected:

```text
healthy
healthy
```

---

# 📈 ECS Task Definition Revisions

Initial deployment:

```text
kubemind-dev-app:1
```

After GitHub Actions:

```text
kubemind-dev-app:2
```

Future deployments:

```text
kubemind-dev-app:3
kubemind-dev-app:4
kubemind-dev-app:5
...
```

Each ECS task definition revision represents a deployment configuration.

---

# 🧪 Phase 16 — Perform a Complete Deployment Test

Modify the application:

```bash
cd /home/ec2-user/.alamgir/kubemind-aws-devops

nano app/src/app.py
```

Change:

```python
@app.route("/")
def home():
    return "🚀 KubeMind AI is running!"
```

to:

```python
@app.route("/")
def home():
    return "🚀 KubeMind AI v2 is running!"
```

---

# 🧪 Run Tests

```bash
cd app
pytest -v
```

Expected:

```text
2 passed
```

Return to root:

```bash
cd ..
```

---

# 📤 Commit the Change

```bash
git add .
```

Commit:

```bash
git commit -m "Update KubeMind application"
```

Push:

```bash
git push origin main
```

---

# 🔄 What Happens Automatically?

```text
git push
   |
   v
GitHub Actions
   |
   v
Run Tests
   |
   v
OIDC Authentication
   |
   v
AWS IAM
   |
   v
ECR Login
   |
   v
Docker Build
   |
   v
Docker Push
   |
   v
New ECS Task Definition
   |
   v
ECS Deployment
   |
   v
Fargate
   |
   v
ALB
   |
   v
New Application Version
```

---

# 🛠️ Troubleshooting

# 1. OIDC AssumeRole Error

Error:

```text
Could not assume role with OIDC:
Not authorized to perform sts:AssumeRoleWithWebIdentity
```

Check:

```bash
aws iam get-role \
  --role-name kubemind-github-actions-role \
  --query 'Role.AssumeRolePolicyDocument' \
  --output json
```

Verify audience:

```text
sts.amazonaws.com
```

Verify subject:

```text
repo:Alamgir00@46954227/kubemind-aws-devops@1364813519:ref:refs/heads/main
```

Make sure:

* Repository name is correct.
* Owner is correct.
* Owner ID is correct.
* Repository ID is correct.
* Branch is `main`.
* OIDC provider exists.
* IAM role trust policy is updated.

---

# 2. ECR AccessDenied

Inspect IAM policy:

```bash
aws iam get-role-policy \
  --role-name kubemind-github-actions-role \
  --policy-name KubeMindGitHubActionsDeploymentPolicy
```

Verify ECR permissions:

```text
ecr:GetAuthorizationToken
ecr:BatchCheckLayerAvailability
ecr:CompleteLayerUpload
ecr:InitiateLayerUpload
ecr:PutImage
ecr:UploadLayerPart
ecr:BatchGetImage
ecr:GetDownloadUrlForLayer
```

---

# 3. ECS Deployment Failure

Check service:

```bash
aws ecs describe-services \
  --cluster kubemind-dev-cluster \
  --services kubemind-dev-service
```

List tasks:

```bash
aws ecs list-tasks \
  --cluster kubemind-dev-cluster \
  --service-name kubemind-dev-service
```

Describe tasks:

```bash
aws ecs describe-tasks \
  --cluster kubemind-dev-cluster \
  --tasks TASK_ARN
```

---

# 4. ECS Task Stopped

Check stopped reason:

```bash
aws ecs describe-tasks \
  --cluster kubemind-dev-cluster \
  --tasks TASK_ARN \
  --query 'tasks[0].{StopCode:stopCode,StoppedReason:stoppedReason}'
```

Check container:

```bash
aws ecs describe-tasks \
  --cluster kubemind-dev-cluster \
  --tasks TASK_ARN \
  --query 'tasks[0].containers[].{Name:name,Reason:reason,ExitCode:exitCode}'
```

---

# 5. ALB Returns 503

Check target health:

```bash
aws elbv2 describe-target-health \
  --target-group-arn TARGET_GROUP_ARN
```

Expected:

```text
healthy
healthy
```

Verify:

```text
ALB Listener
    |
    +--> Port 80
    |
    v
Target Group
    |
    +--> Port 8080
    |
    v
ECS Container
    |
    +--> Port 8080
    |
    v
Health Check
    |
    +--> /health
```

---

# 6. ECS Tasks Are Not Starting

Check service events:

```bash
aws ecs describe-services \
  --cluster kubemind-dev-cluster \
  --services kubemind-dev-service \
  --query 'services[0].events[0:10]'
```

Look for:

```text
CannotPullContainerError
ResourceInitializationError
Health check failed
CannotStartContainerError
```

---

# 7. Docker Image Cannot Be Pulled

Check ECR:

```bash
aws ecr describe-images \
  --repository-name kubemind-app \
  --region ap-south-1
```

Verify:

```text
Image exists
Correct repository
Correct tag
Correct region
```

---

# 8. Terraform Output Is Empty

Terraform outputs must be executed from the Terraform directory.

Correct:

```bash
cd /home/ec2-user/.alamgir/kubemind-aws-devops/terraform
```

Then:

```bash
terraform output -raw alb_dns_name
```

Do not execute from:

```text
/home/ec2-user/.alamgir/kubemind-aws-devops
```

unless using the appropriate Terraform working directory/state.

---

# ☁️ Useful AWS Commands

## Current Identity

```bash
aws sts get-caller-identity
```

---

## ECR Repositories

```bash
aws ecr describe-repositories \
  --region ap-south-1
```

---

## ECR Images

```bash
aws ecr describe-images \
  --repository-name kubemind-app \
  --region ap-south-1
```

---

## ECS Clusters

```bash
aws ecs list-clusters \
  --region ap-south-1
```

---

## ECS Services

```bash
aws ecs describe-services \
  --cluster kubemind-dev-cluster \
  --services kubemind-dev-service
```

---

## ECS Tasks

```bash
aws ecs list-tasks \
  --cluster kubemind-dev-cluster \
  --service-name kubemind-dev-service
```

---

## ECS Task Definition

```bash
aws ecs describe-task-definition \
  --task-definition kubemind-dev-app
```

---

## CloudWatch Log Groups

```bash
aws logs describe-log-groups \
  --log-group-name-prefix /ecs/kubemind-dev
```

---

# 🏗️ Useful Terraform Commands

Initialize:

```bash
terraform init
```

Format:

```bash
terraform fmt -recursive
```

Validate:

```bash
terraform validate
```

Plan:

```bash
terraform plan
```

Apply:

```bash
terraform apply
```

Show outputs:

```bash
terraform output
```

ALB DNS:

```bash
terraform output -raw alb_dns_name
```

List resources:

```bash
terraform state list
```

Inspect resource:

```bash
terraform state show RESOURCE
```

Destroy:

```bash
terraform destroy
```

> ⚠️ `terraform destroy` removes infrastructure. Never run it accidentally against a production environment.

---

# 🐙 Useful Git Commands

Check status:

```bash
git status
```

View history:

```bash
git log --oneline --graph --decorate --all
```

Add:

```bash
git add .
```

Commit:

```bash
git commit -m "Update application"
```

Push:

```bash
git push origin main
```

Pull:

```bash
git pull origin main
```

Remote:

```bash
git remote -v
```

Branches:

```bash
git branch
```

---

# 🐳 Useful Docker Commands

List images:

```bash
docker images
```

List running containers:

```bash
docker ps
```

List all containers:

```bash
docker ps -a
```

Build:

```bash
docker build -t kubemind-app:latest .
```

Run:

```bash
docker run -d \
  --name kubemind-app \
  -p 8080:8080 \
  kubemind-app:latest
```

Logs:

```bash
docker logs kubemind-app
```

Stop:

```bash
docker stop kubemind-app
```

Remove:

```bash
docker rm kubemind-app
```

---

# 🔐 Security Architecture

The project follows several security principles.

## 1. No Long-Lived AWS Credentials in GitHub

Instead of:

```text
GitHub
   |
   | Permanent AWS Access Key
   v
AWS
```

we use:

```text
GitHub
   |
   | OIDC Token
   v
AWS STS
   |
   v
Temporary Credentials
```

---

# 2. Private ECS Tasks

ECS tasks run in private subnets:

```text
Internet
    |
    X
    |
    X
ECS Task
```

The application is accessed through:

```text
Internet
    |
    v
ALB
    |
    v
ECS
```

---

# 3. Security Group Restriction

```text
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
```

---

# 4. IAM Least Privilege

The GitHub deployment role only receives the permissions required for:

```text
ECR
+
ECS
+
iam:PassRole
```

Terraform infrastructure permissions should remain separate.

---

# 5. Immutable Image Tags

Instead of:

```text
latest
```

the CI/CD pipeline uses:

```text
github.sha
```

Example:

```text
kubemind-app:8e91a23...
```

---

# 🚀 Production Hardening Roadmap

The current project successfully demonstrates the core deployment platform.

The next step is to harden the architecture for production.

---

# Phase A — Separate CI and CD

Current:

```text
Git Push
    |
    v
Test
    |
    v
Build
    |
    v
Deploy
```

Recommended:

```text
Pull Request
      |
      v
+----------------------+
| CI                   |
|                      |
| Lint                 |
| Unit Tests           |
| Security Scan        |
| Docker Build Test    |
+----------------------+
```

Then:

```text
main
 |
 v
+----------------------+
| CD                   |
|                      |
| Build Image          |
| Push ECR             |
| Deploy ECS            |
| Verify Deployment    |
+----------------------+
```

---

# Phase B — Terraform CI/CD

Recommended pipeline:

```text
Pull Request
      |
      +--> terraform fmt -check
      |
      +--> terraform validate
      |
      +--> terraform plan
      |
      v
Approval
      |
      v
terraform apply
```

Separate IAM roles:

```text
GitHub Terraform Plan Role
GitHub Terraform Apply Role
GitHub Application Deployment Role
```

Do not give the application deployment role unrestricted Terraform permissions.

---

# Phase C — Security Scanning

Recommended tools:

```text
Trivy
CodeQL
Dependabot
GitHub Secret Scanning
IaC Security Scanning
Container Vulnerability Scanning
```

Pipeline:

```text
Source Code
     |
     +--> SAST
     |
     +--> Dependency Scan
     |
     +--> Secret Scan
     |
     +--> IaC Scan
     |
     +--> Container Scan
     |
     v
Deployment
```

---

# Phase D — Deployment Strategies

Current:

```text
Rolling Deployment
```

Future options:

```text
Blue/Green Deployment
```

```text
Canary Deployment
```

```text
Progressive Delivery
```

Add:

```text
Automatic Rollback
```

when deployment health checks fail.

---

# Phase E — Observability

Recommended monitoring:

```text
                    CloudWatch
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
        Logs         Metrics        Alarms
```

Monitor:

```text
ECS CPU
ECS Memory
Running Tasks
Desired Tasks
ALB 4xx
ALB 5xx
ALB Latency
Target Health
Container Restarts
```

---

# Phase F — Secrets Management

Never store secrets in:

```text
Git
Dockerfile
Terraform source
README.md
GitHub workflow YAML
```

Use:

```text
AWS Secrets Manager
```

or:

```text
AWS Systems Manager Parameter Store
```

---

# Phase G — Environment Strategy

Future environment structure:

```text
Development
     |
     v
Staging
     |
     v
Production
```

Example:

```text
GitHub
   |
   +--> dev
   |
   +--> staging
   |
   +--> production
```

Production deployment should use:

```text
Manual Approval
+
Protected Environment
+
Restricted IAM Role
```

---

# 🧠 DevOps Concepts Learned

## Terraform

Terraform manages infrastructure:

```text
Terraform
    |
    +--> VPC
    +--> Subnets
    +--> Route Tables
    +--> Internet Gateway
    +--> NAT Gateway
    +--> Security Groups
    +--> ALB
    +--> IAM
    +--> ECS
    +--> CloudWatch
```

---

# 🐳 Docker

Docker packages:

```text
Application
     +
Dependencies
     +
Runtime
     |
     v
Docker Image
```

---

# 📦 Amazon ECR

ECR stores Docker images:

```text
Docker Build
     |
     v
Docker Image
     |
     v
Amazon ECR
```

---

# 🚢 Amazon ECS

ECS manages containers:

```text
ECR Image
     |
     v
Task Definition
     |
     v
ECS Service
     |
     v
Fargate Tasks
```

---

# 🌐 Application Load Balancer

ALB routes application traffic:

```text
Internet
    |
    v
ALB :80
    |
    v
Target Group :8080
    |
    v
ECS Fargate
```

---

# 🔑 GitHub OIDC

OIDC enables keyless AWS authentication:

```text
GitHub Actions
      |
      | OIDC
      v
AWS STS
      |
      v
Temporary Credentials
      |
      v
AWS Resources
```

---

# 🏷️ Deployment Traceability

The deployment creates a relationship:

```text
Git Commit
     |
     v
GitHub Actions
     |
     v
Docker Image
     |
     v
ECR
     |
     v
ECS Task Definition
     |
     v
Running Container
```

This makes it possible to identify which source code version is running.

---

# 🧪 Final End-to-End Validation

Run:

```bash
cd /home/ec2-user/.alamgir/kubemind-aws-devops/terraform
```

Get ALB:

```bash
terraform output -raw alb_dns_name
```

Application:

```bash
curl http://$(terraform output -raw alb_dns_name)/
```

Expected:

```text
🚀 KubeMind AI is running!
```

Health:

```bash
curl http://$(terraform output -raw alb_dns_name)/health
```

Expected:

```json
{
  "status": "healthy"
}
```

ECS:

```bash
aws ecs describe-services \
  --cluster kubemind-dev-cluster \
  --services kubemind-dev-service \
  --query 'services[0].{Desired:desiredCount,Running:runningCount,Pending:pendingCount,Status:status,TaskDefinition:taskDefinition}' \
  --output table
```

Expected:

```text
Desired   Pending   Running   Status
2         0         2         ACTIVE
```

---

# 📋 Final Project Checklist

## Application

```text
[✓] Flask application created
[✓] / endpoint created
[✓] /health endpoint created
[✓] Python dependencies configured
[✓] Pytest tests created
[✓] Tests passing
```

## Docker

```text
[✓] Dockerfile created
[✓] Docker image built
[✓] Docker container started
[✓] Application tested locally
[✓] Health endpoint tested locally
```

## Amazon ECR

```text
[✓] ECR repository created
[✓] Docker authenticated
[✓] Docker image tagged
[✓] Docker image pushed
```

## Terraform

```text
[✓] Terraform initialized
[✓] S3 backend configured
[✓] Remote state configured
[✓] State locking configured
[✓] VPC created
[✓] Public subnets created
[✓] Private subnets created
[✓] Internet Gateway created
[✓] NAT Gateway created
[✓] Route tables created
[✓] Security Groups created
[✓] Application Load Balancer created
[✓] Target Group created
[✓] ECS Cluster created
[✓] ECS Service created
[✓] Task Definition created
[✓] IAM roles created
[✓] CloudWatch log group created
```

## ECS

```text
[✓] ECS service ACTIVE
[✓] Desired tasks = 2
[✓] Running tasks = 2
[✓] Pending tasks = 0
[✓] Target 1 healthy
[✓] Target 2 healthy
```

## GitHub

```text
[✓] GitHub repository created
[✓] Git initialized
[✓] Remote configured
[✓] Main branch configured
[✓] Source pushed
```

## GitHub OIDC

```text
[✓] GitHub OIDC provider configured
[✓] IAM deployment role created
[✓] Trust policy configured
[✓] Repository restricted
[✓] Main branch restricted
[✓] OIDC authentication successful
[✓] AWS identity verified
```

## GitHub Actions

```text
[✓] Workflow created
[✓] Python setup
[✓] Dependency installation
[✓] Automated tests
[✓] AWS OIDC authentication
[✓] ECR login
[✓] Docker build
[✓] Docker push
[✓] ECS task definition rendered
[✓] ECS deployment
[✓] ECS service stability verified
```

## Runtime

```text
[✓] ALB accessible
[✓] Application endpoint working
[✓] Health endpoint working
[✓] ECS service ACTIVE
[✓] 2/2 tasks running
[✓] New task definition revision deployed
```

---

# 🏆 Final Architecture

```text
                         KUBEMIND AI
                    AWS DEVOPS PLATFORM


                         DEVELOPER
                             |
                             |
                       git push main
                             |
                             v
                     +---------------+
                     |    GitHub     |
                     |   Repository  |
                     +-------+-------+
                             |
                             v
                   +-------------------+
                   | GitHub Actions    |
                   +---------+---------+
                             |
              +--------------+--------------+
              |                             |
              v                             v
         Python Tests                  GitHub OIDC
              |                             |
              |                             v
              |                         AWS STS
              |                             |
              |                             v
              |                      AWS IAM Role
              |                             |
              |                 +-----------+-----------+
              |                 |                       |
              |                 v                       v
              |                ECR                     ECS
              |                 |                       |
              |                 |               Task Definition
              |                 |                       |
              |                 +-----------------------+
              |                                         |
              |                                         v
              |                                  Fargate × 2
              |                                         |
              |                                         v
              |                                        ALB
              |                                         |
              +-----------------------------------------+
                                                        |
                                                        v
                                                🚀 KubeMind AI
```

---

# 🔄 Complete CI/CD Lifecycle

```text
                     SOURCE
                       |
                       v
                 GitHub Repository
                       |
                       v
                 GitHub Actions
                       |
                       v
                  Unit Testing
                       |
                       v
                  OIDC Login
                       |
                       v
                   AWS IAM
                       |
                       v
                  Docker Build
                       |
                       v
                     ECR
                       |
                       v
               Docker Image
                       |
                       v
             ECS Task Definition
                       |
                       v
               ECS Fargate
                       |
                       v
              Application Load
                 Balancer
                       |
                       v
                 APPLICATION
                       |
                       v
                  HEALTH CHECK
                       |
                       v
                    SUCCESS
```

---

# 🎯 Final Project Result

The KubeMind AI project successfully demonstrates:

```text
GitHub
   ↓
GitHub Actions
   ↓
Automated Tests
   ↓
GitHub OIDC
   ↓
AWS IAM
   ↓
Amazon ECR
   ↓
Docker Image
   ↓
ECS Task Definition
   ↓
Amazon ECS Fargate
   ↓
Application Load Balancer
   ↓
KubeMind AI
```

Final application:

```text
🚀 KubeMind AI is running!
```

Health:

```json
{
  "status": "healthy"
}
```

ECS:

```text
Desired = 2
Running = 2
Pending = 0
Status  = ACTIVE
```

---

# 📚 Official Documentation

## GitHub

GitHub README documentation:

[https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)

GitHub Actions:

[https://docs.github.com/en/actions](https://docs.github.com/en/actions)

GitHub OIDC:

[https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws)

---

## AWS

AWS IAM:

[https://docs.aws.amazon.com/IAM/latest/UserGuide/](https://docs.aws.amazon.com/IAM/latest/UserGuide/)

AWS OIDC:

[https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_oidc.html](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_oidc.html)

Amazon ECR:

[https://docs.aws.amazon.com/AmazonECR/latest/userguide/](https://docs.aws.amazon.com/AmazonECR/latest/userguide/)

Amazon ECS:

[https://docs.aws.amazon.com/AmazonECS/latest/developerguide/](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/)

AWS Fargate:

[https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html)

Application Load Balancer:

[https://docs.aws.amazon.com/elasticloadbalancing/latest/application/](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/)

Amazon VPC:

[https://docs.aws.amazon.com/vpc/latest/userguide/](https://docs.aws.amazon.com/vpc/latest/userguide/)

Amazon CloudWatch:

[https://docs.aws.amazon.com/cloudwatch/](https://docs.aws.amazon.com/cloudwatch/)

---

## Terraform

Terraform Documentation:

[https://developer.hashicorp.com/terraform/docs](https://developer.hashicorp.com/terraform/docs)

Terraform AWS Provider:

[https://registry.terraform.io/providers/hashicorp/aws/latest/docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

Terraform S3 Backend:

[https://developer.hashicorp.com/terraform/language/backend/s3](https://developer.hashicorp.com/terraform/language/backend/s3)

---

# 👨‍💻 Author

## SK Alamgir Ali

**Project:**

```text
KubeMind AI
```

**Track:**

```text
AWS DevOps
Cloud Architecture
Infrastructure as Code
CI/CD
Containerization
Cloud Security
```

**Technology Stack:**

```text
Python
Flask
Gunicorn
Pytest
Docker
Terraform
AWS
Amazon VPC
Amazon ECR
Amazon ECS
AWS Fargate
Application Load Balancer
AWS IAM
GitHub
GitHub Actions
GitHub OIDC
Amazon CloudWatch
Amazon S3
```

---

# 🏁 Project Status

| Component                 | Status      |
| ------------------------- | ----------- |
| Python Application        | ✅ Completed |
| Flask                     | ✅ Completed |
| Pytest                    | ✅ Completed |
| Docker                    | ✅ Completed |
| Amazon ECR                | ✅ Completed |
| Terraform                 | ✅ Completed |
| VPC                       | ✅ Completed |
| Public Subnets            | ✅ Completed |
| Private Subnets           | ✅ Completed |
| NAT Gateway               | ✅ Completed |
| Internet Gateway          | ✅ Completed |
| Security Groups           | ✅ Completed |
| Application Load Balancer | ✅ Completed |
| Target Group              | ✅ Completed |
| ECS Cluster               | ✅ Completed |
| ECS Fargate               | ✅ Completed |
| CloudWatch                | ✅ Completed |
| IAM                       | ✅ Completed |
| GitHub Repository         | ✅ Completed |
| GitHub OIDC               | ✅ Completed |
| GitHub Actions            | ✅ Completed |
| Automated CI/CD           | ✅ Completed |
| Application Verification  | ✅ Completed |

---

# 🚀 Final Achievement

```text
┌──────────────────────────────────────────────────────┐
│                                                      │
│                 KUBEMIND AI                          │
│                                                      │
│          AWS DEVOPS CI/CD PLATFORM                   │
│                                                      │
│  GitHub                                               │
│     ↓                                                │
│  GitHub Actions                                       │
│     ↓                                                │
│  Automated Tests                                      │
│     ↓                                                │
│  GitHub OIDC                                          │
│     ↓                                                │
│  AWS IAM                                              │
│     ↓                                                │
│  Amazon ECR                                           │
│     ↓                                                │
│  ECS Fargate × 2                                      │
│     ↓                                                │
│  Application Load Balancer                            │
│     ↓                                                │
│  🚀 KubeMind AI                                       │
│                                                      │
│       END-TO-END CI/CD: ✅ SUCCESSFUL                │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

# ⭐ What This Project Demonstrates

This project demonstrates the complete DevOps lifecycle:

```text
PLAN
  ↓
CODE
  ↓
TEST
  ↓
BUILD
  ↓
PACKAGE
  ↓
PUSH
  ↓
DEPLOY
  ↓
VERIFY
  ↓
MONITOR
  ↓
IMPROVE
```

The final platform connects:

```text
Application Development
        +
Containerization
        +
Infrastructure as Code
        +
Cloud Infrastructure
        +
Identity and Access Management
        +
CI/CD
        +
Observability
        =
Production-Oriented DevOps Platform
```

---

# 🎓 End of Hands-On Lab

**KubeMind AI — Production-Grade AWS DevOps CI/CD**

```text
GitHub → GitHub Actions → OIDC → AWS
       → ECR → ECS Fargate → ALB
       → KubeMind AI
```

**Status: 🚀 END-TO-END DEPLOYMENT SUCCESSFUL**

````

### After pasting

Save in `nano`:

```text
Ctrl + O
Enter
Ctrl + X
````

Then run:

```bash
cd /home/ec2-user/.alamgir/kubemind-aws-devops

git add README.md

git commit -m "Add complete KubeMind AI hands-on lab documentation"

git push origin main
```

One important point: in the README, `ACCOUNT_ID` is intentionally a placeholder so you don't unnecessarily publish your AWS account number throughout your documentation. Your actual GitHub Actions workflow should continue using the real account ID where required.
