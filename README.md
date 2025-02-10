Missing Bus Reporter NI 🚍

A Flask app for reporting missing buses in Northern Ireland. Deployed via Docker on AWS EC2 using GitHub Actions and Amazon ECR.
🚀 Setup & Run
1️⃣ Install Dependencies

pip install -r requirements.txt

2️⃣ Run Locally

flask run

Access at http://127.0.0.1:5000
📦 Docker Setup
1️⃣ Build & Run Container

docker build -t missing-bus-reporter .
docker run -d -p 5000:5000 --name flask-container missing-bus-reporter

🚀 Deployment (GitHub Actions + EC2)
1️⃣ GitHub Secrets

Set these in GitHub → Settings → Secrets:

    SSH_PRIVATE_KEY – SSH key for EC2
    EC2_PUBLIC_IP – EC2 instance IP
    AWS_REGION – AWS region
    ECR_REPOSITORY – ECR repo URI

2️⃣ Deployment Process

Pushing to main triggers:

    Docker build & push to ECR
    EC2 pulls the image & restarts the container

📍 Access the App

http://<EC2_PUBLIC_IP>:5000

Check Running Containers

docker ps -a
docker logs flask-container

