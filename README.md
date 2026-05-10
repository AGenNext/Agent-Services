# AI Services Platform

A comprehensive multi-provider AI services platform that integrates with multiple AI backends.

## Supported Providers

- **OpenAI** - GPT models
- **Anthropic** - Claude models
- **Google** - Gemini models
- **AWS Bedrock** - Amazon Bedrock AgentCore
- **Azure AI Foundry** - Microsoft Azure AI
- **Ollama** - Local models
- **OpenRouter** - Unified API for 500+ models
- **IBM Watson** - Watson AI models
- **Salesforce Einstein** - Einstein AI
- **Mistral AI** - Mistral models

## Features

- Multi-provider LLM access
- Agent orchestration
- Document parsing (LlamaParse integration)
- RAG capabilities
- Visual workflow builder (Sim Studio compatible)
- Tool integration

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run the server
python -m app.main
```

## Architecture

```
services/
├── providers/       # LLM provider integrations
├── agents/       # Agent orchestration
├── rag/         # RAG functionality
├── parsing/      # Document parsing
└── ui/          # Web interface
```

## License

Apache 2.0