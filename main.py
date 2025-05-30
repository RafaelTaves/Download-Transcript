import os
import subprocess
from pathlib import Path
import whisper
from openai import OpenAI
from config import OPENAI_API_KEY  # Certifique-se de ter esse arquivo com sua chave

# CONFIGURAÇÕES
CANAL_URL = "https://www.youtube.com/@inffelcursos3360"
PASTA_TRANSCRITOS = "videos_transcritos_inffelCursos"
PASTA_TRANSLITERADOS = "videos_transliterados_inffelCursos"

# Criar pastas se não existirem
os.makedirs(PASTA_TRANSCRITOS, exist_ok=True)
os.makedirs(PASTA_TRANSLITERADOS, exist_ok=True)

# Prompt para a transliteração
PROMPT_TEMPLATE = """
Tarefa:
Você é um assistente especialista em transformar transcrições de vídeos em uma documentação clara, organizada e objetiva, adequada para ser usada em um sistema de IA baseado em RAG.

Entrada:
Você receberá uma transcrição de vídeo, que pode conter informalidades, repetições ou interrupções típicas da fala natural.

Objetivo:
Sua tarefa é transliterar essa transcrição em um conteúdo documental, bem estruturado, com tópicos claros, subtítulos quando necessário e sem linguagem coloquial. A ideia é manter toda a informação essencial passada no vídeo, mas no formato de um texto técnico ou explicativo, semelhante a um artigo, manual ou documentação de conhecimento.

Instruções específicas:
- Organize o conteúdo em tópicos, subtópicos e parágrafos coerentes.
- Elimine vícios de linguagem e repetições.
- Conserve o sentido original da fala, mas com clareza e concisão.
- Quando possível, use bullet points, enumerações ou tabelas para facilitar a leitura.
- Não invente informações não presentes na transcrição.
- Todas as palavras encontradas como Einfel, fel, infel, ou termos relacionados devem ser substituídas por 'Inffel' para manter a consistência com a marca.

Formato de saída:
Uma documentação clara, didática e adequada para indexação e consulta por uma IA via RAG.

Agora, aqui está a transcrição para ser processada:

{}
"""

# Instancia cliente da OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Função para transliterar o texto
def transliterar_transcricao(conteudo):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": PROMPT_TEMPLATE.format(conteudo)}
        ],
        temperature=0.6
    )
    return response.choices[0].message.content

# Etapa 1: Baixar os áudios do canal
def baixar_audios():
    print("🔽 Baixando os áudios do canal...")
    subprocess.run([
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "-o", f"{PASTA_TRANSCRITOS}/%(title)s.%(ext)s",
        CANAL_URL
    ])
    print("✅ Download concluído.")

# Etapa 2: Transcrever com Whisper
def transcrever_audios():
    print("🧠 Carregando modelo Whisper...")
    model = whisper.load_model("small")

    print("📝 Iniciando transcrição...")
    for audio_file in Path(PASTA_TRANSCRITOS).glob("*.mp3"):
        print(f"🔊 Transcrevendo: {audio_file.name}")
        result = model.transcribe(str(audio_file), language="pt")

        transcript_path = audio_file.with_suffix(".txt")
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(result["text"])
        print(f"✅ Transcrição salva: {transcript_path.name}")
    print("📄 Transcrições finalizadas.")

# Etapa 3: Transliterar os textos
def transliterar_transcricoes():
    print("📚 Iniciando transliteração...")
    for nome_arquivo in os.listdir(PASTA_TRANSCRITOS):
        if nome_arquivo.endswith(".txt") and not nome_arquivo.endswith("-Transliterado.txt"):
            caminho_arquivo = os.path.join(PASTA_TRANSCRITOS, nome_arquivo)
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                conteudo = f.read()

            print(f"🔄 Processando: {nome_arquivo}")
            resultado = transliterar_transcricao(conteudo)

            nome_saida = nome_arquivo.replace(".txt", "-Transliterado.txt")
            caminho_saida = os.path.join(PASTA_TRANSLITERADOS, nome_saida)
            with open(caminho_saida, "w", encoding="utf-8") as f_out:
                f_out.write(resultado)
            print(f"✅ Transliteração salva: {nome_saida}")
    print("📘 Transliteração finalizada.")

# Execução do fluxo completo
if __name__ == "__main__":
    baixar_audios()
    transcrever_audios()
    transliterar_transcricoes()
    print("🚀 Transliterações finalizadas com sucesso!")
