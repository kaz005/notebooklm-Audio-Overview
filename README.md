# AudioOverviewGenerator

## 概要

AudioOverviewGeneratorは、StreamlitベースのWebアプリです。シナリオファイル（会話台本）をアップロードし、登場人物ごとに声を選択して、OpenAI TTS APIでMP3音声を自動生成・ダウンロードできます。

---

## 技術スタック
- Python 3.8以降
- [Streamlit](https://streamlit.io/)（Web UI）
- [OpenAI API](https://platform.openai.com/docs/guides/text-to-speech)（TTS音声合成）
- [pydub](https://github.com/jiaaro/pydub)（音声結合）
- [python-dotenv](https://github.com/theskumar/python-dotenv)（APIキー管理）
- [ruamel.yaml](https://pypi.org/project/ruamel.yaml/)（YAML処理/拡張用）

---

## セットアップ手順

1. **リポジトリをクローン**
2. **仮想環境の作成・有効化**
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **依存パッケージのインストール**
   ```sh
   pip install -r requirements.txt
   ```
4. **OpenAI APIキーの設定**
   プロジェクトルートに `.env` ファイルを作成し、下記のように記載してください。
   ```
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
5. **アプリの起動**
   ```sh
   streamlit run app.py
   ```

---

## 使い方

1. **シナリオファイルをアップロード**
   - ファイル形式: `.txt`, `.md`, `.json`（推奨はUTF-8テキスト）
   - フォーマット例：
     ```
     太郎: こんにちは、花子さん。
     花子: こんにちは、太郎くん。今日はいい天気ですね。
     太郎: そうですね。散歩に行きませんか？
     花子: いいですね、行きましょう！
     ```
   - 登場人物名は「キャラ名:」で自動抽出されます。
2. **各キャラの声を選択**
   - 選択肢例: `nova`, `shimmer`, `echo`, `onyx`, `fable`, `alloy`, `ash`, `sage`, `coral`
3. **「MP3ファイル生成」ボタンを押す**
   - OpenAI TTS APIで各セリフを音声合成し、1つのMP3に結合
4. **音声の再生・ダウンロード**
   - 生成されたMP3をその場で再生・ダウンロード可能

---

## シナリオファイル定義
- 1行ごとに「キャラ名: セリフ」形式（コロンは半角）
- 登場人物名は日本語・英語どちらも可
- 空行や余計な行は含めないこと（会話のみ）
- 例：
  ```
  アキラ: 皆さん、こんにちは。
  ミホ: 今回は最新動向をお伝えします。
  ```

---

## 注意事項・エラー対策
- OpenAI APIキーは有効なものを使用してください（401エラー時はキーを再確認）
- voiceパラメータはAPI仕様に従ってください（例: `olivia`や`luna`は不可）
- シナリオファイルの文字コードはUTF-8推奨（自動判別あり）
- 1ファイルの長さ・APIレート制限に注意

---

## ライセンス
MIT License 