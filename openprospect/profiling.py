from __future__ import annotations
import re, urllib.request
from html import unescape
from html.parser import HTMLParser

class PageText(HTMLParser):
    def __init__(self):
        super().__init__();self.title=False;self.in_title=False;self.parts=[];self.meta={}
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="title":self.in_title=True
        if tag=="meta" and a.get("name","").lower() in ("description","og:description"):
            self.meta[a.get("name","").lower()]=a.get("content","")
        if tag in ("script","style","noscript","svg"):self.parts.append(" ")
    def handle_endtag(self,tag):
        if tag=="title":self.in_title=False
    def handle_data(self,data):
        if data.strip():self.parts.append(data.strip())

def profile_website(url:str):
    if not url:return {"error":"No website URL saved for this company."}
    if not re.match(r"^https?://",url,re.I):url="https://"+url
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; OpenProspect/0.1; +https://github.com/linkto254-bot/openprospect)"})
    try:
        with urllib.request.urlopen(req,timeout=20) as res:
            final_url=res.geturl();raw=res.read(1_500_000).decode("utf-8","replace")
    except Exception as e:return {"error":f"Could not read website: {e}"}
    parser=PageText()
    try:parser.feed(raw)
    except Exception:pass
    text=" ".join(parser.parts)
    text=re.sub(r"\s+"," ",unescape(text))[:12000]
    emails=sorted(set(re.findall(r"(?i)[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}",raw)))
    phones=sorted(set(re.findall(r"(?<!\w)(?:\+?\d[\d ().-]{7,}\d)",text)))[:10]
    title=re.search(r"<title[^>]*>(.*?)</title>",raw,re.I|re.S)
    return {"url":final_url,"title":unescape(re.sub(r"<.*?>","",title.group(1))).strip() if title else "",
            "description":parser.meta.get("description","") or parser.meta.get("og:description",""),
            "emails":emails,"phones":phones,"text":text}
