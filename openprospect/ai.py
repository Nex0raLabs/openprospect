from __future__ import annotations
import json, os, urllib.request

def ask_ai(prompt: str, system: str = "You are a helpful business research and outreach assistant.") -> str:
    provider=os.getenv("OPENPROSPECT_AI_PROVIDER","openai-compatible").lower()
    model=os.getenv("OPENPROSPECT_AI_MODEL","")
    key=os.getenv("OPENPROSPECT_AI_API_KEY","")
    base=os.getenv("OPENPROSPECT_AI_BASE_URL","https://api.openai.com/v1").rstrip("/")
    if provider=="ollama":
        base=os.getenv("OPENPROSPECT_AI_BASE_URL","http://localhost:11434/v1").rstrip("/")
        model=model or "llama3.2"
    if provider=="anthropic":
        base=os.getenv("ANTHROPIC_BASE_URL","https://api.anthropic.com").rstrip("/")
        model=model or "claude-3-5-haiku-latest"
        payload={"model":model,"max_tokens":1200,"system":system,"messages":[{"role":"user","content":prompt}]}
        headers={"x-api-key":key,"anthropic-version":"2023-06-01","content-type":"application/json"}
        req=urllib.request.Request(base+"/v1/messages",data=json.dumps(payload).encode(),headers=headers,method="POST")
        with urllib.request.urlopen(req,timeout=90) as res: data=json.loads(res.read())
        return "".join(x.get("text","") for x in data.get("content",[]) if x.get("type")=="text")
    if not model: raise RuntimeError("Set OPENPROSPECT_AI_MODEL in .env before using AI.")
    payload={"model":model,"messages":[{"role":"system","content":system},{"role":"user","content":prompt}]}
    headers={"content-type":"application/json"}
    if key: headers["authorization"]="Bearer "+key
    req=urllib.request.Request(base+"/chat/completions",data=json.dumps(payload).encode(),headers=headers,method="POST")
    with urllib.request.urlopen(req,timeout=90) as res: data=json.loads(res.read())
    return data["choices"][0]["message"]["content"]
