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

## Services (Modules)

The platform includes these services:

### Core Services
- **Cost Prediction** (`app/cost_predictor.py`) - Estimate API costs across providers
- **Localization** (`app/localization.py`) - Multi-language and local model support
- **Data Control** (`app/data_control.py`) - Privacy, retention, and audit controls
- **Data Preparation** (`app/data_prep.py`) - Text cleaning, chunking, validation
- **Data Generation** (`app/data_generation.py`) - Synthetic test data
- **AI Use Case ID** (`app/use_case_id.py`) - Identify AI use cases for business
- **ROI Measurement** (`app/roi_measurement.py`) - Calculate AI ROI
- **Agent Evaluation** (`app/agent_eval.py`) - Benchmark agent performance
- **AI Research** (`app/ai_research.py`) - Paper/model/technique library

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run the server
python -m app.main

# Use services
python -c "from app.cost_predictor import estimate_request; print(estimate_request('openai', 'gpt-4o', 1000, 500))"
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