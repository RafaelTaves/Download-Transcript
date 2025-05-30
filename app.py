import os
import subprocess
import whisper
from pathlib import Path
import streamlit as st
from openai import OpenAI
from config import OPENAI_API_KEY
import tempfile

# =========================
# CONFIGURAÇÕES PADRÃO
# =========================
PASTA_TRANSCRITOS_PADRAO = "videos_transcritos"
PASTA_TRANSLITERADOS_PADRAO = "videos_transliterados"

# Cliente OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Prompt para transliteração
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

Formato de saída:
Uma documentação clara, didática e adequada para indexação e consulta por uma IA via RAG.

Agora, aqui está a transcrição para ser processada:

{}
"""

# =========================
# FUNÇÕES AUXILIARES
# =========================

def criar_pastas(pasta_transcritos, pasta_transliterados):
    """Cria as pastas necessárias"""
    os.makedirs(pasta_transcritos, exist_ok=True)
    os.makedirs(pasta_transliterados, exist_ok=True)

def salvar_audio_temporario(uploaded_file):
    """Salva o arquivo de áudio em um local temporário"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        return tmp_file.name

# =========================
# FUNÇÕES PRINCIPAIS
# =========================

def baixar_audios_canal(canal_url: str, pasta_transcritos: str):
    """Baixa todos os áudios de um canal"""
    st.info("🔽 Baixando áudios do canal...")
    subprocess.run([
        "yt-dlp",
        "-x", "--audio-format", "mp3",
        "-o", f"{pasta_transcritos}/%(title)s.%(ext)s",
        canal_url
    ])
    st.success("✅ Download do canal concluído!")

def baixar_video_unico(video_url: str, pasta_transcritos: str):
    """Baixa o áudio de um vídeo específico"""
    st.info("🔽 Baixando áudio do vídeo...")
    subprocess.run([
        "yt-dlp",
        "-x", "--audio-format", "mp3",
        "-o", f"{pasta_transcritos}/%(title)s.%(ext)s",
        video_url
    ])
    st.success("✅ Download do vídeo concluído!")

def transcrever_audios(pasta_transcritos: str, modelo: str = "small"):
    """Transcreve todos os áudios na pasta"""
    st.info("🧠 Carregando modelo Whisper...")
    model = whisper.load_model(modelo)

    st.info("📄 Iniciando transcrição...")
    arquivos_processados = 0
    
    for audio_file in Path(pasta_transcritos).glob("*.mp3"):
        txt_path = audio_file.with_suffix(".txt")
        if txt_path.exists():
            st.write(f"⏭️ Pulando (já transcrito): {audio_file.name}")
            continue

        st.write(f"🔊 Transcrevendo: {audio_file.name}")
        result = model.transcribe(str(audio_file), language="pt")

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(result["text"])
        
        arquivos_processados += 1

    if arquivos_processados > 0:
        st.success(f"✅ Transcrição finalizada! ({arquivos_processados} arquivos processados)")
    else:
        st.info("ℹ️ Nenhum arquivo novo para transcrever.")

def transcrever_audio_unico(caminho_audio: str, modelo: str = "small"):
    """Transcreve um único arquivo de áudio"""
    st.info("🧠 Carregando modelo Whisper...")
    model = whisper.load_model(modelo)
    
    st.info("📄 Iniciando transcrição...")
    result = model.transcribe(caminho_audio, language="pt")
    
    st.success("✅ Transcrição concluída!")
    return result["text"]

def transliterar_transcricao(conteudo: str):
    """Translita uma transcrição usando OpenAI"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": PROMPT_TEMPLATE.format(conteudo)}],
        temperature=0.6
    )
    return response.choices[0].message.content

def executar_transliteracao(pasta_transcritos: str, pasta_transliterados: str):
    """Executa a transliteração de todos os arquivos transcritos"""
    st.info("🔄 Iniciando transliteração...")
    arquivos_processados = 0
    
    for nome_arquivo in os.listdir(pasta_transcritos):
        if nome_arquivo.endswith(".txt") and not nome_arquivo.endswith("-Transliterado.txt"):
            caminho_arquivo = os.path.join(pasta_transcritos, nome_arquivo)
            
            # Verificar se já foi transliterado
            nome_saida = nome_arquivo.replace(".txt", "-Transliterado.txt")
            caminho_saida = os.path.join(pasta_transliterados, nome_saida)
            
            if os.path.exists(caminho_saida):
                st.write(f"⏭️ Pulando (já transliterado): {nome_arquivo}")
                continue
            
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                conteudo = f.read()

            st.write(f"📝 Transliterando: {nome_arquivo}")
            resultado = transliterar_transcricao(conteudo)

            with open(caminho_saida, "w", encoding="utf-8") as f_out:
                f_out.write(resultado)

            st.success(f"✅ Salvo: {nome_saida}")
            arquivos_processados += 1
    
    if arquivos_processados > 0:
        st.success(f"🎉 Transliteração concluída! ({arquivos_processados} arquivos processados)")
    else:
        st.info("ℹ️ Nenhum arquivo novo para transliterar.")

def mostrar_arquivos_transliterados(pasta_transliterados: str):
    """Mostra os arquivos transliterados disponíveis"""
    if not os.path.exists(pasta_transliterados):
        st.warning("📁 Pasta de transliterados não encontrada.")
        return
    
    arquivos = [arq for arq in os.listdir(pasta_transliterados) if arq.endswith("-Transliterado.txt")]
    
    if not arquivos:
        st.info("📄 Nenhum arquivo transliterado encontrado.")
        return
    
    st.subheader("📁 Arquivos transliterados disponíveis:")
    for arq in arquivos:
        with open(os.path.join(pasta_transliterados, arq), "r", encoding="utf-8") as f:
            conteudo = f.read()
        with st.expander(f"📄 {arq}"):
            st.text_area("Conteúdo:", conteudo, height=300, disabled=True)

# =========================
# STREAMLIT APP
# =========================

st.set_page_config(page_title="Transcrição + Transliteração de Vídeos", layout="wide")
st.title("🎥 Transcrição e Transliteração de Vídeos")

# Sidebar para configurações
with st.sidebar:
    st.header("⚙️ Configurações")
    
    pasta_transcritos = st.text_input(
        "📁 Pasta de Transcritos:", 
        value=PASTA_TRANSCRITOS_PADRAO,
        help="Nome da pasta onde serão salvos os arquivos transcritos"
    )
    
    pasta_transliterados = st.text_input(
        "📁 Pasta de Transliterados:", 
        value=PASTA_TRANSLITERADOS_PADRAO,
        help="Nome da pasta onde serão salvos os arquivos transliterados"
    )
    
    modelo_whisper = st.selectbox(
        "🧠 Modelo Whisper", 
        ["tiny", "base", "small", "medium", "large"], 
        index=2,
        help="Modelo mais pesado = melhor qualidade, mas mais lento"
    )

# Criar as pastas com os nomes configurados
criar_pastas(pasta_transcritos, pasta_transliterados)

# Tabs principais
tab1, tab2, tab3, tab4 = st.tabs(["🌐 Canal Completo", "🎬 Vídeo Único", "🎵 Upload de Áudio", "📋 Resultados"])

# =========================
# TAB 1: CANAL COMPLETO
# =========================
with tab1:
    st.header("🌐 Processar Canal Completo do YouTube")
    
    with st.form("canal_form"):
        canal_url = st.text_input(
            "URL do canal do YouTube", 
            value="https://www.youtube.com/",
            placeholder="https://www.youtube.com/@seucanal"
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            fazer_download = st.checkbox("🔽 Baixar áudios", value=True)
        with col2:
            fazer_transcricao = st.checkbox("📄 Transcrever", value=True)
        with col3:
            fazer_transliteracao = st.checkbox("🔄 Transliterar", value=True)
        
        submitted_canal = st.form_submit_button("🚀 Processar Canal Completo", use_container_width=True)

    if submitted_canal and canal_url:
        try:
            if fazer_download:
                baixar_audios_canal(canal_url, pasta_transcritos)
            
            if fazer_transcricao:
                transcrever_audios(pasta_transcritos, modelo_whisper)
            
            if fazer_transliteracao:
                executar_transliteracao(pasta_transcritos, pasta_transliterados)
            
            st.success("✅ Processo do canal completo finalizado!")
        except Exception as e:
            st.error(f"❌ Erro durante o processamento: {str(e)}")

# =========================
# TAB 2: VÍDEO ÚNICO
# =========================
with tab2:
    st.header("🎬 Processar Vídeo Único do YouTube")
    
    with st.form("video_form"):
        video_url = st.text_input(
            "URL do vídeo do YouTube",
            placeholder="https://www.youtube.com/watch?v=..."
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            fazer_download_video = st.checkbox("🔽 Baixar áudio", value=True, key="video_download")
        with col2:
            fazer_transcricao_video = st.checkbox("📄 Transcrever", value=True, key="video_transcricao")
        with col3:
            fazer_transliteracao_video = st.checkbox("🔄 Transliterar", value=True, key="video_transliteracao")
        
        submitted_video = st.form_submit_button("🚀 Processar Vídeo", use_container_width=True)

    if submitted_video and video_url:
        try:
            if fazer_download_video:
                baixar_video_unico(video_url, pasta_transcritos)
            
            if fazer_transcricao_video:
                transcrever_audios(pasta_transcritos, modelo_whisper)
            
            if fazer_transliteracao_video:
                executar_transliteracao(pasta_transcritos, pasta_transliterados)
            
            st.success("✅ Processamento do vídeo finalizado!")
        except Exception as e:
            st.error(f"❌ Erro durante o processamento: {str(e)}")

# =========================
# TAB 3: UPLOAD DE ÁUDIO
# =========================
with tab3:
    st.header("🎵 Upload e Processamento de Áudio")
    
    uploaded_file = st.file_uploader(
        "Escolha um arquivo de áudio",
        type=['mp3', 'wav', 'm4a', 'flac', 'ogg'],
        help="Formatos suportados: MP3, WAV, M4A, FLAC, OGG"
    )
    
    if uploaded_file is not None:
        st.success(f"✅ Arquivo carregado: {uploaded_file.name}")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            nome_arquivo = st.text_input(
                "Nome para o arquivo (sem extensão):",
                value=Path(uploaded_file.name).stem
            )
        
        if st.button("🚀 Processar Áudio Carregado", use_container_width=True):
            try:
                # Salvar arquivo temporário
                caminho_temp = salvar_audio_temporario(uploaded_file)
                
                # Transcrever
                with st.spinner("🔊 Transcrevendo áudio..."):
                    transcricao = transcrever_audio_unico(caminho_temp, modelo_whisper)
                
                # Salvar transcrição
                nome_transcricao = f"{nome_arquivo}.txt"
                caminho_transcricao = os.path.join(pasta_transcritos, nome_transcricao)
                
                with open(caminho_transcricao, "w", encoding="utf-8") as f:
                    f.write(transcricao)
                
                st.success("✅ Transcrição salva!")
                
                # Mostrar prévia da transcrição
                with st.expander("👀 Prévia da Transcrição"):
                    st.text_area("Transcrição:", transcricao, height=200, disabled=True)
                
                # Transliterar
                with st.spinner("🔄 Transliterando..."):
                    transliteracao = transliterar_transcricao(transcricao)
                
                # Salvar transliteração
                nome_transliteracao = f"{nome_arquivo}-Transliterado.txt"
                caminho_transliteracao = os.path.join(pasta_transliterados, nome_transliteracao)
                
                with open(caminho_transliteracao, "w", encoding="utf-8") as f:
                    f.write(transliteracao)
                
                st.success("✅ Transliteração concluída!")
                
                # Mostrar resultado final
                with st.expander("📄 Resultado da Transliteração"):
                    st.text_area("Transliteração:", transliteracao, height=400, disabled=True)
                
                # Limpar arquivo temporário
                os.unlink(caminho_temp)
                
            except Exception as e:
                st.error(f"❌ Erro durante o processamento: {str(e)}")

# =========================
# TAB 4: RESULTADOS
# =========================
with tab4:
    st.header("📋 Resultados e Arquivos Gerados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📁 Estatísticas")
        
        # Contar arquivos
        transcritos_count = len([f for f in os.listdir(pasta_transcritos) if f.endswith('.txt')]) if os.path.exists(pasta_transcritos) else 0
        transliterados_count = len([f for f in os.listdir(pasta_transliterados) if f.endswith('.txt')]) if os.path.exists(pasta_transliterados) else 0
        audios_count = len([f for f in os.listdir(pasta_transcritos) if f.endswith('.mp3')]) if os.path.exists(pasta_transcritos) else 0
        
        st.metric("🎵 Áudios baixados", audios_count)
        st.metric("📄 Arquivos transcritos", transcritos_count)
        st.metric("🔄 Arquivos transliterados", transliterados_count)
    
    with col2:
        st.subheader("🛠️ Ações")
        
        if st.button("🔄 Atualizar estatísticas"):
            st.rerun()
        
        if st.button("🗂️ Abrir pasta de transcritos"):
            if os.path.exists(pasta_transcritos):
                os.startfile(pasta_transcritos)  # Windows
        
        if st.button("🗂️ Abrir pasta de transliterados"):
            if os.path.exists(pasta_transliterados):
                os.startfile(pasta_transliterados)  # Windows
    
    # Mostrar arquivos transliterados
    mostrar_arquivos_transliterados(pasta_transliterados)