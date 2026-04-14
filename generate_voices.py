import urllib.request
import urllib.parse
import json
import os

SPEAKER_ID = 13
VOICEVOX_URL = "http://localhost:50021"
OUTPUT_DIR = "voices"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate(text, filename):
    print(f"生成中: {text} -> {filename}")

    # audio_query
    query_url = f"{VOICEVOX_URL}/audio_query?text={urllib.parse.quote(text)}&speaker={SPEAKER_ID}"
    req = urllib.request.Request(query_url, method="POST")
    with urllib.request.urlopen(req) as res:
        query = json.loads(res.read())

    # synthesis
    synth_url = f"{VOICEVOX_URL}/synthesis?speaker={SPEAKER_ID}"
    body = json.dumps(query).encode("utf-8")
    req2 = urllib.request.Request(synth_url, data=body, method="POST")
    req2.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req2) as res2:
        audio = res2.read()

    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(audio)

# 時（0〜23時）
for h in range(24):
    generate(f"{h}時", f"h_{h}.wav")

# 分（0〜59分）
for m in range(60):
    generate(f"{m}分", f"m_{m}.wav")

# 秒（15・30・45秒）
for s in [15, 30, 45]:
    generate(f"{s}秒", f"s_{s}.wav")

print("\n完了！voicesフォルダに音声ファイルが生成されました。")