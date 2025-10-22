from pathlib import Path
from datetime import datetime
import time
import queue

from streamlit_webrtc import WebRtcMode, webrtc_streamer
import streamlit as st

import pydub
import openai

PASTA_ARQUIVOS = Path(__file__).parent / 'arquivos'
PASTA_ARQUIVOS.mkdir(exist_ok=True)

PROMPT = '''
Faça o reumo do texto delimitado por #### 
O texto é a transcrição de uma reunião.
O resumo deve contar com os principais assuntos abordados.
O resumo deve ter no máximo 300 caracteres.
O resumo deve estar em texto corrido.
No final, devem ser apresentados todos acordos e combinados 
feitos na reunião no formato de bullet points.

O formato final que eu desejo é:

Resumo reunião:
- escrever aqui o resumo.

Acordos da Reunião:
- acrodo 1
- acordo 2
- acordo 3
- acordo n

texto: ####{}####
'''


def salva_arquivo(caminho_arquivo, conteudo):
    with open(caminho_arquivo, 'w') as f:
        f.write(conteudo)

def le_arquivo(caminho_arquivo):
    if caminho_arquivo.exists():
        with open(caminho_arquivo) as f:
            return f.read()
    else:
        return ''

def listar_reunioes():
    lista_reunioes = PASTA_ARQUIVOS.glob('*')
    lista_reunioes = list(lista_reunioes)
    lista_reunioes.sort(reverse=True)
    reunioes_dict = {}
    for pasta_reuniao in lista_reunioes:
        data_reuniao = pasta_reuniao.stem
        ano, mes, dia, hora, min, seg = data_reuniao.split('_')
        reunioes_dict[data_reuniao] = f'{ano}/{mes}/{dia} {hora}:{min}:{seg}'
        titulo = le_arquivo(pasta_reuniao / 'titulo.txt')
        if titulo != '':
            reunioes_dict[data_reuniao] += f' - {titulo}'
    return reunioes_dict


# OPENAI UTILS ====================
def transcreve_audio(openai_key, caminho_audio, language='pt', response_format='text'):
    # Cria um client do OpenAI usando a chave passada como argumento
    client = openai.OpenAI(api_key=openai_key)
    with open(caminho_audio, 'rb') as arquivo_audio:
        transcricao = client.audio.transcriptions.create(
            model='whisper-1',
            language=language,
            response_format=response_format,
            file=arquivo_audio,
        )
    return transcricao


def chat_openai(openai_key, mensagem, modelo='gpt-3.5-turbo-1106'):
    # Cria um client do OpenAI usando a chave passada como argumento
    client = openai.OpenAI(api_key=openai_key)
    mensagens = [{'role': 'user', 'content': mensagem}]
    resposta = client.chat.completions.create(
        model=modelo,
        messages=mensagens,
    )
    return resposta.choices[0].message.content

# TAB GRAVA REUNIÃO =====================

def adiciona_chunck_audio(frames_de_audio, audio_chunck):
    for frame in frames_de_audio:
        sound = pydub.AudioSegment(
            data=frame.to_ndarray().tobytes(),
            sample_width=frame.format.bytes,
            frame_rate=frame.sample_rate,
            channels=len(frame.layout.channels),
        )
        audio_chunck += sound
    return audio_chunck

def tab_grava_reuniao():
    webrtx_ctx = webrtc_streamer(
        key='recebe_audio',
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        media_stream_constraints={'video': False, 'audio': True},
    )

    if not webrtx_ctx.state.playing:
        return

    container = st.empty()
    container.markdown('Comece a falar, estou gravando ...')
    pasta_reuniao = PASTA_ARQUIVOS / datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    pasta_reuniao.mkdir()

    ultima_trancricao = time.time()
    audio_completo = pydub.AudioSegment.empty()
    audio_chunck = pydub.AudioSegment.empty()
    transcricao = ''

    while True:
        if webrtx_ctx.audio_receiver:
            try:
                frames_de_audio = webrtx_ctx.audio_receiver.get_frames(timeout=1)
            except queue.Empty:
                time.sleep(0.1)
                continue
            audio_completo = adiciona_chunck_audio(frames_de_audio, audio_completo)
            audio_chunck = adiciona_chunck_audio(frames_de_audio, audio_chunck)
            if len(audio_chunck) > 0:
                audio_completo.export(pasta_reuniao / 'audio.mp3')
                agora = time.time()
                if agora - ultima_trancricao > 5:
                    ultima_trancricao = agora
                    audio_chunck.export(pasta_reuniao / 'audio_temp.mp3')
                    transcricao_chunck = transcreve_audio(st.session_state['api_key'],pasta_reuniao / 'audio_temp.mp3')
                    transcricao += transcricao_chunck
                    salva_arquivo(pasta_reuniao / 'transcricao.txt', transcricao)
                    container.markdown(transcricao)
                    audio_chunck = pydub.AudioSegment.empty()
        else:
            break


# TAB SELEÇÃO REUNIÃO =====================
def tab_selecao_reuniao():
    reunioes_dict = listar_reunioes()
    if len(reunioes_dict) > 0:
        reuniao_selecionada = st.selectbox('SELECIONE UMA REUNIÃO:',
                                        list(reunioes_dict.values()))
        st.divider()
        reuniao_data = [k for k, v in reunioes_dict.items() if v == reuniao_selecionada][0]
        pasta_reuniao = PASTA_ARQUIVOS / reuniao_data
        if not (pasta_reuniao / 'titulo.txt').exists():
            st.warning('Adicione um titulo')
            titulo_reuniao = st.text_input('Título da reunião')
            st.button('Salvar',
                      on_click=salvar_titulo,
                      args=(pasta_reuniao, titulo_reuniao))
        else:
            titulo = le_arquivo(pasta_reuniao / 'titulo.txt')
            transcricao = le_arquivo(pasta_reuniao / 'transcricao.txt')
            resumo = le_arquivo(pasta_reuniao / 'resumo.txt')
            if resumo == '':
                gerar_resumo(pasta_reuniao)
                resumo = le_arquivo(pasta_reuniao / 'resumo.txt')
            st.markdown(f'## {titulo}')
            st.markdown(f'{resumo}')
            st.markdown(f'Transcricao: {transcricao}')
        
def salvar_titulo(pasta_reuniao, titulo):
    salva_arquivo(pasta_reuniao / 'titulo.txt', titulo)

def gerar_resumo(pasta_reuniao):
    transcricao = le_arquivo(pasta_reuniao / 'transcricao.txt')
    resumo = chat_openai(st.session_state['api_key'],mensagem=PROMPT.format(transcricao))
    salva_arquivo(pasta_reuniao / 'resumo.txt', resumo)


# TAB CONFIGURACAO API KEY =====================
def tab_configuracao():
    
    st.subheader("Configuração da API Key")

    # Exibe o valor atual (se houver) mas com ocultação de texto
    api_key = st.text_input(
        "Adicione sua API KEY da OpenAI:",
        type="password",
        value=st.session_state.get("api_key", ""),
        key="input_api_key"  #  key única
    )

    if st.button("Salvar", key="btn_salvar_api"):  #  key única
        if api_key:
            st.session_state["api_key"] = api_key
            st.success("✅ Chave salva com sucesso!")
        else:
            st.warning("⚠️ Por favor, insira uma chave válida antes de salvar.")
    
    

# MAIN =====================
def main():
    
    if 'api_key' not in st.session_state:
        st.session_state['api_key'] = ""
    
    st.header('Bem-vindo ao MeetGPT - Transcrição de Reuniões 🎙️', divider=True)
    tab_gravar, tab_selecao, tab_configurar = st.tabs(['Gravar Nova Reunião', 'Ver Transcrições/Reuniões Salvas', 'Configuração da API KEY'])
    with tab_gravar:
        tab_grava_reuniao()
    with tab_selecao:
        tab_selecao_reuniao()
    with tab_configurar:
        tab_configuracao()

if __name__ == '__main__':
    main()