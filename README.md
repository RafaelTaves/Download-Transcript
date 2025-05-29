# 🎙️ YouTube Video Downloader + Transcriber (Whisper)

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

#### CANAL_URL = "https://www.youtube.com/@nome_do_canal"

### 2. Execute o script

No terminal, dentro da pasta do projeto:

#### python baixar_e_transcrever.py

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


# English Version

This project allows you to **download all videos from a YouTube channel**, extract the **audio in MP3 format**, and generate **automatic transcripts in Portuguese** using OpenAI's [`Whisper`](https://github.com/openai/whisper) model.  
Perfect for building datasets for **RAG-based chatbots**, content creation, or video analysis.

---

## 📺 Recommended Tutorial

Follow this excellent tutorial to set up your environment on Windows:

🔗 [YouTube Tutorial - How to Install Whisper on Windows](https://www.youtube.com/watch?v=G6sOzBmxrLM&ab_channel=TheBinaryBrainiac)

---

## ⚙️ Requirements

- Python 3.7+
- ffmpeg
- pip

---

## 📦 Installation

### 1. Clone the repository or download the script

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

## ▶️ How to Use
### 1. Set the channel link
Open the download_and_transcript.py file and update the CANAL_URL variable with the desired YouTube channel link:

#### CANAL_URL = "https://www.youtube.com/@channel_name"

## 2. Run the script
In the terminal, inside the project folder:

#### python baixar_e_transcrever.py

The script will automatically perform the following steps:

    Fetch the list of videos from the specified channel
    Download the audio from each video in .mp3 format
    Use Whisper to generate the transcript in Portuguese
    Save the transcript as a .txt file with the same name as the audio

## 📁 Output Structure

The script will create a folder named videos_transcritos/, where each video will include:

videos_transcritos/
├── video-name-1.mp3
├── video-name-1.txt
├── video-name-2.mp3
├── video-name-2.txt
└── ...

## 🧠 Possible Use Cases

Build knowledge bases for RAG (Retrieval-Augmented Generation)

Generate summaries and articles from video content

Improve accessibility with automatic transcription

Enable internal search by indexing video transcripts






