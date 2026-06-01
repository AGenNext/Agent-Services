# Agent Registry

Central registry of all agents in the Agent-Services ecosystem.

---

## Luna - Headlamp AI Pod Manager Agent

**Source:** [headlamp-k8s/plugins/ai-assistant](https://github.com/headlamp-k8s/plugins/tree/main/ai-assistant)

### Overview
Luna is a Kubernetes-focused agent for managing pod deployments with GitOps support.

### AI Provider Integration
| Provider | Status | Notes |
|----------|--------|-------|
| OpenAI | ✅ | `OPENAI_API_KEY` |
| Azure | ✅ | `AZURE_API_KEY`, `AZURE_API_BASE` |
| Anthropic | ✅ | `ANTHROPIC_API_KEY` |
| Ollama | ✅ | Local models support |

### Capabilities
- One-command K3s/K8s deployment
- Multi-provider AI integration via Agent-Services
- MCP server integration (Flux, Prometheus)
- K8s manifest validation
- CI/CD pipeline management

### Configuration
```bash
# Deploy with specific AI provider
AI_PROVIDER=openai bash deploy.sh

# Use Azure
AI_PROVIDER=azure AZURE_API_KEY=xxx bash deploy.sh
```

### Integration Points
```yaml
mcp:
  servers:
    - name: flux
      command: flux-operator-mcp
      env:
        FLUX_PROVIDER: openai  # Uses Agent-Services LLM
    - name: prometheus
      command: prometheus-mcp
      env:
        PROMETHEUS_PROVIDER: azure
```

### Files Reference
```
https://github.com/headlamp-k8s/plugins/tree/main/ai-assistant/
├── agents/headlamp-ai-assistant.md    # Luna agent definition
├── .skills/
│   ├── gitops.md                      # GitOps skill
│   └── semantic-validation.md         # K8s validation
├── deploy.sh                          # One-command deploy
└── src/pod_manager/                   # FastAPI app
```

### Status
- [x] Agent Definition (Luna identity)
- [x] GitOps Skill (Flux, ArgoCD, Helm)
- [x] Semantic Validation Skill
- [x] One-Command Deploy
- [x] E2E Tests (ArgoCD, Terraform)
- [x] CI/CD Pipeline with SBOM

---

*Add new agents above*