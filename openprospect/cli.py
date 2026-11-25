import argparse, os, webbrowser
from pathlib import Path
import uvicorn
from dotenv import load_dotenv
from .db import list_companies
from .training import train_website


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(prog="openprospect")
    parser.add_argument("command", nargs="?", default="dashboard", choices=["dashboard", "status", "companies", "mcp", "train"])
    parser.add_argument("url", nargs="?")
    args = parser.parse_args()
    if args.command == "dashboard":
        host = os.getenv("OPENPROSPECT_HOST", "127.0.0.1")
        port = int(os.getenv("OPENPROSPECT_PORT", "5555"))
        if host not in {"127.0.0.1", "::1", "localhost"}:
            parser.error("Dashboard host must be loopback-only (127.0.0.1, ::1 or localhost).")
        from .app import app
        from .training_routes import router as training_router
        app.include_router(training_router)
        url = f"http://{host}:{port}"
        print(f"OpenProspect dashboard: {url} (CTRL+C to stop)")
        webbrowser.open(url)
        uvicorn.run(app, host=host, port=port)
    elif args.command == "status":
        print("OpenProspect status")
        print("Saved companies:", len(list_companies(100000)))
        print("Outbound sending: disabled")
    elif args.command == "companies":
        for company in list_companies():
            print(f"#{company['id']} {company['name']} | {company['website']} | {company['industry']} | {company['location']}")
    elif args.command == "mcp":
        from .mcp_server import main as run_mcp
        run_mcp()
    elif args.command == "train":
        if not args.url:
            parser.error("train requires a website URL, e.g. openprospect train https://example.com")
        data = train_website(args.url)
        print("Website training saved.")
        print("Config:", data["_config_path"])
        print("Pages read:", len(data["pages_read"]))
        print("Product excerpts:", len(data["product"]))
        print("Published emails:", len(data["emails_published"]))
        print("Edit the result in the dashboard at /train or in the JSON config file.")


if __name__ == "__main__":
    main()
