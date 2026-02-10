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

---

## 🐳 How to Create a Dockerfile (From Easiest to Hardest)

New to containers? Here are **many ways** to create a Dockerfile, sorted from simplest to most advanced. Many options **don't require Docker Desktop** at all.

### 1. 🤖 GitHub Copilot in VS Code
**Difficulty:** ⭐ | **Docker Desktop Required**

Ask Copilot Chat to generate a Dockerfile for your project:

> *"Generate a Dockerfile for this Python app that runs on port 8080"*

Copilot analyzes your project structure and generates an optimized Dockerfile. You can iterate with follow-up prompts like:

> *"Make it use Alpine for a smaller image"*
> *"Add a health check"*

### 2. 📦 VS Code Extension "Microsoft Containers"
**Difficulty:** ⭐⭐ | **Docker Desktop Required**

Install the [Docker extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker) (`ms-azuretools.vscode-docker`), then:

1. Open Command Palette → **Docker: Add Docker Files to Workspace**
2. Select your app platform (Python, Node.js, .NET, Java, etc.)
3. Answer a few prompts (port, etc.)
4. A Dockerfile and `.dockerignore` are generated automatically

> **Tip:** You don't need Docker Desktop installed to *author* Dockerfiles — only to *build* locally. Use ACR to build in the cloud instead (see option 6).

### 3. 📝 Use a Template from Docker Hub / GitHub
**Difficulty:** ⭐⭐ | **Docker Desktop Required**

Start from a proven template:

- [Docker Official Images](https://hub.docker.com/search?q=&type=image&image_filter=official) — find your language's base image
- [Awesome Docker](https://github.com/veggiemonk/awesome-docker) — community-curated Dockerfile examples
- Search GitHub for `Dockerfile language:<your-language>`

Copy, paste, and modify to fit your app.



