from flask import Flask, render_template, request, redirect, url_for
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = Flask(__name__)

with open("documento.txt", "r", encoding="utf-8") as f:
    texto_base = f.read()

def gerar_resposta(pergunta, contexto):
    prompt = (
        "Responda a pergunta usando apenas o texto abaixo, sem adicionar informações externas. "
        "Se a resposta não estiver no texto, responda 'Não há informação suficiente no texto para responder.'\n\n"
        f"Texto:\n{contexto}\n\n"
        f"Pergunta: {pergunta}\nResposta:"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um assistente útil."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=200,
            temperature=0,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Erro API OpenAI:", e)
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
            resposta = gerar_resposta(pergunta, texto_base)
            if resposta is None:
                erro = "Erro ao processar a sua pergunta. Tente novamente mais tarde."
    return render_template("perguntar.html", resposta=resposta, erro=erro, pergunta=pergunta)

if __name__ == "__main__":
    app.run(debug=True)
