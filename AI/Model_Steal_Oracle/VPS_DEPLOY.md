# VPS Deployment Guide (Option C)

This guide shows how to host the **verification server** on a Linux VPS using Docker.

You will end up with a public verifier at:

- `http://<VPS_IP>:5000/verify`

Only the verifier is hosted. **Do not upload the oracle source/binary to the VPS.**

---

## What you need

- A small VPS (Ubuntu 22.04/24.04 recommended)
- SSH access (root or a sudo user)
- This folder on your local machine:
  - `server.py`
  - `requirements.txt`
  - `Dockerfile`
  - `.dockerignore`
  - `docker-compose.yml`

---

## 1) Provision the VPS

Create a VPS and note its public IP, e.g. `203.0.113.10`.

SSH in:

```bash
ssh ubuntu@<VPS_IP>
```

---

## 2) Install Docker

Ubuntu:

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Verify:

```bash
docker version
docker compose version
```

---

## 3) Create a secret seed (important)

On the VPS, generate a long random seed. Example:

```bash
export CTF_SEED="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
```

This seed controls the hidden test set generation. Keep it secret.

To make it persistent across reboots, add it to a root-owned env file.

Create `/opt/model-steal-verifier/.env`:

```bash
sudo mkdir -p /opt/model-steal-verifier
sudo sh -c 'echo "CTF_SEED='$CTF_SEED'" > /opt/model-steal-verifier/.env'
sudo chmod 600 /opt/model-steal-verifier/.env
```

---

## 4) Upload ONLY the verifier files

From your local machine, upload the folder contents (verifier only):

```bash
scp -r ./REVERSE/Model_Steal_Oracle ubuntu@<VPS_IP>:/opt/model-steal-verifier/app
```

Then on the VPS:

```bash
cd /opt/model-steal-verifier/app
```

Make sure `model_oracle.exe` is NOT in this directory. (`.dockerignore` also prevents it from being built into the image.)

---

## 5) Build and run with docker compose

```bash
cd /opt/model-steal-verifier/app

# Load env
set -a
source /opt/model-steal-verifier/.env
set +a

sudo docker compose up -d --build
sudo docker compose ps
```

The verifier should now be live at:

- `http://<VPS_IP>:5000/verify`

---

## 6) Open the port (firewall)

If you use `ufw`:

```bash
sudo ufw allow 5000/tcp
sudo ufw enable
sudo ufw status
```

If your VPS provider uses a cloud firewall, also allow inbound TCP/5000.

---

## 7) Updating the verifier

When you change server code:

```bash
cd /opt/model-steal-verifier/app
sudo docker compose up -d --build
```

---

## 8) What you share to players

- Share only: `model_oracle.exe`
- Share a short description:
  - Takes 5 floats -> prints 0/1
  - Submit predictions to `http://<VPS_IP>:5000/verify`

Do NOT share:
- `server.py`
- test set
- `CTF_SEED`
- Docker files

---

## Troubleshooting

### Can’t reach the verifier
- Check container is running: `sudo docker compose ps`
- Check logs: `sudo docker compose logs -n 100`
- Verify firewall rules: `sudo ufw status`
- Verify provider security group allows TCP/5000

### Want to run behind Nginx / HTTPS
If you want a nicer public URL (and TLS), put Nginx/Caddy in front and proxy to `localhost:5000`.
