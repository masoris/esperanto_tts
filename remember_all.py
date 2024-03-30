
import sys, json, tts, transcription

def remember_all(esp_txt):
    [eo_txt, pol_txt] = transcription.esp_to_polish(esp_txt)
    tts.remember_all_args(esp_txt, pol_txt, esp_txt)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("USAGE: %s filename.js" % sys.argv[0])
        sys.exit(0)
    file = sys.argv[1]
    fp = open(file, "r")
    for i, line in enumerate(fp):
        if i % 10 == 0:
            print("%d" % i)
        line = line.strip()
        print (line[0])
        print (line[-2:])
        if line[0] == "'" and line[-2:] == "',":
            remember_all(line[1:-2])
    fp.close()