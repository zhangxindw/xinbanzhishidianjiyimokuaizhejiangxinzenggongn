import http.server, os, sys
class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/assets/") or self.path.startswith("/"):
            if os.path.exists("dist" + ("" if self.path == "/" else self.path.split("?")[0])):
                pass
            else:
                self.path = "/index.html"
        return super().do_GET()
os.chdir("dist")
http.server.HTTPServer(("0.0.0.0", 3000), Handler).serve_forever()
