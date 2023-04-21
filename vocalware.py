import requests



url = "https://cache-a.oddcast.com/tts/gen.php?EID=2&LID=31&VID=1&TXT=Longan%20Tempon%2C%20Mi%20estas%20Masoris.%20Bonan%20tagon.&IS_UTF8=1&ACC=3314795&API=2292376&CB=vw_mc.vwCallback&HTTP_ERR=1&vwApiVersion=2&d=f88dda1b76a1b76931320d9f8810330ee9f6df88dd"
referer = "https://vocalware.com"

response = requests.get(url, headers={"Referer": referer})

if response.status_code == 200:
    with open("somepage.mp3", "wb") as f:
        f.write(response.content)
else:
    print(f"Failed to fetch {url}")