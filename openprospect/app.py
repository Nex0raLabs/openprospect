from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from .db import add_company, list_companies, connect
from .ai import ask_ai
app=FastAPI(title="OpenProspect",version="0.1.0")
CSS="""<style>:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#0d1117;color:#e6edf3;font:15px system-ui}header{padding:22px 5%;border-bottom:1px solid #30363d;display:flex;justify-content:space-between}.brand{font-size:23px;font-weight:800}small,.muted{color:#8b949e}nav{padding:16px 5%;border-bottom:1px solid #30363d;display:flex;gap:22px;flex-wrap:wrap}a{color:#58a6ff;text-decoration:none}main{max-width:1120px;margin:34px auto;padding:0 22px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px}.card,section{background:#161b22;border:1px solid #30363d;border-radius:12px;padding:20px;margin-bottom:16px}h1{font-size:30px;margin:0 0 8px}.number{font-size:32px;font-weight:800;margin-top:12px}input,textarea,button{font:inherit;padding:11px;border-radius:8px;border:1px solid #30363d;background:#0d1117;color:#e6edf3;width:100%;margin:5px 0}button{background:#238636;border:0;font-weight:700;cursor:pointer}table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:11px;border-bottom:1px solid #30363d}@media(max-width:600px){header{flex-direction:column;gap:8px}}</style>"""
def shell(body):
 return f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OpenProspect</title>{CSS}</head><body><header><div><div class="brand">◈ OpenProspect</div><small>Free, open-source prospecting workspace</small></div><small>Local-first · Human approval</small></header><nav><a href="/">Today</a><a href="/companies">Companies</a><a href="/drafts">Drafts</a><a href="/docs">API docs</a></nav><main>{body}</main></body></html>'
def table(items):
 if not items:return '<p class="muted">No companies yet.</p>'
 rows="".join(f"<tr><td>{x['name']}</td><td>{x['website'] or '—'}</td><td>{x['industry']}</td><td>{x['location']}</td></tr>" for x in items)
 return f"<table><tr><th>Company</th><th>Website</th><th>Industry</th><th>Location</th></tr>{rows}</table>"
@app.get("/",response_class=HTMLResponse)
def home():
 items=list_companies()
 with connect() as c: drafts=c.execute("SELECT COUNT(*) n FROM drafts").fetchone()["n"]
 return shell(f"<h1>Your prospecting workspace</h1><p class='muted'>Manage prospects and prepare outreach. Nothing is sent automatically.</p><div class='grid'><div class='card'>Companies<div class='number'>{len(items)}</div></div><div class='card'>Drafts<div class='number'>{drafts}</div></div><div class='card'>Emails sent<div class='number'>0</div><small>Sending is not enabled in this release</small></div></div><section><h2>Add a company</h2><form method='post' action='/companies'><input name='name' placeholder='Business name' required><input name='website' placeholder='Website URL'><input name='industry' placeholder='Industry'><input name='location' placeholder='City, country'><textarea name='notes' placeholder='Notes'></textarea><button>Add company</button></form></section><section><h2>Recent companies</h2>{table(items[:10])}</section>")
@app.get("/companies",response_class=HTMLResponse)
def companies_page(): return shell("<h1>Companies</h1>"+table(list_companies(500)))
@app.post("/companies")
def create_company(name:str=Form(...),website:str=Form(""),industry:str=Form(""),location:str=Form(""),notes:str=Form("")):
 add_company(name,website,industry,location,notes);return RedirectResponse("/",status_code=303)
@app.get("/api/companies")
def api_companies(): return {"companies":list_companies(500)}
@app.post("/api/companies")
def api_add_company(payload:dict):
 if not payload.get("name"): raise HTTPException(400,"name is required")
 ident=add_company(payload["name"],payload.get("website",""),payload.get("industry",""),payload.get("location",""),payload.get("notes",""),"api")
 return {"id":ident,"ok":True}
@app.get("/drafts",response_class=HTMLResponse)
def drafts_page():
 with connect() as c: rows=[dict(r) for r in c.execute("SELECT * FROM drafts ORDER BY id DESC")]
 body="".join(f"<section><b>{r['subject'] or 'Message draft'}</b><p>{r['body']}</p><small>Status: {r['status']}</small></section>" for r in rows) or "<p class='muted'>No drafts yet.</p>"
 return shell("<h1>Drafts</h1>"+body)
@app.post("/api/ai")
def ai_chat(payload:dict):
 try:return {"response":ask_ai(str(payload.get("prompt","")))}
 except Exception as e:raise HTTPException(400,str(e))
