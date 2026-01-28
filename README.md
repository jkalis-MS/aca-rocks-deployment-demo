# ACA Rocks Deployment Demo

This repository demonstrates rapid Azure Container Apps deployment using `az containerapp up` with automated ACR image builds. The script creates a new timestamped environment and app with dual timers to measure end-to-end vs ACA-specific provisioning time.

## Key Command

```powershell
az containerapp up `
    --name $AppName `
    --resource-group $ResourceGroup `
    --location $Location `
    --environment $EnvName `
    --image $ImageName `
    --target-port 8080 `
    --ingress external `
    --registry-server $AcrLoginServer `
    --registry-username $AcrCreds.username `
    --registry-password $AcrCreds.password `
    --logs-workspace-id $LogAnalyticsId
```

## Usage

Run `.\deploy-aca-rocks.ps1` to build, push, and deploy a new container app with a fresh environment. The script outputs two timers: total deployment time and ACA resource creation time (excluding ACR build).

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `AcrName` | `academos` | Azure Container Registry name for storing images |
| `ResourceGroup` | `rg-mcaps-feb26-demos` | Azure resource group for all resources |
| `Location` | `westus` | Azure region for deployment |
| `LogAnalyticsWorkspace` | `workspace-rgmcapsfeb26demoslbgR` | Shared Log Analytics workspace for monitoring |
