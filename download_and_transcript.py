import os
import subprocess
import whisper
from pathlib import Path

# CONFIGURAÇÕES
CANAL_URL = "https://www.youtube.com/@inffelcursos3360"
PASTA_SAIDA = "videos_transcritos_inffelCursos"

# Criar a pasta de saída se não existir
os.makedirs(PASTA_SAIDA, exist_ok=True)

# Passo 1: Baixar os áudios do canal
print("🔽 Baixando os áudios do canal...")
subprocess.run([
    "yt-dlp",
    "-x",                      # extrair áudio
    "--audio-format", "mp3",   # formato mp3
    "-o", f"{PASTA_SAIDA}/%(title)s.%(ext)s",  # caminho de saída
    CANAL_URL
])

# Passo 2: Carregar modelo Whisper
print("Carregando modelo Whisper...")
model = whisper.load_model("small")  # Pode ser: tiny, base, small, medium, large

# Passo 3: Transcrever cada arquivo de áudio
print("Iniciando transcrição...")
for audio_file in Path(PASTA_SAIDA).glob("*.mp3"):
    print(f"🔊 Transcrevendo: {audio_file.name}")
    result = model.transcribe(str(audio_file), language="pt")

    # Salvar transcrição como .txt
    transcript_path = audio_file.with_suffix(".txt")
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

print("Transcrição finalizada!")
