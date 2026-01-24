# Azure Deployment Guide

## Prerequisites
- Azure Account (Free tier works)
- Azure CLI installed
- GitHub repository with your challenges

## Step 1: Create Azure Web Apps (One for each challenge)

```bash
# Login to Azure
az login

# Create a resource group
az group create --name ctf-challenges-rg --location eastus

# Create App Service plan (Free tier)
az appservice plan create \
  --name ctf-plan \
  --resource-group ctf-challenges-rg \
  --sku F1 \
  --is-linux

# Create Web Apps for each challenge
az webapp create \
  --name challenge1-paysecure \
  --resource-group ctf-challenges-rg \
  --plan ctf-plan \
  --runtime "PYTHON:3.11"

az webapp create \
  --name challenge2-medportal \
  --resource-group ctf-challenges-rg \
  --plan ctf-plan \
  --runtime "PYTHON:3.11"

az webapp create \
  --name challenge3-techcorp \
  --resource-group ctf-challenges-rg \
  --plan ctf-plan \
  --runtime "PYTHON:3.11"
```

## Step 2: Get Publish Profiles

```bash
# Download publish profiles for each app
az webapp deployment list-publishing-profiles \
  --name challenge1-paysecure \
  --resource-group ctf-challenges-rg \
  --xml > challenge1.publishsettings

az webapp deployment list-publishing-profiles \
  --name challenge2-medportal \
  --resource-group ctf-challenges-rg \
  --xml > challenge2.publishsettings

az webapp deployment list-publishing-profiles \
  --name challenge3-techcorp \
  --resource-group ctf-challenges-rg \
  --xml > challenge3.publishsettings
```

## Step 3: Add GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:

1. **AZURE_WEBAPP_NAME_CHALLENGE1**: `challenge1-paysecure`
2. **AZURE_WEBAPP_PUBLISH_PROFILE_CHALLENGE1**: (Content of challenge1.publishsettings)

3. **AZURE_WEBAPP_NAME_CHALLENGE2**: `challenge2-medportal`
4. **AZURE_WEBAPP_PUBLISH_PROFILE_CHALLENGE2**: (Content of challenge2.publishsettings)

5. **AZURE_WEBAPP_NAME_CHALLENGE3**: `challenge3-techcorp`
6. **AZURE_WEBAPP_PUBLISH_PROFILE_CHALLENGE3**: (Content of challenge3.publishsettings)

## Step 4: Configure Startup Commands

For each web app, set the startup command:

```bash
# Challenge 1
az webapp config set \
  --name challenge1-paysecure \
  --resource-group ctf-challenges-rg \
  --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app"

# Challenge 2
az webapp config set \
  --name challenge2-medportal \
  --resource-group ctf-challenges-rg \
  --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app"

# Challenge 3
az webapp config set \
  --name challenge3-techcorp \
  --resource-group ctf-challenges-rg \
  --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app"
```

## Step 5: Update requirements.txt

Add gunicorn to each challenge's requirements.txt:

```bash
# Add this line to requirements.txt in each challenge
gunicorn==21.2.0
```

## Step 6: Push to GitHub

Once you push to `main` branch, GitHub Actions will automatically deploy all challenges!

```bash
git add .
git commit -m "Add Azure deployment workflow"
git push origin main
```

## Access Your Challenges

After deployment, access your challenges at:
- Challenge 1: https://challenge1-paysecure.azurewebsites.net
- Challenge 2: https://challenge2-medportal.azurewebsites.net
- Challenge 3: https://challenge3-techcorp.azurewebsites.net

## Alternative: Docker Container Deployment

If you prefer using Docker, use Azure Container Instances:

```bash
# Build and push Docker images
docker build -t challenge1 ./web/Challenge1-ClawCTF-BruteForce
docker tag challenge1 yourregistry.azurecr.io/challenge1
docker push yourregistry.azurecr.io/challenge1

# Create container instance
az container create \
  --name challenge1-container \
  --resource-group ctf-challenges-rg \
  --image yourregistry.azurecr.io/challenge1 \
  --dns-name-label challenge1-ctf \
  --ports 5000
```

## Cost Optimization

- **Free Tier**: F1 tier is free but limited (60 CPU minutes/day)
- **Basic Tier**: B1 tier costs ~$13/month per app
- **Shared Resources**: All 3 apps can use the same App Service Plan

## Monitoring

View logs:
```bash
az webapp log tail \
  --name challenge1-paysecure \
  --resource-group ctf-challenges-rg
```

## Troubleshooting

1. **App not starting**: Check logs with `az webapp log tail`
2. **502 errors**: Verify startup command is correct
3. **Dependencies failing**: Ensure requirements.txt includes all packages
4. **Port issues**: Azure expects apps to listen on port 8000 or use the PORT environment variable
