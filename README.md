# Hybrid AI Router Demo

A smart AI routing system that automatically directs queries to **local models** (fast, free, private) or **cloud APIs** (powerful, paid) based on query complexity.

Built for client demonstrations by [LeniLani Consulting](https://lenilani.com).

## The 80/20 Principle

- **80% of queries** are simple and can be handled locally at zero cost
- **20% of queries** are complex and benefit from cloud AI capabilities
- **Result:** 70-80% cost savings compared to cloud-only solutions

## Features

- **Smart Routing** - Automatic complexity analysis determines best route
- **Real-time Metrics** - Latency, tokens/sec, and cost tracking
- **Privacy First** - Local queries never leave your infrastructure
- **Cost Calculator** - See savings compared to all-cloud approach
- **Query History** - Review routing decisions and performance

## Quick Start

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/download) installed and running
- NVIDIA GPU with 16GB+ VRAM (recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/hybrid-demo.git
cd hybrid-demo

# Install dependencies
pip install -r requirements.txt

# Pull the local model
ollama pull deepseek-r1:7b

# Set API keys (optional, for cloud comparison)
export ANTHROPIC_API_KEY="your_key_here"
export OPENAI_API_KEY="your_key_here"  # optional
```

### Run the Demo

```bash
# Verify setup
python3 test_setup.py

# Start the app
streamlit run hybrid_router_demo.py
```

Open http://localhost:8501 in your browser.

## Project Structure

```
hybrid-demo/
├── hybrid_router_demo.py   # Main Streamlit application
├── test_setup.py           # System verification script
├── requirements.txt        # Python dependencies
├── DEMO_GUIDE.md          # Comprehensive setup and usage guide
├── DEMO_CHEAT_SHEET.md    # Quick reference for live demos
├── PROPOSAL_TEMPLATE.md   # Post-demo proposal template
└── README.md              # This file
```

## How It Works

### Complexity Analysis

The router analyzes each query for:
- **Length** - Longer queries often indicate complex requests
- **Keywords** - Terms like "analyze", "compare", "evaluate" suggest complexity
- **Question count** - Multiple questions require more processing
- **Request type** - Requests for examples, steps, or detailed explanations

### Routing Decision

```
Score < 0.6  →  LOCAL  (DeepSeek-R1 7B via Ollama)
Score >= 0.6 →  CLOUD  (Claude Sonnet 4 via API)
```

### Example Queries

| Query | Score | Route |
|-------|-------|-------|
| "What is HIPAA?" | 0.2 | LOCAL |
| "Explain machine learning" | 0.3 | LOCAL |
| "Analyze the legal implications of AI in healthcare..." | 0.75 | CLOUD |

## Configuration

### Adjust Complexity Threshold

Edit `hybrid_router_demo.py` line ~95:
```python
threshold = 0.6  # Lower = more cloud, Higher = more local
```

### Change Local Model

```python
LOCAL_MODEL = "deepseek-r1:7b"  # or "qwen3:8b", "llama3.3:8b"
```

## Performance

Tested on NVIDIA RTX 4080 SUPER (16GB VRAM):

| Model | Tokens/Sec | Best For |
|-------|------------|----------|
| deepseek-r1:7b | 30-50 t/s | Production use |
| deepseek-r1:14b | 15-25 t/s | Complex reasoning |

## Use Cases

### Healthcare (HIPAA Compliant)
- Patient data never leaves infrastructure
- Routine queries handled locally
- Complex medical analysis uses cloud

### Legal (Attorney-Client Privilege)
- Client communications stay private
- Case research can use cloud APIs
- Full audit trail

### Financial (PCI-DSS)
- Sensitive data processed locally
- Market analysis uses cloud
- Complete data sovereignty

## Documentation

- **[DEMO_GUIDE.md](DEMO_GUIDE.md)** - Full setup instructions and demo script
- **[DEMO_CHEAT_SHEET.md](DEMO_CHEAT_SHEET.md)** - Quick reference during demos
- **[PROPOSAL_TEMPLATE.md](PROPOSAL_TEMPLATE.md)** - Post-demo client proposal

## Troubleshooting

### Model not found
```bash
ollama pull deepseek-r1:7b
ollama list  # Verify installation
```

### Slow first response
Normal - model loads into GPU memory on first query. Subsequent queries are fast.

### Port already in use
```bash
pkill -f streamlit
streamlit run hybrid_router_demo.py --server.port 8502
```

## License

MIT License - See [LICENSE](LICENSE) for details.

## Contact

**Reno Provine**
LeniLani Consulting
- Email: reno@lenilani.com
- Web: [lenilani.com](https://lenilani.com)

---

Built with love in Hawaii
