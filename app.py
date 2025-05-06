import streamlit as st
import os
import io
from pydub import AudioSegment
import openai
from dotenv import load_dotenv
import re

# .envから環境変数をロード
load_dotenv()

# --- 設定 ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TTS_MODEL = "tts-1"
VOICE_OPTIONS = ["nova", "shimmer", "echo", "onyx", "fable", "alloy", "ash", "sage", "coral"]

# --- UI雛形 ---
st.title("AudioOverviewGenerator")

scenario_file = st.file_uploader("シナリオファイルをアップロード", type=["txt", "md", "json"], key="scenario_file")

# キャラ名抽出用関数
def extract_char_names(text):
    # 「キャラ名:」で始まる行からキャラ名を抽出
    names = set()
    for line in text.splitlines():
        m = re.match(r"^([\wぁ-んァ-ヶ一-龠々ー・\u30A0-\u30FF\u3040-\u309F\u4E00-\u9FFF]+):", line.strip())
        if m:
            names.add(m.group(1))
    return list(names)

char_names = []
char_voices = []

if scenario_file:
    raw_bytes = scenario_file.read()
    try:
        scenario_text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        try:
            scenario_text = raw_bytes.decode("shift_jis")
        except UnicodeDecodeError:
            scenario_text = raw_bytes.decode("cp932", errors="replace")
    char_names = extract_char_names(scenario_text)
    st.write(f"抽出された登場人物: {', '.join(char_names)}")
    for i, name in enumerate(char_names):
        voice = st.selectbox(f"{name} の声を選択", options=VOICE_OPTIONS, key=f"char_voice_{i}")
        char_voices.append(voice)

# --- 音声生成・結合処理 ---
def parse_scenario(text, char_names):
    """
    シナリオテキストを「キャラ名: セリフ」形式で分割し、
    [{name, voice, text}] のリストを返す
    空行や余計なスペースがあってもスキップする
    """
    lines = text.splitlines()
    result = []
    for line in lines:
        line = line.strip()
        if not line:
            continue  # 空行スキップ
        for idx, name in enumerate(char_names):
            if line.startswith(f"{name}:"):
                content = line[len(name)+1:].strip()
                if content:
                    result.append({"name": name, "voice": char_voices[idx], "text": content})
                break
    return result

def tts_generate(text, voice, api_key):
    """
    OpenAI TTS APIで音声合成し、MP3バイトデータを返す
    """
    client = openai.OpenAI(api_key=api_key)
    response = client.audio.speech.create(
        model=TTS_MODEL,
        voice=voice,
        input=text,
        response_format="mp3"
    )
    return io.BytesIO(response.content)

if 'audio_bytes' not in st.session_state:
    st.session_state['audio_bytes'] = None

if st.button("MP3ファイル生成", key="generate_mp3"):
    if not OPENAI_API_KEY:
        st.error("OpenAI APIキーが設定されていません。環境変数OPENAI_API_KEYをセットしてください。")
    elif not scenario_file or not char_names or not char_voices or len(char_names) != len(char_voices):
        st.error("シナリオファイルと全ての登場人物の声を選択してください。")
    else:
        parsed = parse_scenario(scenario_text, char_names)
        if not parsed:
            st.error("シナリオ形式が正しくありません。『キャラ名: セリフ』形式で記述してください。")
        else:
            audio_segments = []
            for part in parsed:
                try:
                    audio_io = tts_generate(part["text"], part["voice"], OPENAI_API_KEY)
                    audio = AudioSegment.from_file(audio_io, format="mp3")
                    audio_segments.append(audio)
                except Exception as e:
                    st.error(f"TTS生成エラー: {e}")
                    break
            if audio_segments:
                combined = audio_segments[0]
                for seg in audio_segments[1:]:
                    combined += seg
                buf = io.BytesIO()
                combined.export(buf, format="mp3")
                st.session_state['audio_bytes'] = buf.getvalue()
                st.success("MP3生成が完了しました。下の再生・ダウンロードボタンからご利用ください。")

if st.session_state.get('audio_bytes'):
    st.audio(st.session_state['audio_bytes'], format="audio/mp3", start_time=0)
    st.download_button("MP3をダウンロード", data=st.session_state['audio_bytes'], file_name="script_output.mp3", mime="audio/mpeg", key="download_mp3")
else:
    st.audio(b"", format="audio/mp3", start_time=0)
    st.download_button("MP3をダウンロード", data=b"", file_name="script_sample.mp3", mime="audio/mpeg", key="download_mp3")

# --- APIエンドポイント雛形（今後FastAPI等で分離予定） ---
# def create_audio():
#     pass  # 実装予定 