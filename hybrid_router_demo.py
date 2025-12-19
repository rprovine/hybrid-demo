"""
LeniLani AI Hybrid Router Demo
Shows clients the 80/20 split: Local models for simple queries, Cloud APIs for complex ones
"""

import streamlit as st
import ollama
import anthropic
import openai
import time
import re
import subprocess
from datetime import datetime

# Cloud Model Configurations
CLOUD_MODELS = {
    "Claude Sonnet 4": {
        "id": "claude-sonnet-4-20250514",
        "provider": "anthropic",
        "description": "Fast & capable. Best for most business tasks, coding, and analysis.",
        "pricing": {"input": 3.00, "output": 15.00},
        "best_for": ["Daily tasks", "Code generation", "Quick analysis", "Cost-effective"]
    },
    "Claude Opus 4": {
        "id": "claude-opus-4-20250514",
        "provider": "anthropic",
        "description": "Most powerful Claude. Best for complex reasoning and research.",
        "pricing": {"input": 15.00, "output": 75.00},
        "best_for": ["Complex analysis", "Research", "Strategic planning", "Nuanced writing"]
    },
    "GPT-4o": {
        "id": "gpt-4o",
        "provider": "openai",
        "description": "OpenAI's flagship. Strong at creative tasks and general knowledge.",
        "pricing": {"input": 2.50, "output": 10.00},
        "best_for": ["Creative writing", "General tasks", "Multimodal", "Wide knowledge"]
    },
    "GPT-4o Mini": {
        "id": "gpt-4o-mini",
        "provider": "openai",
        "description": "Fast & affordable OpenAI model. Good for simpler cloud tasks.",
        "pricing": {"input": 0.15, "output": 0.60},
        "best_for": ["Simple tasks", "High volume", "Budget-friendly", "Quick responses"]
    }
}

# Local model descriptions (matched by name patterns)
LOCAL_MODEL_INFO = {
    "deepseek-r1": {
        "description": "Excellent reasoning model. Great for logic, math, and step-by-step thinking.",
        "best_for": ["Reasoning", "Math", "Logic puzzles", "Code review"]
    },
    "llama3": {
        "description": "Meta's versatile model. Good all-around performance for general tasks.",
        "best_for": ["General tasks", "Conversation", "Summarization", "Q&A"]
    },
    "qwen": {
        "description": "Strong multilingual model. Excellent for coding and technical tasks.",
        "best_for": ["Coding", "Technical docs", "Multilingual", "Analysis"]
    },
    "mistral": {
        "description": "Efficient European model. Fast and capable for its size.",
        "best_for": ["Fast inference", "European languages", "Efficient", "General tasks"]
    },
    "codellama": {
        "description": "Specialized for code. Best choice for programming tasks.",
        "best_for": ["Code generation", "Debugging", "Code explanation", "Programming"]
    },
    "phi": {
        "description": "Microsoft's small but mighty model. Surprisingly capable for its size.",
        "best_for": ["Resource-limited", "Quick tasks", "Edge deployment", "Efficiency"]
    }
}

def get_local_model_info(model_name: str) -> dict:
    """Get description info for a local model based on its name"""
    model_lower = model_name.lower()
    for pattern, info in LOCAL_MODEL_INFO.items():
        if pattern in model_lower:
            return info
    return {
        "description": "Local model running on your hardware. Fast, free, and private.",
        "best_for": ["Privacy", "No API costs", "Fast responses", "Offline capable"]
    }

def get_available_local_models() -> list:
    """Fetch list of models available in Ollama"""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            models = []
            for line in lines:
                if line.strip():
                    model_name = line.split()[0]
                    models.append(model_name)
            return models if models else ["No models found"]
        return ["Error fetching models"]
    except Exception as e:
        return [f"Error: {str(e)}"]

# Pricing lookup (per 1M tokens)
def get_pricing(model_key: str) -> dict:
    """Get pricing for a model"""
    if model_key in CLOUD_MODELS:
        return CLOUD_MODELS[model_key]["pricing"]
    return {"input": 0, "output": 0}  # Local models are free

# Initialize session state
if 'queries' not in st.session_state:
    st.session_state.queries = []
if 'total_cost' not in st.session_state:
    st.session_state.total_cost = {"local": 0, "cloud": 0}

def analyze_query_complexity(query: str) -> dict:
    """
    Analyze query complexity to determine routing
    Returns: {score: float, factors: list, route: str}
    """
    score = 0.0
    factors = []

    # Length analysis
    word_count = len(query.split())
    if word_count > 100:
        score += 0.3
        factors.append(f"Long query ({word_count} words)")
    elif word_count > 50:
        score += 0.15
        factors.append(f"Medium length ({word_count} words)")

    # Complexity keywords
    complex_keywords = {
        'analyze deeply': 0.3,
        'comprehensive analysis': 0.3,
        'compare and contrast': 0.25,
        'detailed explanation': 0.2,
        'critically evaluate': 0.25,
        'strategic planning': 0.2,
        'analyze': 0.15,
        'compare': 0.15,
        'explain': 0.1,
        'evaluate': 0.15,
        'multiple': 0.1,
        'complex': 0.15,
        'various': 0.1
    }

    query_lower = query.lower()
    for keyword, weight in complex_keywords.items():
        if keyword in query_lower:
            score += weight
            factors.append(f"Complex keyword: '{keyword}'")

    # Multiple questions
    question_marks = query.count('?')
    if question_marks > 2:
        score += 0.2
        factors.append(f"Multiple questions ({question_marks})")
    elif question_marks > 1:
        score += 0.1
        factors.append(f"Two questions")

    # Request for examples/steps
    if any(word in query_lower for word in ['step by step', 'examples', 'multiple examples']):
        score += 0.15
        factors.append("Requests examples/steps")

    # Simple indicators (reduce score)
    if any(word in query_lower for word in ['what is', 'who is', 'when did', 'where is']):
        score -= 0.1
        factors.append("Simple question format")

    # Determine route
    threshold = 0.6  # Adjust based on testing
    route = "cloud" if score >= threshold else "local"

    return {
        "score": min(max(score, 0), 1),  # Clamp between 0-1
        "factors": factors,
        "route": route,
        "threshold": threshold
    }

def estimate_tokens(text: str) -> int:
    """Rough token estimation: ~4 chars per token"""
    return len(text) // 4

def calculate_cost(input_tokens: int, output_tokens: int, model: str) -> float:
    """Calculate API cost"""
    pricing = PRICING.get(model, {"input": 0, "output": 0})
    cost = (input_tokens * pricing["input"] / 1_000_000) + \
           (output_tokens * pricing["output"] / 1_000_000)
    return cost

def local_inference(query: str, model: str) -> dict:
    """Run inference on local Ollama model"""
    start_time = time.time()

    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": query}]
        )

        end_time = time.time()
        response_text = response['message']['content']

        return {
            "success": True,
            "response": response_text,
            "model": model,
            "latency": end_time - start_time,
            "tokens_per_sec": estimate_tokens(response_text) / (end_time - start_time),
            "cost": 0.0,
            "input_tokens": estimate_tokens(query),
            "output_tokens": estimate_tokens(response_text)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "model": model
        }

def cloud_inference(query: str, cloud_model_key: str) -> dict:
    """Run inference on cloud API"""
    start_time = time.time()

    model_config = CLOUD_MODELS.get(cloud_model_key)
    if not model_config:
        return {"success": False, "error": f"Unknown cloud model: {cloud_model_key}", "model": cloud_model_key}

    model_id = model_config["id"]
    provider = model_config["provider"]
    pricing = model_config["pricing"]

    try:
        if provider == "anthropic":
            client = anthropic.Anthropic()
            response = client.messages.create(
                model=model_id,
                max_tokens=2000,
                messages=[{"role": "user", "content": query}]
            )
            response_text = response.content[0].text
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens

        else:  # OpenAI
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": query}]
            )
            response_text = response.choices[0].message.content
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens

        end_time = time.time()

        # Calculate cost
        cost = (input_tokens * pricing["input"] / 1_000_000) + \
               (output_tokens * pricing["output"] / 1_000_000)

        return {
            "success": True,
            "response": response_text,
            "model": f"{cloud_model_key} ({model_id})",
            "latency": end_time - start_time,
            "cost": cost,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "model": cloud_model_key
        }

# Streamlit UI
st.set_page_config(
    page_title="LeniLani AI Hybrid Router",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .local-route {
        color: #28a745;
        font-weight: bold;
    }
    .cloud-route {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🤖 LeniLani AI Hybrid Router")
st.markdown("### Smart AI that knows when to run local vs. cloud")

# Model Guide
with st.expander("📚 **Model Selection Guide** - When to use each model"):
    st.markdown("""
    ### 🏠 Local Models (Free, Private, Fast)
    Run on your hardware. Data never leaves your machine. Best for:

    | Model | Best For | Speed |
    |-------|----------|-------|
    | **DeepSeek-R1** | Reasoning, math, logic, step-by-step thinking | Fast |
    | **Qwen** | Coding, technical docs, multilingual | Fast |
    | **Llama 3** | General tasks, conversation, Q&A | Fast |
    | **CodeLlama** | Programming, debugging, code review | Fast |
    | **Mistral** | Efficient general tasks, European languages | Very Fast |

    ### ☁️ Cloud Models (Powerful, Paid)
    API-based. Use for complex tasks that need maximum capability:

    | Model | Best For | Cost |
    |-------|----------|------|
    | **Claude Sonnet 4** | Daily tasks, coding, quick analysis | $$ |
    | **Claude Opus 4** | Complex reasoning, research, strategic planning | $$$$ |
    | **GPT-4o** | Creative writing, general knowledge, multimodal | $$ |
    | **GPT-4o Mini** | Simple cloud tasks, high volume, budget-friendly | $ |

    ### 💡 Quick Decision Guide
    - **Simple question?** → Local model (free!)
    - **Need deep analysis?** → Claude Opus 4
    - **Coding task?** → DeepSeek-R1 or Qwen locally, or Claude Sonnet 4
    - **Creative writing?** → GPT-4o
    - **Budget-conscious?** → Local first, GPT-4o Mini for cloud
    - **Privacy critical?** → Always local
    """)

st.markdown("---")

# Sidebar - Configuration & Stats
with st.sidebar:
    st.header("⚙️ Model Selection")

    # Get available local models
    available_local_models = get_available_local_models()

    # Local Model Selection
    st.markdown("**🏠 Local Model**")
    selected_local_model = st.selectbox(
        "Choose local model:",
        available_local_models,
        index=0 if available_local_models else 0,
        key="local_model_select"
    )

    # Show local model info
    if selected_local_model and not selected_local_model.startswith("Error"):
        local_info = get_local_model_info(selected_local_model)
        st.caption(f"_{local_info['description']}_")
        with st.expander("Best for"):
            for use in local_info['best_for']:
                st.markdown(f"• {use}")

    st.markdown("---")

    # Cloud Model Selection
    st.markdown("**☁️ Cloud Model**")
    cloud_model_options = list(CLOUD_MODELS.keys())
    selected_cloud_model = st.selectbox(
        "Choose cloud model:",
        cloud_model_options,
        index=0,
        key="cloud_model_select"
    )

    # Show cloud model info
    if selected_cloud_model:
        cloud_info = CLOUD_MODELS[selected_cloud_model]
        st.caption(f"_{cloud_info['description']}_")
        pricing = cloud_info['pricing']
        st.caption(f"💰 ${pricing['input']:.2f} in / ${pricing['output']:.2f} out per 1M tokens")
        with st.expander("Best for"):
            for use in cloud_info['best_for']:
                st.markdown(f"• {use}")

    st.markdown("---")

    st.header("📊 Session Statistics")

    total_queries = len(st.session_state.queries)
    local_queries = sum(1 for q in st.session_state.queries if q['route'] == 'local')
    cloud_queries = total_queries - local_queries

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Queries", total_queries)
        st.metric("Local", local_queries, f"{(local_queries/total_queries*100 if total_queries > 0 else 0):.0f}%")
    with col2:
        st.metric("Cloud", cloud_queries, f"{(cloud_queries/total_queries*100 if total_queries > 0 else 0):.0f}%")

    st.markdown("---")

    total_cost = sum(q.get('cost', 0) for q in st.session_state.queries)
    st.metric("💰 Total API Cost", f"${total_cost:.4f}")

    # Calculate savings
    if total_queries > 0:
        # Estimate: if all queries went to cloud
        avg_cloud_cost = 0.005  # Rough average per query
        estimated_all_cloud = total_queries * avg_cloud_cost
        savings = estimated_all_cloud - total_cost
        savings_pct = (savings / estimated_all_cloud * 100) if estimated_all_cloud > 0 else 0

        st.metric("💵 Estimated Savings", f"${savings:.2f}", f"{savings_pct:.0f}%")

    if st.button("🗑️ Clear History"):
        st.session_state.queries = []
        st.session_state.total_cost = {"local": 0, "cloud": 0}
        st.rerun()

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🎯 Query Input")

    # Sample queries
    st.markdown("**Try these examples:**")
    example_col1, example_col2 = st.columns(2)

    with example_col1:
        if st.button("📝 Simple: What is HIPAA?"):
            query = "What is HIPAA?"
            st.session_state.current_query = query

    with example_col2:
        if st.button("🧠 Complex: Analyze legal implications"):
            query = "Analyze the legal implications of using AI for patient diagnosis in Hawaii, considering HIPAA compliance, malpractice liability, and state regulations. Provide detailed examples and risk mitigation strategies."
            st.session_state.current_query = query

    # Query input
    query = st.text_area(
        "Enter your query:",
        value=st.session_state.get('current_query', ''),
        height=100,
        placeholder="Type your question here..."
    )

    col_btn1, col_btn2, col_btn3 = st.columns(3)

    with col_btn1:
        run_auto = st.button("🚀 Auto Route", type="primary", use_container_width=True)
    with col_btn2:
        force_local = st.button("🏠 Force Local", use_container_width=True)
    with col_btn3:
        force_cloud = st.button("☁️ Force Cloud", use_container_width=True)

with col2:
    st.header("🎚️ Routing Decision")

    if query:
        analysis = analyze_query_complexity(query)

        # Complexity score visualization
        st.markdown(f"**Complexity Score: {analysis['score']:.2f}**")
        st.progress(analysis['score'])

        # Threshold indicator
        st.markdown(f"Threshold: {analysis['threshold']}")

        # Recommended route
        route_color = "local-route" if analysis['route'] == 'local' else "cloud-route"
        st.markdown(f"**Recommended:** <span class='{route_color}'>{analysis['route'].upper()}</span>",
                   unsafe_allow_html=True)

        # Factors
        with st.expander("📋 Complexity Factors"):
            for factor in analysis['factors']:
                st.markdown(f"- {factor}")

# Process query
if query and (run_auto or force_local or force_cloud):
    analysis = analyze_query_complexity(query)

    # Determine route
    if force_local:
        route = "local"
    elif force_cloud:
        route = "cloud"
    else:
        route = analysis['route']

    # Get selected models from session state
    local_model = st.session_state.get('local_model_select', available_local_models[0] if available_local_models else "deepseek-r1:7b")
    cloud_model = st.session_state.get('cloud_model_select', 'Claude Sonnet 4')

    # Show routing decision
    st.markdown("---")
    model_display = local_model if route == "local" else cloud_model
    st.markdown(f"### 🎯 Routing to: <span class='{'local-route' if route == 'local' else 'cloud-route'}'>{route.upper()}</span> → {model_display}",
               unsafe_allow_html=True)

    # Execute query
    with st.spinner(f"Processing with {model_display}..."):
        if route == "local":
            result = local_inference(query, local_model)
        else:
            result = cloud_inference(query, cloud_model)

    # Display results
    if result['success']:
        col_result1, col_result2 = st.columns([2, 1])

        with col_result1:
            st.markdown("### 💬 Response")
            st.markdown(result['response'])

        with col_result2:
            st.markdown("### 📊 Performance")

            st.metric("⚡ Latency", f"{result['latency']:.2f}s")

            if route == "local":
                st.metric("🚀 Speed", f"{result.get('tokens_per_sec', 0):.1f} t/s")

            st.metric("💰 Cost", f"${result['cost']:.6f}")

            # Token usage
            with st.expander("📝 Token Usage"):
                st.write(f"Input: {result.get('input_tokens', 0):,}")
                st.write(f"Output: {result.get('output_tokens', 0):,}")

        # Save to history
        st.session_state.queries.append({
            "query": query,
            "route": route,
            "model": result['model'],
            "latency": result['latency'],
            "cost": result['cost'],
            "timestamp": datetime.now().isoformat(),
            "complexity_score": analysis['score']
        })

    else:
        st.error(f"Error: {result.get('error', 'Unknown error')}")

# Query History
if st.session_state.queries:
    st.markdown("---")
    st.header("📜 Query History")

    for idx, q in enumerate(reversed(st.session_state.queries[-10:])):  # Show last 10
        with st.expander(f"Query {len(st.session_state.queries) - idx}: {q['query'][:50]}..."):
            col_hist1, col_hist2, col_hist3, col_hist4 = st.columns(4)

            with col_hist1:
                st.write(f"**Route:** {q['route'].upper()}")
            with col_hist2:
                st.write(f"**Model:** {q['model'].split(':')[0]}")
            with col_hist3:
                st.write(f"**Latency:** {q['latency']:.2f}s")
            with col_hist4:
                st.write(f"**Cost:** ${q['cost']:.6f}")

            st.write(f"**Complexity:** {q['complexity_score']:.2f}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <strong>LeniLani Consulting</strong> | AI & Technology Consulting for Hawaii Businesses<br>
    808-XXX-XXXX | reno@lenilani.com | lenilani.com
</div>
""", unsafe_allow_html=True)
