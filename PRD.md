Product Requirement Document (PRD)
Simple 2FA Email Login Page (Django + Jenkins DevOps Pipeline)
1. 🧭 Project Overview

Project Name: Simple-2FA-Email-Login
Objective:
Develop a minimal but secure web login page with 2-Factor Authentication using Email OTP, deployed with Jenkins CI/CD pipeline.

Primary Focus: DevOps delivery workflow — build, test, deploy, and manage the app automatically using Jenkins and Infrastructure as Code.

2. 🎯 Goals & Scope
Goals ✅	Non-Goals ❌
Implement email-based 2FA login page	TOTP / biometric / advanced MFA
Automate build, test, and deployment via Jenkins	Mobile application
Containerize application using Docker	UI enhancements beyond basic forms
Deploy using Terraform + Ansible	Multi-cloud support
Basic monitoring & rollback	Advanced analytics
3. 🧰 DevOps Tools Stack
Tool / Tech	Purpose
GitHub / GitLab	Version Control
Jenkins	CI/CD automation
Docker	Containerization
Terraform	Infrastructure provisioning (AWS / local VM)
Ansible	Server configuration & deployment
Nginx	Reverse proxy, HTTPS termination
Django (Python)	Web application logic (email login & OTP verification)
PostgreSQL	User & OTP storage
SMTP	Email OTP delivery
Prometheus + Grafana	Monitoring
4. 🧑‍💻 Functional Requirements
ID	Feature	Description
FR-01	User Registration	Simple registration with email & password
FR-02	Login Page	User enters email & password
FR-03	Email OTP Trigger	OTP sent to registered email
FR-04	OTP Verification Page	User enters OTP to complete login
FR-05	OTP Expiry	OTP expires after 2 minutes
FR-06	Logout	End session
FR-07	Basic Audit Logs	Log login/OTP events
5. 📈 Non-Functional Requirements
Category	Requirement
Security	HTTPS, secrets managed securely
Performance	Handle at least 200 concurrent logins
Scalability	Container-based, can scale horizontally
Observability	Monitoring and alerts for pipeline & app
Availability	99.9% uptime
DevOps Automation	Jenkins pipeline must fully automate build → deploy → rollback
6. 🧭 System Architecture (High-Level)
+-------------+         +---------------+       +------------------+
|   Browser   |  --->   |   Nginx + SSL |  -->  |  Django Backend  |
+-------------+         +---------------+       +--------+---------+
                                                      |
              +------------------+--------------------+----------------+
              |                  |                                     |
              ▼                  ▼                                     ▼
       +-------------+   +-----------------+                   +----------------+
       | PostgreSQL  |   | SMTP (Email OTP)|                   | Prometheus/Grafana |
       +-------------+   +-----------------+                   +----------------+
                                ▲
                                │
                       +--------+---------+
                       | Jenkins Pipeline |
                       | (Build/Test/Deploy) |
                       +---------------------+

7. 🧰 CI/CD Pipeline — Jenkins
Pipeline Stages

SCM Checkout – Pull latest code from Git.

Build – Install dependencies & run linting.

Test – Run Django unit tests (OTP flow).

Docker Build – Build image with tag.

Push Image – Push to Docker Hub.

Infra Provision – Run Terraform (if needed).

Deploy – Run Ansible playbook to deploy container.

Smoke Test & Notify – Test endpoint & send Slack/email on success/failure.

8. 🐳 Infrastructure Layout
Component	Description	Tool
EC2 VM / On-Prem Node	Host Django + Nginx container	Terraform
Jenkins Server	Automate CI/CD	Manual or Terraform
PostgreSQL	User and OTP storage	RDS / Container
SMTP	OTP delivery	SES / Mailtrap
Nginx	Reverse proxy	Ansible
9. 📂 Repository Structure
2fa-email-login/
├── app/
│   ├── manage.py
│   ├── config/
│   ├── authentication/
│   │   ├── views.py
│   │   ├── models.py
│   │   ├── email_otp.py
│   │   └── urls.py
│   ├── templates/
│   │   ├── login.html
│   │   └── otp.html
│   └── tests/
│       └── test_auth.py
│
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── nginx.conf
│
├── infra/
│   ├── terraform/
│   └── ansible/
│       └── deploy.yml
│
├── jenkins/
│   └── Jenkinsfile
│
├── requirements.txt
├── .env.example
└── README.md

10. 🧪 Testing & Quality Gates
Type	Tool	Description
Unit Test	Django Test	Check login + OTP flow
Lint	flake8, black	Code quality
Integration Test	pytest	End-to-end flow
Load Test	locust	OTP under load
Security Test	bandit	Basic vulnerability checks
Jenkins Smoke Test	curl endpoint	Validate deployment health
11. ⚠️ Risks & Mitigation
Risk	Description	Mitigation
Jenkins failure	Pipeline breaks	Rollback to previous image
Email delivery delay	OTP may be slow	Use reliable SMTP / short timeout
Secrets exposure	Sensitive creds in repo	Use Jenkins Credentials Vault
Infra drift	Manual infra edits break deploy	Manage infra with Terraform
OTP replay attack	Reuse of OTP codes	Single-use OTP with 2 min expiry
12. 🕒 Milestones
Phase	Deliverable	Duration
Phase 1: Setup Jenkins CI/CD	Jenkins server + pipeline live	1 week
Phase 2: Django App	Simple login & email OTP working	1 week
Phase 3: Infra Automation	Terraform + Ansible provisioning	1 week
Phase 4: Deployment	Containerized deployment via Jenkins	1 week
Phase 5: Monitoring	Prometheus + alerting configured	1 week
13. ✅ Acceptance Criteria

 Jenkins pipeline automates full flow (build → test → deploy)

 Login & Email OTP flow works end-to-end

 OTP expires after 2 minutes & is single-use

 Secrets stored securely in Jenkins

 Monitoring dashboard up (Prometheus + Grafana)

 Rollback possible via Jenkins if deploy fails

14. 🔮 Future Enhancements (Optional)

Add TOTP support (Google Authenticator)

Add social login (Google, GitHub)

Deploy to Kubernetes cluster

Integrate with Vault for advanced secrets

Add API endpoints with DRF

✅ Final Note:
This project emphasizes DevOps automation over feature complexity — using Jenkins, Docker, Terraform, and Ansible to manage a secure 2FA login app with full CI/CD and infrastructure control.



Here’s a technical architecture blueprint for the Simple 2FA Email Login Page Project based on the PRD you requested — with a strong DevOps focus (Jenkins CI/CD, containerization, and infrastructure as code).

🏗️ 1. Technical Architecture Overview

Core Components:

Frontend: Basic HTML/CSS/JavaScript (served by Django templates)

Backend: Django web framework (Python)

Authentication: Django’s built-in auth + Email OTP for 2FA

Database: PostgreSQL (for user management and OTP logs)

CI/CD: Jenkins pipeline with GitHub integration

Containerization: Docker (App + DB services)

Reverse Proxy: Nginx

IaC & Deployment: Ansible or Terraform (optional for infra automation)

Workflow:

User enters email & password.

Django authenticates user credentials.

An OTP is generated and sent to the user’s registered email.

User enters OTP to complete login.

Jenkins automates build, test, and deployment to dev/prod.

Application runs behind Nginx with HTTPS.

🗂️ 2. Folder Structure
2fa-auth-project/
├── app/
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── 2fa_app/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   ├── authentication/
│   │   ├── __init__.py
│   │   ├── views.py
│   │   ├── models.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   └── utils.py (OTP generation, mailer)
│   ├── templates/
│   │   ├── login.html
│   │   ├── verify_otp.html
│   │   └── dashboard.html
│   └── static/
│       └── css/
│           └── style.css
│
├── jenkins/
│   ├── Jenkinsfile
│
├── nginx/
│   └── default.conf
│
├── docker-compose.yml
├── ansible/
│   └── deploy.yml (optional)
└── README.md

🧰 3. Key Python Libraries
Library	Purpose
Django	Web framework
django-allauth	Authentication (optional)
psycopg2	PostgreSQL DB adapter
python-dotenv	Manage environment variables
django-otp	OTP management (optional)
smtplib / email	Sending OTP via email
gunicorn	WSGI server
🗃️ 4. Database Schema
User (Django default auth_user):

id (PK)

username

email (unique)

password_hash

is_active

OTPLog:
Field	Type	Description
id	PK	Unique identifier
user_id	FK → User	Reference to user
otp_code	VARCHAR(6)	Generated OTP
created_at	DateTime	OTP creation timestamp
is_used	Boolean	Whether OTP is used or expired
🔄 5. Jenkins CI/CD Pipeline Flow
Jenkinsfile (High Level Stages)

SCM Checkout: Pull from GitHub

Build Stage:

pip install -r requirements.txt

run linting (flake8)

Test Stage:

Run Django unit tests

Docker Build & Push:

Build image

Push to Docker Hub or ECR

Deploy Stage:

SSH to server or use Ansible

docker-compose pull && up -d

Post: Slack/email notifications.

🌐 6. DevOps Tooling Stack
Tool	Purpose
GitHub	Source code repository
Jenkins	CI/CD automation
Docker	Containerization
Nginx	Reverse proxy & HTTPS
PostgreSQL	Database
Ansible/Terraform	Infrastructure as Code (optional)
Slack/Email	Notification hooks
⚠️ 7. Potential Implementation Challenges
Area	Challenge	Mitigation
Email Delivery	Emails landing in spam	Use a trusted SMTP (e.g., SendGrid, SES)
OTP Expiry	Handling race conditions (reuse, delays)	Add expiry + is_used flags
Jenkins Pipeline	Failing builds due to dependencies	Use Docker agents, pinned versions
Secrets Management	Exposing credentials in Jenkins	Use Jenkins credentials store or .env in secrets manager
Scaling	Handling multiple login requests	Gunicorn workers + load balancing
Security	Brute force OTP attempts	Rate limiting, captcha (optional)
🏁 8. Scalability & Future Enhancements

Add Google Authenticator / TOTP in future.

Use Redis for caching OTP for performance.

Deploy to AWS ECS / EKS with Terraform for infra automation.

Integrate monitoring (Prometheus + Grafana).

Add Sentry for error tracking.

✅ Summary:
This architecture leverages Django for the core app, Jenkins for DevOps automation, Docker + Nginx for deployment, and PostgreSQL for persistence. It’s production-ready with room to scale and secure with proper CI/CD best practices.
