# HYBRID ROUTER DEMO - CHEAT SHEET

## PRE-DEMO SETUP (15 minutes before)

```bash
# 1. Run system check
python3 test_setup.py

# 2. Clear any old sessions
rm -rf ~/.streamlit/

# 3. Start Ollama (if not running)
systemctl status ollama

# 4. Pull model (if needed)
ollama pull deepseek-r1:7b

# 5. Start demo
streamlit run hybrid_router_demo.py
```

## DEMO FLOW (15 minutes)

### 1. INTRO (2 min)
**Say:** "Most consultants push expensive APIs. I built something smarter."

### 2. SIMPLE QUERY (3 min)
**Type:** "What is HIPAA?"
**Show:**
- Score: 0.2
- Route: LOCAL
- Cost: $0.00
- Speed: 1-2 sec

**Say:** "Simple question. Answered locally. Zero cost. Data stayed here."

### 3. COMPLEX QUERY (5 min)
**Type:** "Analyze the legal implications of using AI for patient diagnosis in Hawaii, considering HIPAA compliance, malpractice liability, and state regulations."

**Show:**
- Score: 0.75
- Route: CLOUD
- Cost: $0.003
- Quality: High

**Say:** "Complex legal analysis. System knew to use Claude. Cost: one-third of a penny."

### 4. THE NUMBERS (3 min)
**Point to sidebar:**
- 80% local (free)
- 20% cloud (cheap)
- Savings: 88%

**Say:** "1,000 queries per month:
- Hybrid: $5-10
- All cloud: $50-100
- **You save $500+ per year**"

### 5. PRIVACY WIN (2 min)
**Say:** "Local queries = your data NEVER leaves. Perfect for HIPAA and attorney-client privilege."

## KEY TALKING POINTS

### When to emphasize LOCAL:
- ✅ "80% of business queries are simple"
- ✅ "Zero latency - instant responses"
- ✅ "Complete data privacy"
- ✅ "No per-query costs"
- ✅ "Works offline"

### When to emphasize HYBRID:
- ✅ "Best of both worlds"
- ✅ "Smart system chooses for you"
- ✅ "Fallback for truly complex tasks"
- ✅ "70-80% cost savings vs all-cloud"

### When to emphasize COMPLIANCE:
- ✅ "HIPAA compliant by design"
- ✅ "Attorney-client privilege protected"
- ✅ "No training on your data"
- ✅ "Full audit trail"
- ✅ "Data sovereignty"

## OBJECTION HANDLING

### "Can local models handle our needs?"
**Say:** "Let me show you. Give me your hardest question."
**Do:** Run it on local, show quality. If inadequate, say "This is exactly when we route to cloud. Smart system, not rigid."

### "What if local gives wrong answer?"
**Say:** "Two safeguards: (1) Complexity scoring catches hard queries, (2) You can force cloud anytime."
**Do:** Show force cloud button.

### "Isn't setup complicated?"
**Say:** "I handle everything. 2-week deployment, fully managed. You just use it."

### "What about updates?"
**Say:** "Models update regularly. I manage that as part of ongoing support - $1-2K/month includes updates, monitoring, optimization."

## PRICING CLOSE

### POC (Proof of Concept)
**Price:** $5,000-8,000
**Deliverable:** Working demo with your data
**Timeline:** 2 weeks

### Full Implementation
**Price:** $10,000-25,000
**Deliverable:** Production system
**Timeline:** 4-6 weeks
**Includes:** Training, documentation, compliance docs

### Ongoing Support
**Price:** $1,000-2,000/month
**Includes:** Updates, monitoring, optimization, support

### ROI Pitch
**Say:** "$15K investment. Save $500-1,000/year on API costs. Payback in 18 months. After that: pure savings + better privacy."

## TECHNICAL QUESTIONS

### "What models do you use?"
**Local:** DeepSeek-R1 7B (MIT license, O1-level reasoning)
**Cloud:** Claude Sonnet 4 or GPT-4 (your choice)

### "How fast is local?"
**Speed:** 30-50 tokens/second (faster than API calls)
**Latency:** 1-2 seconds typical

### "What about my specific use case?"
**Say:** "Let's test it right now. Give me 3 example queries from your business."
**Do:** Run them through demo, show routing decisions.

### "Can we customize?"
**Say:** "Absolutely. Complexity threshold, model choice, routing rules - all customizable."

### "What about training on our data?"
**Say:** "We can fine-tune the local model on your documents. Keeps that knowledge private, never in cloud."

## TROUBLESHOOTING (During Demo)

### Demo freezes
**Fix:** Ctrl+C, restart streamlit
**Say:** "Let me restart that real quick."

### Model not found
**Fix:** Open terminal, `ollama pull deepseek-r1:7b`
**Say:** "Downloading model real quick, 2 minutes."

### API key error
**Fix:** Demo local only
**Say:** "Let's focus on the local capabilities - that's the main value anyway."

### Slow response
**Say:** "First query always slower - loading model into memory. Watch the next one."

## NEXT STEPS (End of Demo)

1. **Schedule Discovery Call** - 1 hour, understand their needs
2. **Provide written proposal** - Custom scope and pricing
3. **Build custom POC** - 2 weeks with their data
4. **Final presentation** - Show working system
5. **Implementation** - 4-6 weeks to production

## POST-DEMO FOLLOW-UP

**Within 24 hours:**
- Send thank you email
- Attach proposal PDF
- Include demo recording (if recorded)
- Include this cheat sheet

**Within 1 week:**
- Follow-up call
- Answer any technical questions
- Schedule next meeting

## CONTACT INFO TO SHARE

**Reno Provine**
LeniLani Consulting
📧 reno@lenilani.com
📱 808-XXX-XXXX
🌐 lenilani.com

**Specialties:**
- Local LLM deployment
- HIPAA/GDPR compliance
- Hybrid AI architectures
- Cost optimization
- Hawaii businesses

---

## CONFIDENCE BOOSTERS (Read before demo)

✅ Your setup is REAL (not vaporware)
✅ Your hardware runs production workloads
✅ You have 20+ years business experience
✅ You understand compliance (pentesting background)
✅ You're local (Hawaii businesses trust local)
✅ Your pricing is fair and transparent
✅ You can deliver what you promise

**You got this!** 🤙
