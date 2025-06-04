# 🎥 YouTube Video Transcription & AI Documentation Suite

Uma aplicação completa em **Streamlit** para baixar vídeos do YouTube, transcrever áudios usando **Whisper** da OpenAI e transformar as transcrições em documentação estruturada usando **GPT-4** para sistemas de **RAG (Retrieval-Augmented Generation)**.

## ✨ **Principais Funcionalidades**

### 🌐 **Processamento de Canal Completo**
- Download automático de todos os vídeos de um canal do YouTube
- Transcrição em lote usando modelos Whisper
- Transliteração inteligente para documentação técnica

### 🎬 **Processamento de Vídeo Único**
- Download e processamento de vídeos específicos
- Controle granular sobre as etapas do processo
- Ideal para testes e conteúdo pontual

### 🎵 **Upload de Áudio Direto**
- Suporte a múltiplos formatos: MP3, WAV, M4A, FLAC, OGG
- Processamento completo sem necessidade de YouTube
- Perfeito para áudios de reuniões, palestras, podcasts

### 🔄 **Transliteração Inteligente**
- Transforma transcrições brutas em documentação estruturada
- Remove vícios de linguagem e organiza o conteúdo
- Adequado para indexação por sistemas de IA

---

## 📺 **Tutorial Recomendado**

Para configurar o ambiente no Windows, siga este tutorial:

🔗 [Como Instalar Whisper no Windows](https://www.youtube.com/watch?v=G6sOzBmxrLM&ab_channel=TheBinaryBrainiac)

---

## ⚙️ **Requisitos do Sistema**

### **Software Necessário:**
- **Python 3.8+** (recomendado 3.9+)
- **ffmpeg** (para processamento de áudio)
- **yt-dlp** (para download do YouTube)
- **Streamlit** (interface web)

### **APIs Necessárias:**
- **OpenAI API Key** (para transliteração com GPT-4)

### **Hardware Recomendado:**
- **RAM:** 8GB+ (16GB para modelos Whisper maiores)
- **GPU:** NVIDIA CUDA compatível (opcional, acelera a transcrição)
- **Armazenamento:** 10GB+ livre

---

## 📦 **Instalação**

### **1. Clone o Repositório**
```bash
git clone https://github.com/RafaelTaves/Download-Transcript
```

### **2. Crie um Ambiente Virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### **3. Instale as Dependências**
```bash
pip install -r requirements.txt
```

### **4. Configure a API Key**
Crie um arquivo `config.py` na raiz do projeto:
```python
OPENAI_API_KEY = "sua-api-key-aqui"
```

---

## 🚀 **Como Usar**

### **1. Inicie a Aplicação**
```bash
streamlit run app.py
```

### **2. Acesse a Interface**
Abra seu navegador em: `http://localhost:8501`

### **3. Configure as Pastas**
Na **sidebar**, defina os nomes das pastas:
- **Pasta de Transcritos:** onde serão salvos os arquivos .txt
- **Pasta de Transliterados:** onde ficará a documentação final

### **4. Escolha seu Fluxo de Trabalho**

#### **🌐 Canal Completo**
1. Cole a URL do canal do YouTube
2. Selecione as etapas desejadas:
   - ✅ Baixar áudios
   - ✅ Transcrever 
   - ✅ Transliterar
3. Clique em "Processar Canal Completo"

#### **🎬 Vídeo Único**
1. Cole a URL de um vídeo específico
2. Configure as etapas
3. Processe individualmente

#### **🎵 Upload de Áudio**
1. Faça upload do arquivo de áudio
2. Defina um nome para o arquivo
3. O processamento é automático

---

## 📁 **Estrutura de Arquivos**

```
projeto/
├── app.py                          # Aplicação principal
├── config.py                       # Configurações da API
├── requirements.txt                # Dependências
├── README.md                       # Este arquivo
├── videos_transcritos/             # Transcrições brutas
│   ├── video-1.mp3
│   ├── video-1.txt
│   └── ...
└── videos_transliterados/          # Documentação final
    ├── video-1-Transliterado.txt
    └── ...
```

---

## 🎛️ **Configurações Avançadas**

### **Modelos Whisper Disponíveis:**

| Modelo | Tamanho | Velocidade | Qualidade | RAM Necessária |
|--------|---------|------------|-----------|----------------|
| `tiny`   | 39 MB   | Muito rápida | Básica    | 1 GB          |
| `base`   | 74 MB   | Rápida      | Boa       | 1 GB          |
| `small`  | 244 MB  | Moderada    | Muito boa | 2 GB          |
| `medium` | 769 MB  | Lenta       | Excelente | 5 GB          |
| `large`  | 1550 MB | Muito lenta | Superior  | 10 GB         |

### **Personalização do Prompt de Transliteração**

O template pode ser modificado na variável `PROMPT_TEMPLATE` para:
- Ajustar o estilo da documentação
- Definir formatos específicos
- Incluir instruções personalizadas

---

## 🔧 **Solução de Problemas**

### **Erro: "ffmpeg not found"**
```bash
# Instale o ffmpeg conforme sua plataforma
# Certifique-se que está no PATH do sistema
ffmpeg -version
```

### **Erro: "OpenAI API key not configured"**
```python
# Verifique o arquivo config.py
OPENAI_API_KEY = "sk-proj-..."  # Deve começar com sk-
```

### **Erro: "yt-dlp failed"**
```bash
# Atualize o yt-dlp
pip install --upgrade yt-dlp
```

### **Memória Insuficiente**
- Use modelos Whisper menores (`tiny`, `base`)
- Feche outros programas
- Considere processamento em lotes menores

---

## 🧠 **Casos de Uso**

### **🤖 Sistemas de IA e RAG**
- Base de conhecimento para chatbots
- Documentação para retrieval systems
- Datasets para fine-tuning

### **📚 Educação e Treinamento**
- Transcrição de aulas e palestras
- Material de estudo estruturado
- Documentação de cursos online

### **💼 Empresarial**
- Transcrição de reuniões
- Documentação de webinars
- Arquivo de conhecimento corporativo

### **🎙️ Mídia e Conteúdo**
- Transcrição de podcasts
- Legendas para vídeos
- Material para blogs e artigos

### **♿ Acessibilidade**
- Conteúdo acessível para deficientes auditivos
- Busca textual em conteúdo de vídeo
- Multilingual content processing

---

## 📊 **Recursos da Interface**

### **Dashboard de Resultados**
- Estatísticas em tempo real
- Contadores de arquivos processados
- Links diretos para pastas de resultado

### **Controles Granulares**
- Execute apenas as etapas necessárias
- Pule arquivos já processados
- Personalização de nomes e pastas

### **Preview de Conteúdo**
- Visualização de transcrições
- Preview da documentação final
- Expandable text areas para análise

---

## 🔐 **Segurança e Privacidade**

- **API Keys:** Mantenha suas chaves seguras no arquivo `config.py`
- **Dados Locais:** Todo processamento é feito localmente
- **Uploads:** Arquivos de áudio são processados temporariamente

---

## 🚧 **Roadmap e Melhorias Futuras**

- [ ] Suporte a mais idiomas
- [ ] Integração com outras APIs de IA
- [ ] Processamento em lotes otimizado
- [ ] Interface para edição de transcrições
- [ ] Exportação para diferentes formatos
- [ ] Sistema de templates personalizáveis
- [ ] Integração com bancos vetoriais
- [ ] API REST para automação

---

## 🤝 **Contribuindo**

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## 📝 **Licença**

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 🌟 **Agradecimentos**

- **OpenAI** pelo Whisper e GPT-4
- **Streamlit** pela excelente framework
- **yt-dlp** pelos downloads do YouTube
- **Comunidade Open Source** pelas ferramentas incríveis

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela no GitHub! ⭐**

</div>

---

# English Version

# 🎥 YouTube Video Transcription & AI Documentation Suite

A complete **Streamlit** application for downloading YouTube videos, transcribing audio using OpenAI's **Whisper**, and transforming transcriptions into structured documentation using **GPT-4** for **RAG (Retrieval-Augmented Generation)** systems.

## ✨ **Key Features**

### 🌐 **Complete Channel Processing**
- Automatic download of all videos from a YouTube channel
- Batch transcription using Whisper models
- Intelligent transliteration for technical documentation

### 🎬 **Single Video Processing**
- Download and process specific videos
- Granular control over process steps
- Ideal for testing and specific content

### 🎵 **Direct Audio Upload**
- Support for multiple formats: MP3, WAV, M4A, FLAC, OGG
- Complete processing without YouTube dependency
- Perfect for meeting recordings, lectures, podcasts

### 🔄 **Intelligent Transliteration**
- Transforms raw transcriptions into structured documentation
- Removes speech fillers and organizes content
- Suitable for AI system indexing

---

## 📺 **Recommended Tutorial**

To set up the environment on Windows, follow this tutorial:

🔗 [How to Install Whisper on Windows](https://www.youtube.com/watch?v=G6sOzBmxrLM&ab_channel=TheBinaryBrainiac)

---

## ⚙️ **System Requirements**

### **Required Software:**
- **Python 3.8+** (recommended 3.9+)
- **ffmpeg** (for audio processing)
- **yt-dlp** (for YouTube downloads)
- **Streamlit** (web interface)

### **Required APIs:**
- **OpenAI API Key** (for GPT-4 transliteration)

### **Recommended Hardware:**
- **RAM:** 8GB+ (16GB for larger Whisper models)
- **GPU:** NVIDIA CUDA compatible (optional, accelerates transcription)
- **Storage:** 10GB+ free space

---

## 📦 **Installation**

### **1. Clone the Repository**
```bash
git clone https://github.com/RafaelTaves/Download-Transcript
cd youtube-transcription-suite
```

### **2. Create Virtual Environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Configure API Key**
Create a `config.py` file in the project root:
```python
OPENAI_API_KEY = "your-api-key-here"
```

---

## 🚀 **How to Use**

### **1. Start the Application**
```bash
streamlit run app.py
```

### **2. Access the Interface**
Open your browser at: `http://localhost:8501`

### **3. Configure Folders**
In the **sidebar**, define folder names:
- **Transcripts Folder:** where .txt files will be saved
- **Transliterated Folder:** where final documentation will be stored

### **4. Choose Your Workflow**

#### **🌐 Complete Channel**
1. Paste the YouTube channel URL
2. Select desired steps:
   - ✅ Download audio
   - ✅ Transcribe
   - ✅ Transliterate
3. Click "Process Complete Channel"

#### **🎬 Single Video**
1. Paste a specific video URL
2. Configure steps
3. Process individually

#### **🎵 Audio Upload**
1. Upload audio file
2. Define a filename
3. Processing is automatic

---

## 🧠 **Use Cases**

### **🤖 AI Systems and RAG**
- Knowledge base for chatbots
- Documentation for retrieval systems
- Datasets for fine-tuning

### **📚 Education and Training**
- Lecture and presentation transcription
- Structured study materials
- Online course documentation

### **💼 Enterprise**
- Meeting transcription
- Webinar documentation
- Corporate knowledge archive

### **🎙️ Media and Content**
- Podcast transcription
- Video subtitles
- Material for blogs and articles

### **♿ Accessibility**
- Accessible content for hearing impaired
- Text search in video content
- Multilingual content processing

---

<div align="center">

**⭐ If this project was helpful, consider giving it a star on GitHub! ⭐**

</div>