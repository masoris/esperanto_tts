import os, requests
from google.cloud import texttospeech
from playsound import playsound
from urllib.parse import quote

def speak(esp_txt, voicename, output_mp3):
    if voicename=="ludoviko":
        vocalwave_tts_esperanto(esp_txt, voicename, output_mp3)
    else:
        google_tts_polish(esp_txt, voicename, output_mp3)

def vocalwave_tts_esperanto(esp_txt, voicename, output_mp3):
    esp_txt = esp_txt.replace("ĉ", "cx")
    # esp_txt = esp_txt.replace("Cx", "Ĉ")
    esp_txt = esp_txt.replace("ĝ", "gx")
    # esp_txt = esp_txt.replace("Gx", "Ĝ")
    esp_txt = esp_txt.replace("ĥ", "hx")
    # esp_txt = esp_txt.replace("Hx", "Ĥ")
    esp_txt = esp_txt.replace("ĵ", "jx")
    # esp_txt = esp_txt.replace("Jx", "Ĵ")
    esp_txt = esp_txt.replace("ŭ", "ux")
    # esp_txt = esp_txt.replace("Ux", "Ŭ")
    esp_txt = esp_txt.replace("ŝ", "sx")

    url = "https://cache-a.oddcast.com/tts/gen.php?EID=2&LID=31&VID=1&TXT=" + quote(esp_txt) + "&IS_UTF8=1&ACC=3314795&API=2292376&CB=vw_mc.vwCallback&HTTP_ERR=1&vwApiVersion=2&d=f88dda1b76a1b76931320d9f8810330ee9f6df88dd"
    referer = "https://vocalware.com"

    response = requests.get(url, headers={"Referer": referer})

    if response.status_code == 200:
        with open(output_mp3, "wb") as f:
            f.write(response.content)
    else:
        print(f"Failed to fetch {url}")

def google_tts_polish(inputtxt, voicename, output_mp3):
    # 폴란드어 음성에서 ~를 틸다라고 발음하지 않도록 막는다.
    inputtxt = inputtxt.replace("~", "")
    # 인증 정보 설정
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "my-project-tts-383606-c4e8939e2840.json"

    # Text-to-Speech API 클라이언트 생성
    client = texttospeech.TextToSpeechClient()

    # 음성 합성 매개변수 구성
    synthesis_input = texttospeech.SynthesisInput(text = inputtxt) 
    # voice = texttospeech.VoiceSelectionParams(
    #     language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    # )
    if voicename == "male1": voicename = "pl-PL-Standard-B"
    if voicename == "male2": voicename = "pl-PL-Standard-C"
    if voicename == "male3": voicename = "pl-PL-Wavenet-B"
    if voicename == "female1": voicename = "pl-PL-Standard-A"
    if voicename == "female2": voicename = "pl-PL-Standard-D"
    if voicename == "female3": voicename = "pl-PL-Wavenet-A"
    
    voice_conf = texttospeech.VoiceSelectionParams(
        language_code="pl-PL",
        name = voicename,
        # name="pl-PL-Wavenet-B", # 남성 목소리
        ssml_gender=texttospeech.SsmlVoiceGender.MALE
        # pl-PL-Standard-A 여성1
        # pl-PL-Standard-B 남성1
        # pl-PL-Standard-C 남성2
        # pl-PL-Standard-D 여성2
        # pl-PL-Wavenet-A 여성3
        # pl-PL-Wavenet-B 남성3
        # language_code="pl-PL", # 폴란드어
        # ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL # 음성 성별
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    if os.path.exists("./output.mp3"):
        os.remove("output.mp3")
    
    # 음성 합성 요청 보내기
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice_conf, audio_config=audio_config
    )

    # 출력 파일로 저장
    with open(output_mp3, "wb") as out:
        out.write(response.audio_content)

# google_tts_polish("Saluton mi amas vin", "male1", "output.mp3")
# 파일 재생
