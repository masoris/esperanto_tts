import googletts, sys, csv, re
from playsound import playsound

exception_esp = {}
with open('exception_esp.tsv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        # if len(row) < 2:
        #     continue
        exception_esp[row[0]] = row[1]

exception_pol = {}
with open('exception_pol.tsv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        # if len(row) < 2:
        #     continue
        exception_pol[row[0]] = row[1]


def normalize_esp_text(esp_txt):
    esp_txt = esp_txt.lower()

    # x를 삿갓문자로 바꾼다.
    esp_txt = esp_txt.replace("cx", "ĉ")
    # esp_txt = esp_txt.replace("Cx", "Ĉ")
    esp_txt = esp_txt.replace("gx", "ĝ")
    # esp_txt = esp_txt.replace("Gx", "Ĝ")
    esp_txt = esp_txt.replace("hx", "ĥ")
    # esp_txt = esp_txt.replace("Hx", "Ĥ")
    esp_txt = esp_txt.replace("jx", "ĵ")
    # esp_txt = esp_txt.replace("Jx", "Ĵ")
    esp_txt = esp_txt.replace("ux", "ŭ")
    # esp_txt = esp_txt.replace("Ux", "Ŭ")
    esp_txt = esp_txt.replace("sx", "ŝ")
    # esp_txt = esp_txt.replace("Sx", "Ŝ")

    esp_txt = esp_txt.replace("!", " !")
    esp_txt = esp_txt.replace(",", " ,")
    esp_txt = esp_txt.replace(".", " .")
    esp_txt = esp_txt.replace("?", " ?")
    # esp_txt = esp_txt.replace("~", " ")
    esp_txt = esp_txt.replace(":", " :")
    esp_txt = esp_txt.replace(";", " ;")
    esp_txt = esp_txt.replace("(", " (")
    esp_txt = esp_txt.replace(")", " )")

    esp_txt = esp_txt.strip()
    esp_txt = re.sub('\s+', ' ', esp_txt)

    return esp_txt

def esp_to_polish(esp_txt):
    esp_txt = normalize_esp_text(esp_txt)

    # 1 > unu, s-ro > sinjoro 등을 바꾼다
    esp_words = esp_txt.split(" ")
    for i, esp_word in enumerate(esp_words):
        if esp_word in exception_esp:
            esp_words[i] = exception_esp[esp_word]
    esp_txt = " ".join(esp_words)

    #특수문자로 공백으로 분리한 esp_txt
    org_esp_txt = esp_txt

    # esperanto입력 문장을 음절 단위로 분해한다.
    esp_txt = esp_txt.replace("a", "a-")
    # esp_txt = esp_txt.replace("A", "A-")
    esp_txt = esp_txt.replace("e", "e-")
    # esp_txt = esp_txt.replace("E", "E-")
    esp_txt = esp_txt.replace("i", "i-")
    # esp_txt = esp_txt.replace("I", "I-")
    esp_txt = esp_txt.replace("o", "o-")
    # esp_txt = esp_txt.replace("O", "O-")
    esp_txt = esp_txt.replace("u", "u-")
    # esp_txt = esp_txt.replace("U", "U-")

    words = esp_txt.split(" ")
    words2 = []
    for word in words:
        if len(word) >= 2:
            if word[-2] == '-':
                word = word[0:-2] + word [-1:]
                words2.append(word)
                continue
        if len(word) >= 1:
            if word[-1] == '-':
                word = word[0:-1]
        words2.append(word)

    esp_txt = " ".join(words2)
    # return esp_txt


    # 폴란드어 문자 변형 규칙을 반영한다. 
    esp_txt = esp_txt.replace('c', 'ts')
    esp_txt = esp_txt.replace('ĉ', 'cz')
    esp_txt = esp_txt.replace('ĝ', 'dż')
    esp_txt = esp_txt.replace('ĥ', 'ch')
    esp_txt = esp_txt.replace('j', 'y')
    esp_txt = esp_txt.replace('i', 'ij')
    esp_txt = esp_txt.replace('ĵ', 'rz')
    esp_txt = esp_txt.replace('ŝ', 'sz')
    esp_txt = esp_txt.replace('ŭ', 'ł')
    esp_txt = esp_txt.replace('v', 'w')
    

    # 에스페란토 억양을 반영한다.
    words = esp_txt.split(" ")
    words2 = []
    for word in words:
        sylables = word.split('-')
        if len(sylables) >= 2:
            sylables[-2] = sylables[-2].replace('a', 'aa')
            sylables[-2] = sylables[-2].replace('e', 'ee')
            sylables[-2] = sylables[-2].replace('i', 'ii')
            sylables[-2] = sylables[-2].replace('o', 'oł')
            sylables[-2] = sylables[-2].replace('u', 'uł')
        word = "-".join(sylables)
        words2.append(word)
    esp_txt = " ".join(words2)
    
    words = esp_txt.split(' ')
    words2 = []
    for word in words:
        sylables = word.split('-')
        word = "-".join(sylables[0:-1]) + sylables[-1]
        words2.append(word)
    esp_txt = " ".join(words2)
    # esp_txt = "-".join(words[0:-1]) + words[-1]

    # 여기에서 온 갓 종류의 예외 처리를 수행한다 
    # ok > ohk 등으로 바꾼다
    esp_words = org_esp_txt.split(" ")
    pol_words = esp_txt.split(" ")
    assert len(esp_words) == len(pol_words), "길이가 다릅니다"
    for i, esp_word in enumerate(esp_words):
        if esp_word in exception_pol:
            pol_words[i] = exception_pol[esp_word]
        # if esp_word in exception.overrides:
        #     pol_words[i] = exception.overrides[esp_word]
    pol_txt = " ".join(pol_words)

    org_esp_txt = org_esp_txt.replace(" !", "!")
    org_esp_txt = org_esp_txt.replace(" ,", ",")
    org_esp_txt = org_esp_txt.replace(" .", ".")
    org_esp_txt = org_esp_txt.replace(" ?", "?")
    # org_esp_txt = org_esp_txt.replace(" ~", "~")
    org_esp_txt = org_esp_txt.replace(" :", ":")
    org_esp_txt = org_esp_txt.replace(" ;", ";")
    org_esp_txt = org_esp_txt.replace(" (", "(")
    org_esp_txt = org_esp_txt.replace(" )", ")")

    pol_txt = pol_txt.replace(" !", "!")
    pol_txt = pol_txt.replace(" ,", ",")
    pol_txt = pol_txt.replace(" .", ".")
    pol_txt = pol_txt.replace(" ?", "?")
    # pol_txt = pol_txt.replace(" ~", "~")
    pol_txt = pol_txt.replace(" :", ":")
    pol_txt = pol_txt.replace(" ;", ";")
    pol_txt = pol_txt.replace(" (", "(")
    pol_txt = pol_txt.replace(" )", ")")

    org_esp_txt = org_esp_txt.strip()
    pol_txt = pol_txt.strip()
    
    return [org_esp_txt, pol_txt]

if __name__ == "__main__":
    if (len(sys.argv) < 4):
        print("Usage: %s -e 'esp_txt' 'male1'" % sys.argv[0])
        print("Usage: %s -p 'pol_txt' 'female1'" % sys.argv[0])
        sys.exit(0)
    voicename = sys.argv[3]
    if (sys.argv[1] == '-e'):
        esp_txt = sys.argv[2]
        if voicename == 'ludoviko':
            googletts.speak(esp_txt, voicename, "output.mp3")
            [esp_txt, pol_txt] = esp_to_polish(esp_txt)
            print("esp_txt=%s\npol_txt=%s" % (esp_txt, pol_txt))
        else:
            [esp_txt, pol_txt] = esp_to_polish(esp_txt)
            print("esp_txt=%s\npol_txt=%s" % (esp_txt, pol_txt))
            googletts.speak(pol_txt, voicename, "output.mp3")

        # playsound("output.mp3")
    else:
        pol_txt = sys.argv[2]
        print("pol_txt=%s" % (pol_txt))
        googletts.speak(pol_txt, voicename, "output.mp3")

        # playsound("output.mp3")

