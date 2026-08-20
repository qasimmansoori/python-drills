import dns.resolver
from fastapi import FastAPI

app = FastAPI()


def domain_resolver(domain: str) -> dict:
    record_mx = []
    try:
        answer_mx = dns.resolver.resolve(domain, "MX")
        record_mx = [r.to_text() for r in answer_mx]
    except Exception as e:
        print("exception",e)

    record_spf = []
    try:
        answer_spf = dns.resolver.resolve(domain, "TXT")
        record_spf = [r.to_text().strip('"') for r in answer_spf if "v=spf1" in r.to_text().lower()]
    except Exception as e:
        print("exception",e)

    return {"spf": record_spf, "mx": record_mx}

@app.get('/resolve/{domain}')
def run_resolver(domain):
    return domain_resolver(domain)