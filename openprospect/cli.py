import argparse, os, webbrowser
import uvicorn
from dotenv import load_dotenv
from .db import list_companies

def main():
    load_dotenv()
    parser=argparse.ArgumentParser(prog='openprospect')
    parser.add_argument('command',nargs='?',default='dashboard',choices=['dashboard','status','companies','mcp'])
    args=parser.parse_args()
    if args.command=='dashboard':
        host=os.getenv('OPENPROSPECT_HOST','127.0.0.1'); port=int(os.getenv('OPENPROSPECT_PORT','5555'))
        url=f'http://{host}:{port}'
        print(f'OpenProspect dashboard: {url} (CTRL+C to stop)')
        webbrowser.open(url)
        uvicorn.run('openprospect.app:app',host=host,port=port)
    elif args.command=='status':
        print('OpenProspect status')
        print('Saved companies:',len(list_companies(100000)))
        print('Outbound sending: disabled')
    elif args.command=='companies':
        for company in list_companies(): print(f"#{company['id']} {company['name']} | {company['website']} | {company['industry']} | {company['location']}")
    elif args.command=='mcp':
        from .mcp_server import main as run_mcp
        run_mcp()

if __name__=='__main__': main()
