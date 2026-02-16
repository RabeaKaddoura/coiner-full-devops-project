# 💰 Coiner - Personal Finance Manager – End-To-End DevOps Project

![AWS](https://img.shields.io/badge/AWS-Cloud-orange?logo=amazon-aws)
![Kubernetes](https://img.shields.io/badge/Kubernetes-EKS-blue?logo=kubernetes)
![Terraform](https://img.shields.io/badge/IaC-Terraform-purple?logo=terraform)
![ArgoCD](https://img.shields.io/badge/GitOps-ArgoCD-orange?logo=argo)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue?logo=postgresql)

A production-grade Personal Finance Management Web Application deployed on AWS using modern DevOps practices including Infrastructure as Code, GitOps, Kubernetes, Canary Deployments, and comprehensive monitoring.

This project demonstrates a complete end-to-end DevOps workflow from developer commit to production deployment inside a secure AWS environment.

---

## 📑 Table of Contents

- [Project Overview](#-project-overview)
- [Architecture](#-architecture)
  - [Developer Workflow](#-developer-workflow)
  - [AWS Infrastructure](#️-aws-infrastructure)
  - [Security Architecture](#-security-architecture)
- [Technology Stack](#-technology-stack)
- [Deployment Strategy](#-deployment-strategy)
- [Monitoring & Observability](#-monitoring--observability)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Application Features](#-application-features)
- [Database Design](#-database-design)
- [Repository Structure](#-repository-structure)
- [Getting Started](#-getting-started)
- [Scaling & Reliability](#-scaling--reliability)
- [DevOps Practices](#-devops-practices-demonstrated)
- [Future Improvements](#-future-improvements)

---

## 📌 Project Overview

The application allows authenticated users to:

- ✅ Create up to 2 wallets
- ✅ Record income and expense transactions
- ✅ Set and track budgets
- ✅ Define financial goals
- ✅ View insights & reports with spending visualization
- ✅ Store all financial data securely per user account

The system is fully containerized and deployed on **Amazon EKS** using **Helm**, with **ArgoCD** managing GitOps synchronization and **Argo Rollouts** for progressive delivery.

---

## 🏗 Architecture

### 🔄 Developer Workflow

```
Developer
   ↓
GitHub Repository
   ↓
GitHub Actions (CI)
   ↓
Build Docker Image
   ↓
Push to Amazon ECR
   ↓
ArgoCD detects Helm changes
   ↓
Deploy to Amazon EKS
   ↓
Canary Rollout (progressive traffic shift)
   ↓
Application Available via ALB
```

### ☁️ AWS Infrastructure

#### 🌍 External to VPC

- GitHub (Source Control)
- GitHub Actions (CI Pipeline)
- Amazon ECR (Container Registry)
- AWS Secrets Manager
- Internet Users

#### 🏢 Inside AWS VPC

**VPC Design:**
- 2 Public Subnets
- 2 Private Subnets

**Public Subnets:**
- Application Load Balancer (ALB)
- NAT Gateway (for outbound internet access)

**Private Subnets:**
- Amazon EKS Cluster & Worker Nodes
- RDS PostgreSQL
- Prometheus
- Grafana

### 🔐 Security Architecture

Security is a core feature of this project.

#### 🛡 Network Isolation

- EKS worker nodes are deployed in **private subnets**
- RDS PostgreSQL is deployed in **private subnet**
- No direct public access to database
- All internet-bound traffic routes through NAT Gateway

#### 🔒 Security Groups

- **RDS:** Only allows inbound traffic from backend pods
- **ALB:** Allows HTTP/HTTPS from internet
- **Worker Nodes:** Allow traffic only within cluster/VPC
- Restricted outbound rules following principle of least privilege

#### 🔑 Secrets Management

- **AWS Secrets Manager** stores:
  - Database credentials
  - Application secrets
    
- Secrets injected securely into Kubernetes pods
- No hardcoded credentials in code

#### 🔐 Authentication

- Users must authenticate to access the application
- Financial data is isolated per user
- Secure session handling

---

## 🧱 Technology Stack

### ☁️ Infrastructure

| Technology | Purpose |
|------------|---------|
| **Terraform** | Infrastructure as Code |
| **Amazon VPC** | Network isolation |
| **Amazon EKS** | Kubernetes cluster |
| **Amazon RDS** | PostgreSQL database |
| **Amazon ECR** | Container registry |
| **AWS Secrets Manager** | Secrets storage |
| **Application Load Balancer** | Traffic distribution |

### 🚀 Deployment & GitOps

| Technology | Purpose |
|------------|---------|
| **Helm** | Kubernetes package manager |
| **ArgoCD** | GitOps continuous delivery |
| **Argo Rollouts** | Canary deployments |
| **GitHub Actions** | CI pipeline automation |

### 📊 Monitoring

| Technology | Purpose |
|------------|---------|
| **Prometheus** | Metrics collection |
| **Grafana** | Metrics visualization |

### 💻 Application

| Technology | Purpose |
|------------|---------|
| **Vue.js** | Frontend framework |
| **Django** | Backend API |
| **PostgreSQL** | Relational database |

---

## 🚀 Deployment Strategy

### GitOps with ArgoCD

ArgoCD continuously monitors the Git repository for Helm chart changes and syncs them automatically to the cluster.

**Benefits:**
- ✅ Declarative deployments
- ✅ Automatic drift detection
- ✅ Version-controlled infrastructure
- ✅ Rollback capabilities
- ✅ Audit trail

### 🐤 Canary Rollout (Progressive Delivery)

Backend deployments use **Canary Strategy**:

1. New version deployed alongside stable version
2. Small percentage of traffic routed to canary (e.g., 10%)
3. Metrics observed via Prometheus
4. Gradual traffic increase (20% → 50% → 100%)
5. Old version terminated after successful rollout

**This ensures:**
- ✅ Zero downtime deployments
- ✅ Reduced deployment risk
- ✅ Safer production releases
- ✅ Quick rollback capability

---

## 📊 Monitoring & Observability

### Prometheus

- Collects application metrics
- Monitors pod health and performance
- Tracks rollout metrics
- Provides alerting capabilities

### Grafana

**Displays dashboards for:**
- Request rates and latency
- Error rates and success metrics
- Resource usage (CPU, Memory)
- Database performance
- Financial insights metrics
- Canary rollout progress

---

## 🧪 CI/CD Pipeline

### Continuous Integration (GitHub Actions)

**On every push to main branch:**

1. ✅ Run automated tests
2. ✅ Build Docker image
3. ✅ Tag image with commit SHA
4. ✅ Push image to Amazon ECR
5. ✅ Update Helm values file with new image tag
6. ✅ Commit changes to trigger ArgoCD

### Continuous Deployment (ArgoCD)

1. ✅ Detects changes in Git repository
2. ✅ Syncs Helm charts to EKS
3. ✅ Triggers Canary rollout
4. ✅ Monitors deployment health
5. ✅ Automatically promotes or rolls back

---

## 💰 Application Features

### 💼 Wallet Management
- Create up to 2 wallets per user
- Track balances
- View transaction history

### 💳 Transactions
- Record income & expenses
- Categorized entries (Food, Transport, Entertainment, etc.)
- Table view with filtering and sorting
- Transaction details and notes

### 🎯 Goals
- Define savings goals
- Track progress with visual indicators
- Set target amounts and deadlines

### 📊 Reports & Insights
- Spending visualization (charts and graphs)
- Budget tracking and alerts
- Monthly/yearly financial summaries
- Category-wise expense breakdown

---

## 🗄 Database Design

**PostgreSQL hosted on Amazon RDS:**
- Private subnet only (no public access)
- Persistent storage with automated backups
- Encrypted at rest
- Multi-AZ deployment for high availability

**Data Models Include:**
- **Users:** Authentication and profile data
- **Wallets:** Max 2 per user with balance tracking
- **Transactions:** Income/expense records with categories
- **Budgets:** Monthly budget limits per category
- **Goals:** Savings targets with progress tracking

---

## 🔄 Scaling & Reliability

- ✅ **Rolling updates** with Canary strategy
- ✅ **Health checks** and readiness probes
- ✅ **Metrics-based monitoring** for proactive issue detection
- ✅ **Multi-AZ deployment** for high availability
- ✅ **Automated failover** for database

---

## 🏆 DevOps Practices Demonstrated

This project showcases industry-standard DevOps practices:

- ✅ **Infrastructure as Code (IaC)** with Terraform
- ✅ **GitOps** with ArgoCD for declarative deployments
- ✅ **Progressive Delivery** with Canary rollouts
- ✅ **CI/CD Automation** with GitHub Actions
- ✅ **Secure Cloud Architecture** with AWS best practices
- ✅ **Monitoring & Observability** with Prometheus and Grafana
- ✅ **Containerized Microservices** architecture
- ✅ **Network Segmentation** with public/private subnets
- ✅ **Principle of Least Privilege** for security
- ✅ **Secrets Management** with AWS Secrets Manager
- ✅ **Automated Testing** in CI pipeline



## 👨‍💻 Author

**YOUR_NAME**  
DevOps Engineer | Cloud Enthusiast

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)]([YOUR_LINKEDIN_URL](https://www.linkedin.com/in/rabea-kaddoura-3ab858228/))

