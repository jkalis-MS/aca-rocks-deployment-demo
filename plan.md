 # Azure Container Apps: Fast Deployment Challenge

**Objective**: Deploy and run a working application in Azure Container Apps (ACA) as fast as possible - from resource creation to seeing "ACA ROCKS!" output in the console.

**Date**: January 28, 2026  
**Status**: Specification & Planning Phase

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Sample Applications](#sample-applications)
3. [Deployment Methods](#deployment-methods)
4. [Comparison Matrix](#comparison-matrix)
5. [Validation Methodology](#validation-methodology)
6. [Implementation Checklist](#implementation-checklist)

---

## Executive Summary

Deploy Python container to Azure Container Apps and view "ACA ROCKS!" output in portal console.

**Deployment Method**: Azure CLI with `az containerapp up`

**Steps**:
1. Build and push Python image to ACR
2. Deploy with `az containerapp up`
3. View output in portal console

**Expected Time**: 60-90 seconds (after ACR pre-created)

---

## Sample Applications

### Python "ACA ROCKS!" App

**Directory Structure**:
```
python-aca-rocks/
├── Dockerfile
└── app.py
```

**Dockerfile**:
```dockerfile
FROM python:3.12-alpine

WORKDIR /app

COPY app.py .

EXPOSE 8080

CMD ["python", "app.py"]
```

**app.py**:
```python
import http.server
import socketserver
from datetime import datetime

PORT = 8080

ascii_art = """
   ___    ______ ___       ____   ____   ______ __ __ _____ __
  /   |  / ____//   |     / __ \\ / __ \\ / ____// //_// ___// /
 / /| | / /    / /| |    / /_/ // / / // /    / ,<   \\__ \\/ / 
/ ___ |/ /___ / ___ |   / _, _// /_/ // /___ / /| | ___/ /_/  
/_/  |_|\\____//_/  |_|  /_/ |_| \\____/ \\____//_/ |_|/____(_)   
"""

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = f"""
        <html>
        <head><title>ACA ROCKS!</title></head>
        <body style="background-color: #0078d4; color: white; font-family: 'Courier New', monospace; padding: 40px;">
            <h1>Azure Container Apps Deployment</h1>
            <pre style="font-size: 12px; background-color: #001429; padding: 20px; border-radius: 8px;">
{ascii_art}
            </pre>
            <p style="font-size: 18px;">Deployment Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p style="font-size: 16px;">Container Started Successfully! 🎉</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode())
        
        # Print to console (visible in Azure Portal logs)
        print(ascii_art)
        print(f"Request received at {datetime.now()}")
        print("ACA ROCKS! 🚀")

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Server starting on port {PORT}")
    print(ascii_art)
    print("ACA ROCKS! Container is running! 🎉")
    httpd.serve_forever()
```

**Expected Image Size**: ~55 MB  
**Startup Time**: ~2 seconds

---

## Deployment Method: Azure CLI

**Target Time**: ⚡ **60-90 seconds**

### Prerequisites
- Azure CLI installed
- ACR pre-created
- Authenticated: `az login`

### Complete Deployment Script

**deploy-aca-rocks.ps1**:
```powershell
param(
    [string]$AcrName = "academos",
    [string]$ResourceGroup = "rg-mcaps-feb26-demos",
    [string]$Location = "westus"
)

$Timestamp = Get-Date -Format "MMdd-HHmmss"
$AppName = "aca-rocks-$Timestamp"
$ImageName = "$AcrName.azurecr.io/aca-rocks:$Timestamp"

Write-Host "`n⏱️  Starting deployment at $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Cyan
$StartTime = Get-Date

# Step 1: Build and push to ACR
Write-Host "`n📦 Step 1: Building and pushing image to ACR..." -ForegroundColor Yellow
az acr build `
    --registry $AcrName `
    --image "aca-rocks:$Timestamp" `
    --image "aca-rocks:latest" `
    --file Dockerfile `
    .
Write-Host "✅ Image pushed to ACR" -ForegroundColor Green

# Step 2: Deploy with containerapp up
Write-Host "`n🚀 Step 2: Deploying with 'az containerapp up'..." -ForegroundColor Yellow
az containerapp up `
    --name $AppName `
    --resource-group $ResourceGroup `
    --location $Location `
    --image $ImageName `
    --target-port 8080 `
    --ingress external `
    --registry-server "$AcrName.azurecr.io"

$EndTime = Get-Date
$Duration = ($EndTime - $StartTime).TotalSeconds

Write-Host "`n" + ("=" * 60) -ForegroundColor Green
Write-Host "✅ DEPLOYED in $([math]::Round($Duration, 2)) seconds" -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Green

$Fqdn = az containerapp show `
    --name $AppName `
    --resource-group $ResourceGroup `
    --query properties.configuration.ingress.fqdn `
    -o tsv

Write-Host "`n🎉 App URL: https://$Fqdn" -ForegroundColor White
Write-Host "`n📊 Step 3: View 'ACA ROCKS!' in portal:" -ForegroundColor Cyan
Write-Host "   portal.azure.com → $AppName → Console" -ForegroundColor White
Write-Host "   Visit URL above to trigger output`n" -ForegroundColor White
```

### Time Breakdown

| Step | Time | 
|------|------|
| Build + push to ACR | 20-30s |
| Deploy with `containerapp up` | 35-55s |
| **Total** | **60-90s** |

### Validation
- [ ] Image in ACR
- [ ] App running (<90s total)
- [ ] "ACA ROCKS!" in portal console
- [ ] App accessible at URL

---

## Implementation Checklist

### Pre-Deployment
- [ ] Create ACR: `az acr create --name myacr --resource-group rg --sku Basic`
- [ ] Create resource group: `az group create --name aca-rocks-rg --location eastus`
- [ ] Create Python app (app.py, Dockerfile)

### Deployment
- [ ] Run: `.\deploy-aca-rocks.ps1 -AcrName "myacr"`
- [ ] Record deployment time
- [ ] Open portal → Container App → Console
- [ ] Visit app URL
- [ ] Verify "ACA ROCKS!" in console

---

## Troubleshooting

**ACR authentication fails**:
```powershell
az acr login --name myacr
```

**Image build fails**:
- Verify Dockerfile in current directory
- Check ACR name spelling

**Console output not visible**:
- Visit app URL to trigger request
- Wait 30s for logs to appear
- Use "Log stream" if "Console" empty

---

**Document Version**: 2.1  
**Last Updated**: January 28, 2026  
**Status**: Streamlined for ACR + containerapp up
