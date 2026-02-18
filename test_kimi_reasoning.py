import asyncio
import os
import time
from litellm import acompletion

async def test_kimi(thinking_disabled=False):
    api_key = "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"
    api_base = "https://integrate.api.nvidia.com/v1"
    model = "openai/moonshotai/kimi-k2.5"
    
    kwargs = {
        "model": model,
        "messages": [{"role": "user", "content": "Explain quantum entanglement in 2 sentences."}],
        "api_key": api_key,
        "api_base": api_base,
        "temperature": 1.0,
    }
    
    if thinking_disabled:
        # Based on Moonshot API docs, though NVIDIA NIM might differ
        kwargs["extra_body"] = {"thinking": {"type": "disabled"}}
    
    start = time.time()
    try:
        response = await acompletion(**kwargs)
        end = time.time()
        print(f"Thinking disabled: {thinking_disabled}")
        print(f"Time taken: {end - start:.2f}s")
        print(f"Content: {response.choices[0].message.content}")
        if hasattr(response.choices[0].message, "reasoning_content"):
            print(f"Reasoning: {response.choices[0].message.reasoning_content}")
        print("-" * 20)
    except Exception as e:
        print(f"Error (thinking_disabled={thinking_disabled}): {e}")

async def main():
    print("Testing Kimi k2.5 with and without reasoning...\n")
    await test_kimi(thinking_disabled=False)
    await test_kimi(thinking_disabled=True)

if __name__ == "__main__":
    asyncio.run(main())
