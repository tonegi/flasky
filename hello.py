from flask import Flask, request, redirect, url_for
from markupsafe import escape
from datetime import datetime
import pytz

app = Flask(__name__)

def layout(body_html: str) -> str:
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Avaliação contínua: Aula 050.B</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin:0 }}
    .nav {{ background:#1f1f1f; color:#fff; padding:14px 24px }}
    .nav a {{ color:#fff; text-decoration:none; margin-left:16px }}
    .container {{ max-width:1100px; margin:40px auto; padding:0 24px }}
    h1 {{ font-weight:600; font-size:32px }}
    hr {{ border:0; border-top:1px solid #eee; margin:24px 0 }}
    input, select {{ padding:8px; margin:6px 0 16px 0; width:100%; max-width:500px; display:block }}
    button {{ padding:10px 18px; background:#007bff; color:#fff; border:none; cursor:pointer; border-radius:4px }}
    .card {{ border:1px solid #eee; padding:20px; border-radius:6px; max-width:400px; margin:auto }}
</style>
</head>
<body>
<div class="nav">
 Avaliação contínua: <b>Aula 050.B</b>
 <a href="/">Home</a>
 <a href="/login">Login</a>
</div>
<div class="container">
 {body_html}
</div>
</body>
</html>"""

@app.route("/", methods=["GET", "POST"])
def index():
    tz = pytz.timezone("America/Sao_Paulo")
    now = datetime.now(tz)
    now_readable = now.strftime("%B %d, %Y %I:%M %p")
    now_iso = now.isoformat()

    nome, sobrenome, instituicao, disciplina = "", "", "", ""

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        sobrenome = request.form.get("sobrenome", "").strip()
        instituicao = request.form.get("instituicao", "").strip()
        disciplina = request.form.get("disciplina", "").strip()
        if not nome or not sobrenome or not instituicao or not disciplina:
            return redirect(url_for("index"))

    user_ip = request.remote_addr or "Desconhecido"
    host = request.host_url.rstrip("/")

    body = f"""
    <h1>Olá, {"Estranho" if not nome else escape(nome)} {escape(sobrenome)}!</h1>
    <p>A sua Instituição de ensino é {escape(instituicao) if instituicao else "None"}</p>
    <p>Está cursando a disciplina de {escape(disciplina)}</p>
    <p>O IP do computador remoto é: {escape(user_ip if nome else "None")}</p>
    <p>O host da aplicação é: {escape(host if nome else "None")}</p>
    <hr>
    <form method="post">
        <label>Informe o seu nome:</label>
        <input type="text" name="nome" value="{escape(nome)}" required>
        <label>Informe o seu sobrenome:</label>
        <input type="text" name="sobrenome" value="{escape(sobrenome)}" required>
        <label>Informe a sua Instituição de ensino:</label>
        <input type="text" name="instituicao" value="{escape(instituicao)}" required>
        <label>Informe a sua disciplina:</label>
        <select name="disciplina" required>
            <option value="DSWA5" {"selected" if disciplina=="DSWA5" else ""}>DSWA5</option>
            <option value="DWBA4" {"selected" if disciplina=="DWBA4" else ""}>DWBA4</option>
            <option value="Gestão de Projetos" {"selected" if disciplina=="Gestão de Projetos" else ""}>Gestão de Projetos</option>
        </select>
        <button type="submit">Submit</button>
    </form>
    <hr>
    <p>The local date and time is {now_readable}.</p>
    <p>That was <span id="ago">moments</span> ago.</p>
    <script>
        const renderedAt = new Date("{now_iso}");
        function updateAgo() {{
            const diff = Date.now() - renderedAt.getTime();
            const mins = Math.floor(diff/60000);
            const text = mins <= 0 ? 'moments' : (mins === 1 ? '1 minute' : mins + ' minutes');
            document.getElementById('ago').textContent = text;
        }}
        updateAgo();
        setInterval(updateAgo, 60000);
    </script>
    """
    return layout(body)

@app.route("/login", methods=["GET", "POST"])
def login():
    tz = pytz.timezone("America/Sao_Paulo")
    now = datetime.now(tz)
    now_readable = now.strftime("%B %d, %Y %I:%M %p")

    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        return redirect(url_for("login_response", usuario=usuario))

    body = f"""
    <div class="card">
        <h3>Login:</h3>
        <form method="post">
            <label>Usuário ou e-mail</label>
            <input type="text" name="usuario" required>
            <label>Informe a sua senha</label>
            <input type="password" name="senha" required>
            <button type="submit">Enviar</button>
        </form>
    </div>
    <hr>
    <p>The local date and time is {now_readable}.</p>
    <p>That was a few seconds ago.</p>
    """
    return layout(body)

@app.route("/loginResponse")
def login_response():
    usuario = request.args.get("usuario", "desconhecido")
    tz = pytz.timezone("America/Sao_Paulo")
    now = datetime.now(tz)
    now_readable = now.strftime("%B %d, %Y %I:%M %p")

    body = f"""
    <h2>Dados de Acesso</h2>
    <hr>
    <p>Você está acessando o sistema por meio do usuário {escape(usuario)}</p>
    <p>The local date and time is {now_readable}.</p>
    <p>That was a few seconds ago.</p>
    """
    return layout(body)

@app.errorhandler(404)
def not_found(e):
    return layout("<h1>Not Found</h1><hr>"), 404

if __name__ == "__main__":
    app.run(debug=True)
