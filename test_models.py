#!/usr/bin/env python3
import urllib.request
import json
import time

API_KEY = "YOUR_OPENROUTER_API_KEY"

MODELS = {
    "nemotron-3-super":    "nvidia/llama-3.1-nemotron-super-49b-v1:free",
    "laguna-m1":           "poolside/laguna-m.1:free",
    "gpt-oss-20b":         "openai/gpt-oss-20b:free",
    "glm-4.5-air":         "z-ai/glm-4.5-air:free",
    "minimax-m2.5":        "minimax/minimax-m2.5:free",
    "laguna-xs2":          "poolside/laguna-xs.2:free",
    "nemotron-nano-30b":   "nvidia/llama-3.1-nemotron-nano-8b-v1:free",
    "cobuddy":             "baidu/cobuddy:free",
    "trinity-thinking":    "arcee-ai/trinity-large-thinking:free",
    "deepseek-v4-flash":   "deepseek/deepseek-v4-flash:free",
    "gemma-4-31b":         "google/gemma-4-31b-it:free",
}

print("Testing new models (timeout=20s each)...\n")
print(f"{'Model':<25} {'Status':<8} {'Time':>6}  {'Response'}")
print("-" * 70)

working = {}

for name, model_id in MODELS.items():
    try:
        data = json.dumps({
            "model": model_id,
            "messages": [{"role": "user", "content": "Reply with just: OK"}],
            "max_tokens": 10
        }).encode()

        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=data,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost",
            }
        )

        t0 = time.time()
        with urllib.request.urlopen(req, timeout=20) as r:
            result = json.loads(r.read())
        elapsed = time.time() - t0

        if "choices" in result:
            reply = result["choices"][0]["message"]["content"][:30].strip()
            print(f"  ✅ {name:<23} OK      {elapsed:>5.1f}s  \"{reply}\"")
            working[name] = {"id": model_id, "time": elapsed}
        else:
            err = result.get("error", {}).get("message", "?")[:50]
            print(f"  ❌ {name:<23} FAIL           {err}")

    except Exception as e:
        err = str(e)[:60]
        print(f"  ❌ {name:<23} FAIL           {err}")

# Add previously confirmed working
working["nemotron-nano-12b"] = {"id": "nvidia/nemotron-nano-12b-v2-vl:free", "time": 1.0}
working["gpt-oss-120b"]      = {"id": "openai/gpt-oss-120b:free",            "time": 1.9}
working["owl-alpha"]         = {"id": "openrouter/owl-alpha",                 "time": 4.4}

print("\n" + "=" * 70)
sorted_models = sorted(working.items(), key=lambda x: x[1]["time"])
print(f"\n✅ Total working: {len(working)} models\n")
print("Ranked by speed:")
for i, (name, info) in enumerate(sorted_models, 1):
    print(f"  {i}. {name:<25} {info['time']:.1f}s")

print("\n--- Paste into main.py ---\n")
print("FREE_MODELS = {")
print('    "auto":  "openrouter/auto",')
for name, info in sorted_models:
    print(f'    "{name}": "{info["id"]}",')
print("}")
print(f'\nDEFAULT_MODEL = "{sorted_models[0][0]}"')