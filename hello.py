from flask import Flask
from markupsafe import escape
from datetime import datetime

app = Flask(__name__)

# Layout simples para reaproveitar cabeçalho/estilo
def layout(body_html: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Flasky</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin:0 }}
    .nav {{ background:#1f1f1f; color:#fff; padding:14px 24px }}
    .nav a {{ color:#fff; text-decoration:none; margin-right:16px }}
    .container {{ max-width:1100px; margin:40px auto; padding:0 24px }}
    h1 {{ font-weight:600; font-size:40px }}
    hr {{ border:0; border-top:1px solid #eee; margin:24px 0 }}
  </style>
</head>
<body>
  <div class="nav">
    <a href="/">Flasky</a> <a href="/">Home</a>
  </div>
  <div class="container">
    {body_html}
  </div>
</body>
</html>"""

@app.route("/")
def index():
    now = datetime.now()
    now_readable = now.strftime("%B %d, %Y %I:%M %p")
    now_iso = now.isoformat()
    body = f"""
      <h1>Hello World!</h1>
      <hr>
      <p>The local date and time is {now_readable}.</p>
      <p>That was <span id="ago">moments</span> ago.</p>
      <script>
        const renderedAt = new Date("{now_iso}");
        function updateAgo() {{
          const diff = Date.now() - renderedAt.getTime();
          const mins = Math.floor(diff/60000);
          const text = mins === 0 ? 'moments' : (mins === 1 ? '1 minute' : mins + ' minutes');
          document.getElementById('ago').textContent = text;
        }}
        updateAgo();
        setInterval(updateAgo, 60000);
      </script>
    """
    return layout(body)

@app.route("/user/Rafael%20Tonegi")
def greet(name):
    safe_name = escape(name)
    body = f"<h1>Hello, {safe_name}!</h1><hr>"
    return layout(body)

@app.errorhandler(404)
def not_found(e):
    body = "<h1>Not Found</h1><hr>"
    return layout(body), 404

if __name__ == "__main__":
    app.run()
