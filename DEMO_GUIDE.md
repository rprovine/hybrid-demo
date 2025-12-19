# LeniLani AI Hybrid Router Demo

## 🎯 Purpose
This demo shows clients the **80/20 split**: Local models for 80% of queries (fast, free, private) and Cloud APIs for the complex 20% (powerful but paid).

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Install required packages
pip install streamlit ollama anthropic openai python-dotenv --break-system-packages

# Or use a virtual environment
python3 -m venv ~/venvs/hybrid-demo
source ~/venvs/hybrid-demo/bin/activate
pip install streamlit ollama anthropic openai python-dotenv
```

### 2. Pull Required Models
```bash
# Pull the local model used in the demo
ollama pull deepseek-r1:7b

# Verify it's working
ollama run deepseek-r1:7b "Hello, how are you?"
```

### 3. Set Up API Keys (Optional - for cloud comparison)
```bash
# Create .env file
cat > ~/.env << EOF
ANTHROPIC_API_KEY=your_api_key_here
OPENAI_API_KEY=your_api_key_here
EOF

# Or export directly
export ANTHROPIC_API_KEY="your_key"
export OPENAI_API_KEY="your_key"
```

### 4. Run the Demo
```bash
# Start the Streamlit app
streamlit run hybrid_router_demo.py

# It will open in your browser at http://localhost:8501
```

## 📊 Features

### Smart Routing
- **Automatic complexity analysis** - Analyzes query to determine best route
- **Customizable threshold** - Adjust when to route to cloud (default: 0.6)
- **Manual override** - Force local or cloud for testing

### Performance Tracking
- **Real-time metrics** - Latency, tokens/sec, cost
- **Session statistics** - Track local vs cloud usage
- **Cost calculator** - Show savings compared to all-cloud

### Query History
- **Last 10 queries** - Review past decisions
- **Performance comparison** - See which route was faster/cheaper
- **Complexity scores** - Understand routing decisions

## 🎨 Demo Script for Clients

### Opening (2 minutes)
> "Let me show you something interesting. Most consultants will tell you to use ChatGPT or Claude for everything. But that gets expensive fast - $50, $100, even $500 per month.
>
> I've built something smarter: an AI system that knows when to run locally (free, fast, private) and when to use cloud APIs (powerful but paid)."

### Simple Query Demo (3 minutes)
1. **Enter**: "What is HIPAA?"
2. **Show**:
   - Complexity score: ~0.2 (low)
   - Routes to LOCAL
   - Response in 1-2 seconds
   - Cost: $0.00
   - Speed: 30-50 tokens/second

> "See that? Simple question, answered locally in under 2 seconds. No cost. Your data never left this room."

### Complex Query Demo (5 minutes)
1. **Enter**: "Analyze the legal implications of using AI for patient diagnosis in Hawaii, considering HIPAA compliance, malpractice liability, and state regulations. Provide detailed examples and risk mitigation strategies."
2. **Show**:
   - Complexity score: ~0.75 (high)
   - Routes to CLOUD
   - Detailed, nuanced response
   - Cost: ~$0.003 (less than a penny)

> "This one's complex - multiple topics, legal analysis, specific regulations. The system recognized that and used Claude API for better quality. Cost us a third of a penny."

### The Money Shot (3 minutes)
**Point to sidebar statistics:**
- Total queries: 10
- Local: 8 (80%)
- Cloud: 2 (20%)
- Total cost: $0.006
- If all cloud: ~$0.05
- **Savings: 88%**

> "In a real month with 1,000 queries, you're looking at:
> - My hybrid approach: $5-10/month
> - All cloud (what others do): $50-100/month
> - **You save $500-1,000 per year**"

### Privacy Angle (2 minutes)
> "But here's what really matters for healthcare and legal: When we route locally, your data NEVER leaves your infrastructure. No ChatGPT. No Claude. No external servers.
>
> That means:
> - ✅ HIPAA compliant by design
> - ✅ Attorney-client privilege protected
> - ✅ No data training concerns
> - ✅ Instant responses with zero latency"

### Closing (2 minutes)
> "I can deploy this for [Client Name] in 2 weeks:
> 1. Custom model trained on your data
> 2. Smart routing tuned to your needs
> 3. Full integration with your systems
> 4. Compliance documentation included
>
> Investment: $8,000-15,000
> Monthly savings: $50-100
> Payback: 6-12 months
> After that: pure savings and better privacy"

## 🎯 Customization Guide

### Adjust Complexity Threshold
Edit `hybrid_router_demo.py`:
```python
# Line ~95
threshold = 0.6  # Lower = more cloud, Higher = more local
```

### Change Local Model
```python
# Line 12
LOCAL_MODEL = "deepseek-r1:8b"  # or "qwen3:8b", "llama3.3:8b"
```

### Add Custom Complexity Keywords
```python
# Line ~60
complex_keywords = {
    'analyze deeply': 0.3,
    'your custom keyword': 0.2,  # Add your own
}
```

### Modify Sample Queries
```python
# Line ~290
if st.button("📝 Simple: What is HIPAA?"):
    query = "Your custom simple query"

if st.button("🧠 Complex: Analyze..."):
    query = "Your custom complex query"
```

## 📈 Performance Expectations (RTX 4080 16GB)

| Model | Tokens/Sec | Latency | Best For |
|-------|------------|---------|----------|
| deepseek-r1:7b | 30-50 t/s | Low | Production use |
| deepseek-r1:8b | 25-40 t/s | Low | Balanced |
| deepseek-r1:14b | 15-25 t/s | Medium | Complex reasoning |

## 🔧 Troubleshooting

### Model Not Found
```bash
# Pull the model
ollama pull deepseek-r1:7b

# Verify it's available
ollama list
```

### API Keys Not Working
```bash
# Test Anthropic key
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-sonnet-4-20250514","max_tokens":1024,"messages":[{"role":"user","content":"Hello"}]}'

# Test OpenAI key
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o","messages":[{"role":"user","content":"Hello"}]}'
```

### Slow Performance
```bash
# Check GPU usage
nvidia-smi

# Reduce model size if needed
ollama pull deepseek-r1:1.5b  # Smaller, faster
```

### Port Already in Use
```bash
# Kill existing Streamlit
pkill -f streamlit

# Or use different port
streamlit run hybrid_router_demo.py --server.port 8502
```

## 💡 Pro Tips

1. **Run demo queries BEFORE client meeting** - Build up history to show
2. **Clear history at start of demo** - Fresh slate for client
3. **Adjust threshold live** - Show how routing changes
4. **Have backup internet** - Cloud APIs need connectivity
5. **Prepare for "what if" questions**:
   - "What if local is wrong?" → Show force cloud button
   - "What if I need more power?" → Explain hybrid benefits
   - "What about updates?" → Explain model management

## 📞 Support

For issues or questions:
- Email: reno@lenilani.com
- Phone: 808-XXX-XXXX
- Web: lenilani.com

## 🎓 Next Steps After Demo

1. **Discovery Call** ($0) - Understand client needs
2. **Custom POC** ($5,000-8,000) - 2-week build
3. **Full Implementation** ($10,000-25,000) - Production deployment
4. **Ongoing Support** ($1,000-2,000/month) - Maintenance and optimization

---

**Built with ❤️ in Hawaii by LeniLani Consulting**
