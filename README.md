# ACA Rocks Deployment Demo

This repository demonstrates rapid Azure Container Apps deployment using `az containerapp up` with automated ACR image builds. The script creates a new timestamped environment and app with dual timers to measure end-to-end vs ACA-specific provisioning time.


## Minimal Command

```powershell
az containerapp up `
    --name $AppName `
    --source .
```
## Specify location in your Azure environment

```powershell
az containerapp up `
    --name $AppName `
    --resource-group $ResourceGroup `
    --source .

```

## Usage

Run `.\deploy-aca-rocks.ps1` to build, push, and deploy a new container app with a fresh environment. The script outputs two timers: total deployment time and ACA resource creation time (excluding ACR build).

