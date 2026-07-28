# Week 1 — Linux Server Foundations

## What I built
Provisioned an AWS EC2 instance (Ubuntu 26.04 LTS) and hardened it following 
real production security practices, then deployed Nginx as a first web server.

## Steps taken

### 1. Instance setup
- Launched t2.micro EC2 instance (Ubuntu 26.04 LTS)
- Connected via SSH using a key pair

### 2. User hardening
- Created a non-root sudo user (`swayam`) instead of using the default `ubuntu`/root user
- Copied SSH key access to the new user via `rsync`
- Disabled root SSH login (`PermitRootLogin no`) via an override config in 
  `/etc/ssh/sshd_config.d/99-hardening.conf`
- Confirmed `PasswordAuthentication no` was already enforced (key-only auth)

### 3. Firewall (UFW)
- Enabled UFW with default-deny incoming policy
- Explicitly allowed only SSH (22) and HTTP (80)
- Verified via `ufw status verbose`

### 4. Web server
- Installed and ran Nginx
- Replaced default page with a custom HTML page
- Verified via browser and `curl`

### 5. Observability basics
- Reviewed service logs via `journalctl -u nginx`
- Reviewed access/error logs at `/var/log/nginx/`
- Checked running processes (`ps aux`), resource usage (`free -h`, `df -h`), 
  and listening ports (`ss -tulpn`)

## Problems hit & how I solved them
- SSH key permission errors when switching between Windows/WSL and native Linux 
  — resolved by moving fully to native Linux and using `chmod 400` directly
- Nginx unreachable from browser despite AWS Security Group and UFW both being 
  correctly configured — turned out to be a browser-specific HTTPS redirect issue, 
  confirmed by testing with `curl` from the local machine first

## Commands reference
(full list of commands used, for future reference)


#Day 1-2 — Launch & First SSH Access
<!--chmod 400 project-1.pem
ssh -i project-1.pem ubuntu@<public-ip>
whoami
hostname
uname -a
-->

#Day 1-2 — Exploration (system info, processes, resources)
<!--
cat /etc/os-release
lsb_release -a
ps aux
top
free -h
df -h
nproc
ls -la /
ls -la /home/ubuntu
ls -la /etc | head -20
ip a
curl ifconfig.me
history
-->

#Day 3 — Non-root User & SSH Hardening
<!-- sudo adduser swayam
sudo usermod -aG sudo swayam
sudo rsync --archive --chown=swayam:swayam ~/.ssh /home/swayam
ssh -i project-1.pem swayam@<public-ip>
whoami
sudo whoami
-->

Checking SSH config location/settings:
<!-- 
sudo nano /etc/ssh/sshd_config
ls /etc/ssh/sshd_config.d/
cat /etc/ssh/sshd_config.d/60-cloudimg-settings.conf
sudo sshd -T | grep permitrootlogin
-->

Adding explicit hardening override (/etc/ssh/sshd_config.d/99-hardening.conf):
PermitRootLogin no

<!-- 
sudo systemctl restart ssh
sudo sshd -T | grep permitrootlogin
-->


#Day 4 — Firewall (UFW)
<!-- 
sudo ufw status
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw enable
sudo ufw status verbose
-->


#Day 5 — Nginx Install & Custom Page

<!-- 
sudo apt update
sudo apt install nginx -y
sudo systemctl status nginx
sudo nano /var/www/html/index.html
-->

# Verification
curl localhost
curl ifconfig.me

# From local laptop (not the server)
curl http://<public-ip>


#Day 6 — Logs, Processes, Resource Awareness
<!-- sudo journalctl -u nginx --since "1 hour ago"
sudo journalctl -u nginx -p err
sudo tail -20 /var/log/nginx/access.log
sudo tail -20 /var/log/nginx/error.log
ps aux | grep nginx
free -h
df -h
sudo ss -tulpn | grep nginx
-->


#Native Linux Migration (mid-week troubleshooting)
<!-- ls /media/$USER/
ls -la ~/Desktop
chmod 400 ~/Desktop/project-1.pem
ssh -i ~/Desktop/project-1.pem swayam@<public-ip>
-->


# Week - 2 Git/Github Foundation and Application Building


# Expense Tracker

A simple Flask-based expense tracker that lets you add and delete expenses, 
with automatic total calculation. Built as part of a 4-month project-based 
DevOps learning roadmap — this app serves as the base application that gets 
containerized, deployed via CI/CD, and monitored throughout the project.

## Features
- Add an expense (description, amount, category, date auto-recorded)
- View all expenses in a table with a running total
- Delete individual expenses
- Data persisted using SQLite

## Tech stack
- Python 3 / Flask
- SQLite (file-based database)
- Jinja2 templating (built into Flask)

## Running locally

### Prerequisites
- Python 3 installed
- `python3-venv` package (Debian/Ubuntu: `sudo apt install python3-venv`)

### Setup
\`\`\`bash
git clone https://github.com/SwayamP-24/expense-tracker.git
cd expense-tracker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
\`\`\`

Visit `http://localhost:5000` in your browser.

## Project structure
\`\`\`
expense-tracker/
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # Main page template
├── expenses.db           # SQLite database (auto-created, git-ignored)
└── .gitignore
\`\`\`

## Git workflow practiced
This project was built using a real feature-branch workflow rather than 
committing directly to `main`:
- New features developed on separate branches (e.g., `feature/delete-expense`)
- Changes merged via Pull Requests on GitHub
- Deliberately created and resolved a real merge conflict between two 
  branches editing the same line, to practice conflict resolution properly

## Known issues / notes
- Minor layout/styling isn't polished — functionality was prioritized over 
  UI for this stage of the project
- No authentication/multi-user support (single-user local tool for now)

## What's next
This app will be containerized with Docker (Week 3), deployed via an 
automated CI/CD pipeline (Month 2), and later run on Kubernetes with 
monitoring and logging (Month 3) as part of the broader DevOps roadmap.

## Running with Docker

### Build and run manually
\`\`\`bash
docker build -t expense-tracker .
docker run -d -p 5000:5000 --name expense-tracker-app expense-tracker
\`\`\`

### Or run with Docker Compose (recommended — includes persistent storage)
\`\`\`bash
docker compose up -d --build
\`\`\`
Data persists across container restarts via a mounted volume (`./data`).

### Image on Docker Hub
\`\`\`bash
docker pull your-dockerhub-username/expense-tracker:v1
\`\`\`
