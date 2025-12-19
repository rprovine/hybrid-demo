#!/usr/bin/env python3
"""
Test script to verify hybrid router demo setup
Run this BEFORE your client demo to ensure everything works
"""

import sys
import subprocess

def test_imports():
    """Test that all required packages are installed"""
    print("Testing imports...")
    try:
        import streamlit
        print("✅ Streamlit installed:", streamlit.__version__)
    except ImportError:
        print("❌ Streamlit not installed. Run: pip install streamlit --break-system-packages")
        return False

    try:
        import ollama
        print("✅ Ollama installed")
    except ImportError:
        print("❌ Ollama not installed. Run: pip install ollama --break-system-packages")
        return False

    try:
        import anthropic
        print("✅ Anthropic installed")
    except ImportError:
        print("⚠️  Anthropic not installed (optional). Run: pip install anthropic --break-system-packages")

    try:
        import openai
        print("✅ OpenAI installed")
    except ImportError:
        print("⚠️  OpenAI not installed (optional). Run: pip install openai --break-system-packages")

    return True

def test_ollama_service():
    """Test that Ollama service is running"""
    print("\nTesting Ollama service...")
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            print("✅ Ollama service is running")
            print("\nInstalled models:")
            print(result.stdout)
            return True
        else:
            print("❌ Ollama service error")
            print(result.stderr)
            return False
    except FileNotFoundError:
        print("❌ Ollama not found. Install from: https://ollama.com/download")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Ollama service not responding")
        return False

def test_model_availability():
    """Test that required model is available"""
    print("\nTesting model availability...")
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True
        )

        models = result.stdout.lower()

        if "deepseek-r1:7b" in models:
            print("✅ deepseek-r1:7b is available")
            return True
        elif "deepseek-r1" in models:
            print("⚠️  DeepSeek-R1 found, but not 7b variant")
            print("   Available variants:", [line for line in result.stdout.split('\n') if 'deepseek-r1' in line.lower()])
            return True
        else:
            print("❌ deepseek-r1:7b not found")
            print("\nRun: ollama pull deepseek-r1:7b")
            return False
    except Exception as e:
        print(f"❌ Error checking models: {e}")
        return False

def test_ollama_inference():
    """Test that model can actually run inference"""
    print("\nTesting model inference...")
    try:
        import ollama

        print("Running test query (this may take 10-30 seconds)...")
        response = ollama.chat(
            model="deepseek-r1:7b",
            messages=[{"role": "user", "content": "Say 'Hello from Hawaii' in exactly 3 words."}]
        )

        print("✅ Model inference successful!")
        print(f"Response: {response['message']['content']}")
        return True
    except Exception as e:
        print(f"❌ Inference failed: {e}")
        return False

def test_gpu():
    """Test GPU availability"""
    print("\nTesting GPU...")
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            gpu_info = result.stdout.strip()
            print(f"✅ GPU detected: {gpu_info}")

            # Check VRAM
            if "16" in gpu_info or "4080" in gpu_info:
                print("✅ 16GB VRAM confirmed - perfect for 7B-14B models")

            return True
        else:
            print("⚠️  nvidia-smi failed, but GPU may still work")
            return True
    except FileNotFoundError:
        print("⚠️  nvidia-smi not found (NVIDIA drivers may not be installed)")
        return True
    except Exception as e:
        print(f"⚠️  GPU test error: {e}")
        return True

def test_api_keys():
    """Test API keys (optional)"""
    print("\nTesting API keys (optional for cloud comparison)...")
    import os

    has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))
    has_openai = bool(os.getenv("OPENAI_API_KEY"))

    if has_anthropic:
        print("✅ ANTHROPIC_API_KEY found")
    else:
        print("⚠️  ANTHROPIC_API_KEY not set (cloud comparison will fail)")
        print("   Set with: export ANTHROPIC_API_KEY='your_key'")

    if has_openai:
        print("✅ OPENAI_API_KEY found")
    else:
        print("⚠️  OPENAI_API_KEY not set (optional)")
        print("   Set with: export OPENAI_API_KEY='your_key'")

    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("LeniLani Hybrid Router Demo - System Check")
    print("=" * 60)

    results = {
        "Imports": test_imports(),
        "Ollama Service": test_ollama_service(),
        "Model Availability": test_model_availability(),
        "GPU": test_gpu(),
        "API Keys": test_api_keys(),
    }

    # Only test inference if everything else passed
    if results["Imports"] and results["Ollama Service"] and results["Model Availability"]:
        results["Model Inference"] = test_ollama_inference()
    else:
        results["Model Inference"] = False
        print("\n⚠️  Skipping inference test due to previous failures")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")

    critical_tests = ["Imports", "Ollama Service", "Model Availability", "Model Inference"]
    critical_passed = all(results.get(test, False) for test in critical_tests)

    print("\n" + "=" * 60)
    if critical_passed:
        print("✅ ALL CRITICAL TESTS PASSED!")
        print("\nYou're ready to run the demo:")
        print("  streamlit run hybrid_router_demo.py")
    else:
        print("❌ SOME TESTS FAILED")
        print("\nFix the issues above before running demo.")
    print("=" * 60)

    return 0 if critical_passed else 1

if __name__ == "__main__":
    sys.exit(main())
