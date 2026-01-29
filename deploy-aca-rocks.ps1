param(
    [string]$AcrName = "academos",
    [string]$ResourceGroup = "rg-mcaps-feb26-demos",
    [string]$Location = "westus",
    [string]$LogAnalyticsWorkspace = "workspace-rgmcapsfeb26demoslbgR"
)

$Timestamp = Get-Date -Format "MMdd-HHmmss"
$AppName = "aca-rocks-$Timestamp"
$EnvName = "aca-env-$Timestamp"

# Get the actual ACR login server
$AcrLoginServer = az acr show --name $AcrName --query loginServer -o tsv
$ImageName = "$AcrLoginServer/aca-rocks:$Timestamp"

Write-Host "`n⏱️  Starting deployment at $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Cyan
$StartTime = Get-Date

# Step 1: Build and push to ACR
Write-Host "`n📦 Step 1: Building and pushing image to ACR..." -ForegroundColor Yellow
az acr build `
    --registry $AcrName `
    --image "aca-rocks:$Timestamp" `
    --image "aca-rocks:latest" `
    --file Dockerfile `
    --output none `
    .
Write-Host "✅ Image pushed to ACR" -ForegroundColor Green

# Start Timer 2 for ACA resource creation
Write-Host "`n⏱️  Starting ACA resource creation timer..." -ForegroundColor Cyan
$AcaStartTime = Get-Date

# Get the Log Analytics workspace ID
$LogAnalyticsId = az monitor log-analytics workspace show `
    --resource-group $ResourceGroup `
    --workspace-name $LogAnalyticsWorkspace `
    --query customerId `
    -o tsv

# Get ACR credentials
$AcrCreds = az acr credential show --name $AcrName --query "{username:username, password:passwords[0].value}" -o json | ConvertFrom-Json

# Step 2: Deploy with containerapp up (will create new environment)
Write-Host "`n🚀 Step 2: Deploying with 'az containerapp up'..." -ForegroundColor Yellow
$DeployOutput = az containerapp up `
    --name $AppName `
    --resource-group $ResourceGroup `
    --location $Location `
    --image $ImageName `
    --target-port 8080 `
    --ingress external `
    --registry-server $AcrLoginServer `
    --registry-username $AcrCreds.username `
    --registry-password $AcrCreds.password `
    --logs-workspace-id $LogAnalyticsId 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Container app deployed" -ForegroundColor Green
} else {
    Write-Host "❌ Deployment failed" -ForegroundColor Red
    Write-Host $DeployOutput
    exit 1
}

$EndTime = Get-Date
$TotalDuration = ($EndTime - $StartTime).TotalSeconds
$AcaDuration = ($EndTime - $AcaStartTime).TotalSeconds

Write-Host "`n" + ("=" * 60) -ForegroundColor Green
Write-Host "✅ DEPLOYED" -ForegroundColor Green
Write-Host "   Timer 1 (End-to-End): $([math]::Round($TotalDuration, 2)) seconds" -ForegroundColor Green
Write-Host "   Timer 2 (ACA Creation): $([math]::Round($AcaDuration, 2)) seconds" -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Green

$Fqdn = az containerapp show `
    --name $AppName `
    --resource-group $ResourceGroup `
    --query properties.configuration.ingress.fqdn `
    -o tsv

Write-Host "`n🎉 App URL: https://$Fqdn" -ForegroundColor White
Write-Host "`n📊 Step 3: View 'ACA ROCKS!' in portal:" -ForegroundColor Cyan
Write-Host "   portal.azure.com → $AppName → Console" -ForegroundColor White
