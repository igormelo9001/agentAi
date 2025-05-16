from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Função que gera resposta
def gerar_resposta(pergunta):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um assistente prestativo e amigável."},
                {"role": "user", "content": pergunta}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Erro na geração: {str(e)}")
        return None

@app.route("/")
def index():
    return redirect(url_for("perguntar"))

@app.route("/perguntar", methods=["GET", "POST"])
def perguntar():
    resposta = erro = pergunta = None
    if request.method == "POST":
        pergunta = request.form.get("pergunta", "").strip()
        if not pergunta:
            erro = "Por favor, digite sua pergunta."
        else:
            resposta = gerar_resposta(pergunta)
            if resposta is None:
                erro = "Erro ao processar a sua pergunta."
    return render_template("perguntar.html", resposta=resposta, erro=erro, pergunta=pergunta)

if __name__ == "__main__":
    app.run(debug=True)
