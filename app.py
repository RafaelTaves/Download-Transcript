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

def listar_videos_pasta(pasta_videos):
    """Lista todos os arquivos de vídeo em uma pasta"""
    extensoes_video = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v', '.3gp']
    videos = []
    
    if not os.path.exists(pasta_videos):
        return videos
    
    try:
        for arquivo in os.listdir(pasta_videos):
            if any(arquivo.lower().endswith(ext) for ext in extensoes_video):
                videos.append(arquivo)
    except PermissionError:
        st.error(f"❌ Sem permissão para acessar a pasta: {pasta_videos}")
    
    return sorted(videos)

def extrair_audio_video(caminho_video, pasta_destino):
    """Extrai o áudio de um arquivo de vídeo usando ffmpeg"""
    nome_arquivo = Path(caminho_video).stem
    caminho_audio = os.path.join(pasta_destino, f"{nome_arquivo}.mp3")
    
    # Se o áudio já existe, pular
    if os.path.exists(caminho_audio):
        return caminho_audio
    
    try:
        # Usar ffmpeg para extrair áudio
        subprocess.run([
            'ffmpeg', '-i', caminho_video,
            '-vn', '-acodec', 'mp3', '-ab', '192k',
            '-ar', '44100', '-y', caminho_audio
        ], check=True, capture_output=True)
        
        return caminho_audio
    except subprocess.CalledProcessError as e:
        st.error(f"❌ Erro ao extrair áudio de {Path(caminho_video).name}: {e}")
        return None
    except FileNotFoundError:
        st.error("❌ FFmpeg não encontrado. Instale o FFmpeg para extrair áudio dos vídeos.")
        return None

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

def processar_videos_pasta(pasta_videos, pasta_transcritos, pasta_transliterados, modelo_whisper, videos_selecionados=None):
    """Processa vídeos de uma pasta local"""
    videos = listar_videos_pasta(pasta_videos)
    
    if not videos:
        st.warning("📁 Nenhum vídeo encontrado na pasta especificada.")
        return
    
    # Se não especificou vídeos, processar todos
    if videos_selecionados is None:
        videos_selecionados = videos
    
    st.info(f"🎬 Processando {len(videos_selecionados)} vídeo(s)...")
    
    # Carregar modelo Whisper uma vez
    st.info("🧠 Carregando modelo Whisper...")
    model = whisper.load_model(modelo_whisper)
    
    videos_processados = 0
    videos_com_erro = []
    
    for video in videos_selecionados:
        if video not in videos:
            continue
            
        st.write(f"🎥 Processando: {video}")
        caminho_video = os.path.join(pasta_videos, video)
        nome_base = Path(video).stem
        
        try:
            # 1. Extrair áudio
            st.write("🔊 Extraindo áudio...")
            caminho_audio = extrair_audio_video(caminho_video, pasta_transcritos)
            
            if not caminho_audio:
                videos_com_erro.append(video)
                continue
            
            # 2. Transcrever
            caminho_transcricao = os.path.join(pasta_transcritos, f"{nome_base}.txt")
            
            if not os.path.exists(caminho_transcricao):
                st.write("📄 Transcrevendo...")
                result = model.transcribe(caminho_audio, language="pt")
                
                with open(caminho_transcricao, "w", encoding="utf-8") as f:
                    f.write(result["text"])
            else:
                st.write("⏭️ Transcrição já existe, pulando...")
            
            # 3. Transliterar
            caminho_transliteracao = os.path.join(pasta_transliterados, f"{nome_base}-Transliterado.txt")
            
            if not os.path.exists(caminho_transliteracao):
                st.write("🔄 Transliterando...")
                
                with open(caminho_transcricao, "r", encoding="utf-8") as f:
                    conteudo = f.read()
                
                resultado = transliterar_transcricao(conteudo)
                
                with open(caminho_transliteracao, "w", encoding="utf-8") as f:
                    f.write(resultado)
            else:
                st.write("⏭️ Transliteração já existe, pulando...")
            
            videos_processados += 1
            st.success(f"✅ {video} processado com sucesso!")
            
        except Exception as e:
            st.error(f"❌ Erro ao processar {video}: {str(e)}")
            videos_com_erro.append(video)
    
    # Resumo final
    st.success(f"🎉 Processamento concluído!")
    st.info(f"✅ Vídeos processados com sucesso: {videos_processados}")
    
    if videos_com_erro:
        st.warning(f"⚠️ Vídeos com erro: {len(videos_com_erro)}")
        with st.expander("Ver vídeos com erro"):
            for video in videos_com_erro:
                st.write(f"• {video}")

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
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🌐 Canal Completo", "🎬 Vídeo Único", "🎵 Upload de Áudio", "📁 Pasta de Vídeos", "📋 Resultados"])

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
# TAB 4: PASTA DE VÍDEOS
# =========================
with tab4:
    st.header("📁 Processar Vídeos de uma Pasta Local")
    
    st.info("ℹ️ Esta funcionalidade processa vídeos que você já tem salvos localmente em seu computador.")
    
    with st.form("pasta_videos_form"):
        pasta_videos = st.text_input(
            "📂 Caminho da pasta com vídeos:",
            placeholder="C:/MinhasPastas/Videos ou /home/usuario/videos",
            help="Digite o caminho completo da pasta que contém os vídeos"
        )
        
        # Mostrar vídeos encontrados
        if pasta_videos and os.path.exists(pasta_videos):
            videos_encontrados = listar_videos_pasta(pasta_videos)
            
            if videos_encontrados:
                st.success(f"✅ {len(videos_encontrados)} vídeo(s) encontrado(s)")
                
                # Opção para selecionar vídeos específicos
                processar_todos = st.checkbox("🎬 Processar todos os vídeos", value=True)
                
                videos_selecionados = None
                if not processar_todos:
                    videos_selecionados = st.multiselect(
                        "Selecione os vídeos para processar:",
                        videos_encontrados,
                        default=videos_encontrados[:3] if len(videos_encontrados) > 3 else videos_encontrados
                    )
                
                # Mostrar lista de vídeos
                with st.expander("👀 Ver lista de vídeos encontrados"):
                    for i, video in enumerate(videos_encontrados, 1):
                        st.write(f"{i}. {video}")
            else:
                st.warning("⚠️ Nenhum vídeo encontrado na pasta especificada.")
        elif pasta_videos:
            st.error("❌ Pasta não encontrada. Verifique o caminho.")
        
        submitted_pasta = st.form_submit_button("🚀 Processar Vídeos da Pasta", use_container_width=True)

    if submitted_pasta and pasta_videos:
        if not os.path.exists(pasta_videos):
            st.error("❌ Pasta não encontrada. Verifique o caminho.")
        else:
            try:
                videos_para_processar = None
                if not processar_todos and 'videos_selecionados' in locals():
                    videos_para_processar = videos_selecionados
                
                processar_videos_pasta(
                    pasta_videos, 
                    pasta_transcritos, 
                    pasta_transliterados, 
                    modelo_whisper,
                    videos_para_processar
                )
                
            except Exception as e:
                st.error(f"❌ Erro durante o processamento: {str(e)}")
    
    # Seção de ajuda
    with st.expander("❓ Ajuda - Formatos de vídeo suportados"):
        st.write("""
        **Formatos de vídeo suportados:**
        - MP4 (.mp4)
        - AVI (.avi)
        - MOV (.mov)
        - MKV (.mkv)
        - FLV (.flv)
        - WMV (.wmv)
        - WebM (.webm)
        - M4V (.m4v)
        - 3GP (.3gp)
        
        **Requisitos:**
        - FFmpeg deve estar instalado no sistema
        - Pasta deve existir e ser acessível
        - Vídeos devem ter áudio para transcrição
        """)

# =========================
# TAB 5: RESULTADOS
# =========================
with tab5:
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