import os

ALLOWED_IFRAME_SITES = (
    "https://ui.dev https://*.ui.dev "
    "https://amiresponsive.co.uk https://*.amiresponsive.co.uk "
    "https://amiresponsive.com https://*.amiresponsive.com"
)

class AllowIframePreview:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        resp = self.get_response(request)

        # Enable only when explicitly turned on (e.g. for your demo)
        if os.environ.get("ALLOW_IFRAME", "0") == "1":
            # Remove Django’s X-Frame-Options if present
            resp.headers.pop("X-Frame-Options", None)
            # Loosen CSP for frames to known preview sites
            current_csp = resp.headers.get("Content-Security-Policy", "")
            # Keep other directives if you have them;
            # just ensure frame-ancestors allows previews
            parts = [p.strip() for p in current_csp.split(";") if p.strip() and not p.strip().startswith("frame-ancestors")]
            parts.append(f"frame-ancestors {ALLOWED_IFRAME_SITES}")
            resp.headers["Content-Security-Policy"] = "; ".join(parts)
        return resp