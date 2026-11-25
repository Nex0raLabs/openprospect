"""Dashboard surfaces for real mailbox, inbox, automation and compliance features."""
from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from .db import connect, list_activity, log, is_suppressed, add_suppression
from .conversations import ensure_schema, list_conversations
from .messaging import email_status, imap_status, send_email, sync_imap
from .automation import run_once, start_loop, pause_loop, loop_status
from .compliance import dns_report, privacy_checklist
from .security import get_dashboard_token

router=APIRouter()
def page(title,body):
    from .app import shell
    return shell(f"<h1>{title}</h1>{body}")

@router.get("/inbox",response_class=HTMLResponse)
def inbox():
    ensure_schema(); rows=list_conversations()
    body="".join(f"<section><b>{r['channel'].upper()} · {r['contact_address']}</b><p>{r['subject']}</p><p>{r['last_message'][:800]}</p><small>{r['updated_at']} · {r['status']}</small></section>" for r in rows)
    s=email_status(); m=imap_status()
    body+=f"<section><h2>Mailbox connections</h2><p>SMTP: {'Configured' if s['configured'] else 'Not connected'} · IMAP: {'Configured' if m['configured'] else 'Not connected'}</p><p>Configure OPENPROSPECT_SMTP_* and OPENPROSPECT_IMAP_* environment variables, then restart.</p><form method='post' action='/inbox/sync'><button>Sync IMAP now</button></form></section>"
    return page("Unified conversations",body or "<p>No conversations yet. Connect IMAP or the WhatsApp sidecar to receive messages.</p>")

@router.post("/inbox/sync",response_class=HTMLResponse)
def inbox_sync():
    try: result=sync_imap()
    except Exception as exc: return page("IMAP sync",f"<p class='warning'>Sync failed: {exc}</p><a href='/inbox'>Back</a>")
    return page("IMAP sync",f"<p>New messages imported: {result['synced']}</p><a href='/inbox'>Open inbox</a>")

@router.get("/controls",response_class=HTMLResponse)
def controls():
    state=loop_status()
    return page("Autonomous controls",f"<section><p>Status: <b>{'Running' if state['running'] else 'Paused'}</b></p><p>{state['mode']}</p><form method='post' action='/controls/start'><button>Start loop</button></form><form method='post' action='/controls/pause'><button class='secondary'>Pause loop</button></form><form method='post' action='/controls/run'><button class='secondary'>Run one cycle now</button></form></section><p class='warning'>The loop profiles public websites and records buying signals only. It never sends email or WhatsApp automatically.</p>")
@router.post("/controls/start")
def controls_start():
    start_loop();return RedirectResponse("/controls",303)
@router.post("/controls/pause")
def controls_pause():
    pause_loop();return RedirectResponse("/controls",303)
@router.post("/controls/run",response_class=HTMLResponse)
def controls_run():
    result=run_once()
    return page("Pipeline run",f"<p>Companies profiled: {result.get('processed',0)}</p><pre>{result.get('errors',[])}</pre><a href='/controls'>Back</a>")

@router.get("/compliance",response_class=HTMLResponse)
def compliance():
    items="".join(f"<li>{x['item']}</li>" for x in privacy_checklist())
    return page("Compliance & DNS",f"<section><h2>DNS checks</h2><form method='post' action='/compliance/dns'><input name='domain' placeholder='example.com' required><button>Check SPF, DMARC and MX</button></form><p>DKIM requires your provider's selector and is not guessed.</p></section><section><h2>Privacy readiness checklist</h2><ul>{items}</ul><p class='muted'>Operational checklist only, not legal advice. Review Kenya's Data Protection Act and ODPC guidance with qualified counsel.</p></section>")

@router.post("/compliance/dns",response_class=HTMLResponse)
def compliance_dns(domain:str=Form(...)):
    try: data=dns_report(domain)
    except Exception as exc: return page("DNS report",f"<p class='warning'>{exc}</p><a href='/compliance'>Back</a>")
    rows="".join(f"<tr><td>{k.upper()}</td><td>{v['status']}</td><td>{', '.join(v['records']) or 'No record returned'}</td></tr>" for k,v in data.items() if isinstance(v,dict))
    return page("DNS report",f"<section><p>Domain: {data['domain']}</p><table><tr><th>Record</th><th>Status</th><th>Evidence</th></tr>{rows}</table><p>{data['notes']}</p></section><a href='/compliance'>Check another domain</a>")

@router.get("/connections",response_class=HTMLResponse)
def connections():
    from .messaging import email_status,imap_status
    smtp=email_status();imap=imap_status()
    return page("Connections",f"<section><h2>Email</h2><p>SMTP: {'Configured' if smtp['configured'] else 'Not connected'}</p><p>IMAP: {'Configured' if imap['configured'] else 'Not connected'}</p><p>Missing SMTP variables: {', '.join(smtp['missing']) or 'None'}</p><p>Missing IMAP variables: {', '.join(imap['missing']) or 'None'}</p><p>Credentials are read from environment variables; never paste them into the dashboard.</p></section><section><h2>WhatsApp</h2><p>Baileys sidecar: not connected until separately installed, paired and health-checked.</p><p>Cloud API: not connected until access token, phone-number ID and webhook are configured.</p></section>")
