# Securely Deploy and Expose Applications on Kubernetes (EKS) – With Policy Enforcement

**Author:** Mohamed Mohamed  
**Email:** mohamed0395@gmail.com
![Image](https://imgur.com/3PAp9su.png)
This project demonstrates a full, production-style Kubernetes deployment pipeline using **Amazon EKS**, **Terraform**, **ECR**, **Kyverno**, and the **AWS ALB Ingress Controller**. Along the way, I encountered—and overcame—real-world infrastructure and security challenges. This documentation walks through each phase of the journey, including key learnings and troubleshooting strategies I used.

> 💡 _This wasn’t just a deployment. It was a debugging playground, a security lab, and a crash course in AWS infrastructure recovery. I built, broke, patched, and rebuilt._

---

## 📦 Overview
A secure and observable microservice deployment on EKS:
- Infrastructure as Code using **Terraform**
- Secure policy enforcement with **Kyverno**
- Application exposed through **AWS ALB Ingress Controller**
---

## 🏗️ Infrastructure Provisioning with Terraform

### Tools Used:
- Terraform (v1.6+)
- AWS EKS
- AWS ECR
- Helm

### Resources Provisioned:
- VPC (public subnets + Internet Gateway)
- EKS Cluster + Node Group
- IAM roles and policies for Kubernetes components

### Key Learnings & Hurdles:
Deploying the VPC and EKS cluster was smooth initially, but teardown revealed an important lesson: **Terraform state management must be coupled with AWS console awareness**. Several dependency violations occurred due to ENIs and internet gateway detachment errors. I documented this, adjusted resource dependencies, and even dove into the AWS Console and CLI to manually release resources that blocked the destroy process.

![image](https://imgur.com/cuNSsH3.png)
---

## 🐍 Application Deployment (Flask App)

My Flask application was containerized and deployed to the EKS cluster.

### Steps:
- Dockerized the app (`Dockerfile`, `app.py`, `requirements.txt`)
- Pushed image to **Amazon ECR**
- Created Kubernetes manifests for Deployment and Service

![image](https://imgur.com/JZjX3zW.png)
![image](https://imgur.com/Z5DOXyp.png)

---

## 🌐 Exposing the App with ALB Ingress Controller

This was one of the trickiest parts.

### Challenges Faced:
- ALB not provisioning: traced root cause to a missing **IAM policy binding** for the Kubernetes service account.
- Ingress status stuck: fixed by annotating the correct `alb.ingress.kubernetes.io/*` fields and confirming VPC subnets tagged as public.
- Webhook probe failures: I had to **fully tear down and rebuild** the ALB Controller with correct IAM and Helm setup.

![Image](https://imgur.com/IjDVwzC.png)
![Image](https://imgur.com/qCKVt6o.png)


---

## 🛡️ Security Policy Enforcement with Kyverno

Kyverno was used to define and enforce three cluster-wide policies:
- Disallow containers running as root
- Enforce `readOnlyRootFilesystem`
- Drop all Linux capabilities

### Roadblocks:
- Policies failed to apply at first — discovered Kyverno CRDs hadn’t been installed. Installed them via Helm and verified with `kubectl get clusterpolicy`.

---

## 🔥 Teardown + Clean-Up

This was the most challenging phase.

### What Went Wrong:
- Subnets refused to delete (DependencyViolation errors)
- ENIs still in use by ALB were blocking VPC teardown
- IAM roles stuck in use

### Resolution:
- Identified and manually detached ENIs via AWS Console
- Used `terraform taint` and `terraform destroy -target` to isolate and force-remove hanging resources

![image](https://imgur.com/GDNfPdy.png)


---

## 📚 Summary & Reflection
This project wasn’t just about deploying an app. It was about:
- Troubleshooting IAM, networking, and Kubernetes misconfigurations
- Gaining hands-on experience with **real-world DevSecOps problems**
- Ensuring everything from **security posture** to **observability** was handled correctly

### 🚧 What I Learned
- ALB Ingress and EKS permissions
- Kyverno policy lifecycle
- Terraform state and cleanup strategies
- That error messages are like breadcrumbs — **follow them**

This wasn’t a copy-paste deployment. It was a **battle-tested, hardened, debugged** journey through the EKS ecosystem. Every issue was an opportunity to learn, every roadblock a lesson in resilience.

---

## 📁 Directory Structure
```bash
.
├── app.py
├── Dockerfile
├── requirements.txt
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
├── kyverno/
│   ├── disallow-run-as-root.yaml
│   ├── require-readonly-rootfs.yaml
│   └── restrict-capabilities.yaml
├── terraform-eks/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
```

---

## 🔗 Useful Commands
```bash
# Terraform
terraform init && terraform apply
terraform destroy

# Docker + ECR
aws ecr get-login-password | docker login

docker build -t flask-app .
docker tag flask-app:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/flask-app

docker push <ecr-uri>

# Kubernetes
kubectl apply -f .
kubectl get pods -n monitoring
kubectl get ingress -n monitoring
```

---

## ✅ Conclusion
This project was more than just deploying a Flask app to Kubernetes—it was a full journey through designing, securing, monitoring, and troubleshooting a real-world cloud-native architecture. From managing IAM permissions and Kyverno policies to exposing services with ALB and wiring up observability with Grafana, every step pushed my DevSecOps skills to the next level.

I walked away with not just a working deployment, but a deeper confidence in navigating the complexities of AWS, Kubernetes, and infrastructure-as-code tooling under real conditions.


