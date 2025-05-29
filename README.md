# 🎙️ YouTube Channel Downloader + Transcriber (Whisper)

Este projeto permite **baixar todos os vídeos de um canal do YouTube**, extrair o **áudio em MP3** e gerar **transcrições automáticas em português** usando o modelo [`Whisper`](https://github.com/openai/whisper) da OpenAI.  
Ideal para criar datasets para **chatbots com RAG**, geração de conteúdo, ou análise de vídeo.

---

## 📺 Tutorial recomendado

Siga este excelente tutorial para preparar seu ambiente no Windows:

🔗 [Tutorial YouTube - Como Instalar Whisper no Windows](https://www.youtube.com/watch?v=G6sOzBmxrLM&ab_channel=TheBinaryBrainiac)

---

## ⚙️ Requisitos

- Python 3.7+
- ffmpeg
- pip

---

## 📦 Instalação

### 1. Clone o repositório ou baixe o script

```bash
git clone https://github.com/seu-usuario/nome-do-repo.git
cd nome-do-repo
```
## ▶️ Como usar

### 1. Configure o link do canal

Abra o arquivo download_and_transcript.py e edite a variável CANAL_URL com o link do canal do YouTube desejado:

# CANAL_URL = "https://www.youtube.com/@nome_do_canal"

### 2. Execute o script

No terminal, dentro da pasta do projeto:

# python baixar_e_transcrever.py

O script executará automaticamente as seguintes etapas:

    Obtém a lista de vídeos do canal fornecido

    Baixa o áudio de cada vídeo em formato .mp3

    Usa o Whisper para gerar a transcrição em português

    Salva o resultado como .txt com o mesmo nome do áudio

## 📁 Estrutura de saída
O script criará uma pasta chamada videos_transcritos/, onde cada vídeo terá:

    videos_transcritos/
    ├── nome-do-video-1.mp3
    ├── nome-do-video-1.txt
    ├── nome-do-video-2.mp3
    ├── nome-do-video-2.txt
    └── ...
    
## 🧠 Possíveis usos
Geração de base de conhecimento para RAG (Retrieval-Augmented Generation)

Criação de resumos e artigos baseados em vídeo

Acessibilidade com transcrição automática

Indexação de vídeos para mecanismos de busca internos
