from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import subprocess

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
      <title>3D Password Strength Analyzer</title>
      <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');
        body {
          font-family: 'Poppins', sans-serif;
          background: radial-gradient(circle at 20% 20%, #001F3F, #0074D9, #00BFFF);
          height: 100vh;
          display: flex;
          justify-content: center;
          align-items: center;
          margin: 0;
          color: white;
          overflow: hidden;
        }
        .container {
          background: rgba(255, 255, 255, 0.08);
          padding: 50px;
          border-radius: 20px;
          box-shadow: 0 0 60px rgba(0, 0, 0, 0.5);
          backdrop-filter: blur(15px);
          text-align: center;
          width: 400px;
          transition: transform 0.5s;
          animation: float 4s ease-in-out infinite;
        }
        @keyframes float {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-10px); }
        }
        h1 {
          font-size: 26px;
          text-shadow: 2px 2px 12px #000;
        }
        input[type=password] {
          width: 80%;
          padding: 12px;
          border: none;
          border-radius: 12px;
          margin-top: 25px;
          font-size: 16px;
          text-align: center;
          outline: none;
          box-shadow: inset 0 0 8px rgba(255,255,255,0.3);
        }
        button {
          margin-top: 25px;
          padding: 10px 35px;
          background: linear-gradient(90deg, #00c6ff, #0072ff);
          border: none;
          border-radius: 10px;
          color: white;
          font-size: 16px;
          cursor: pointer;
          transition: 0.3s;
          box-shadow: 0 0 10px #00c6ff;
        }
        button:hover {
          transform: scale(1.05);
          background: linear-gradient(90deg, #0072ff, #00c6ff);
        }
        .progress-container {
          margin-top: 20px;
          height: 15px;
          width: 80%;
          background: rgba(255, 255, 255, 0.2);
          border-radius: 10px;
          overflow: hidden;
          display: inline-block;
        }
        .progress-bar {
          height: 100%;
          width: 0%;
          background: #ff4d4d;
          border-radius: 10px;
          transition: width 0.8s ease, background 0.8s ease;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>🔐 Password Strength Checker</h1>
        <form action="/check" method="post" id="passwordForm">
          <input type="password" id="password" name="password" placeholder="Enter your password" required>
          <div class="progress-container">
            <div class="progress-bar" id="strengthBar"></div>
          </div>
          <br>
          <button type="submit">Analyze</button>
        </form>
      </div>
      <script>
        const password = document.getElementById('password');
        const bar = document.getElementById('strengthBar');
        password.addEventListener('input', () => {
          const val = password.value;
          let score = 0;
          if (val.match(/[a-z]/)) score += 20;
          if (val.match(/[A-Z]/)) score += 20;
          if (val.match(/[0-9]/)) score += 20;
          if (val.match(/[^a-zA-Z0-9]/)) score += 20;
          if (val.length >= 8) score += 20;
          bar.style.width = score + '%';
          if (score < 40) bar.style.background = '#ff4d4d';
          else if (score < 80) bar.style.background = '#FFD700';
          else bar.style.background = '#00ff88';
        });
      </script>
    </body>
    </html>
    """


@app.post("/check", response_class=HTMLResponse)
def check(password: str = Form(...)):
    # Run the compiled C program
    result = subprocess.run(["./password_strength"], input=f"{password}\n", text=True, capture_output=True)

    output = result.stdout.replace("\033[1;31m", "<span style='color:#ff4d4d;font-weight:bold;'>") \
                          .replace("\033[1;33m", "<span style='color:#FFD700;font-weight:bold;'>") \
                          .replace("\033[1;32m", "<span style='color:#00ff88;font-weight:bold;'>") \
                          .replace("\033[0m", "</span>") \
                          .replace("\n", "<br>")

    # Extract suggested password (for copy button)
    suggested_password = ""
    if "Suggested Stronger Password:" in output:
        parts = output.split("Suggested Stronger Password:")
        if len(parts) > 1:
            suggested_password = parts[1].split("<br>")[0].strip()

    return f"""
    <html>
    <head>
      <title>Result - Password Strength</title>
      <style>
        body {{
          font-family: 'Poppins', sans-serif;
          background: linear-gradient(120deg, #2c3e50, #4ca1af);
          color: white;
          text-align: center;
          height: 100vh;
          display: flex;
          justify-content: center;
          align-items: center;
        }}
        .result-box {{
          background: rgba(255,255,255,0.1);
          border-radius: 20px;
          padding: 40px;
          width: 500px;
          box-shadow: 0 0 25px rgba(0,0,0,0.4);
          backdrop-filter: blur(10px);
          animation: pop 0.5s ease;
        }}
        @keyframes pop {{
          from {{ transform: scale(0.9); opacity: 0; }}
          to {{ transform: scale(1); opacity: 1; }}
        }}
        button {{
          background: #00bfff;
          border: none;
          border-radius: 10px;
          padding: 10px 20px;
          color: white;
          font-size: 14px;
          cursor: pointer;
          margin-top: 15px;
          transition: 0.3s;
        }}
        button:hover {{
          background: #0072ff;
        }}
        a {{
          color: #00ffff;
          text-decoration: none;
          margin-top: 15px;
          display: inline-block;
        }}
        a:hover {{
          color: #1abc9c;
        }}
      </style>
    </head>
    <body>
      <div class="result-box">
        <h2>🔍 Password Analysis</h2>
        <p>{output}</p>
        {"<button onclick=\"navigator.clipboard.writeText('" + suggested_password + "')\">📋 Copy Suggested Password</button>" if suggested_password else ""}
        <br>
        <a href="/">⬅️ Try Again</a>
      </div>
    </body>
    </html>
    """

