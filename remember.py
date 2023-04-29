import sys, shutil, os
from esp_polish_transcription import esp_to_polish

if __name__ == "__main__":
    if (len(sys.argv) < 4):
        print("Usage: %s 'esp_txt' 'pol_txt' 'male1'" % sys.argv[0])
        sys.exit(0)

esp_txt = sys.argv[1]
pol_txt = sys.argv[2]
voice_name = sys.argv[3]
[esp_txt_spaced, pol_txt_original] = esp_to_polish(esp_txt)


print("esp_txt: %s\npol_txt: %s\nvoice_name: %s" % (esp_txt, pol_txt, voice_name))
#esp_txt pol_txt를 공백 구분으로 쪼개서
if esp_txt == '' or pol_txt == '':
    sys.exit(0)

esp_words = esp_txt.split(' ')
pol_words = pol_txt.split(' ')
pol_original_words = pol_txt_original.split(' ')

if len(esp_words) != len(pol_words) or len(esp_words) != len(pol_original_words):
    sys.exit(0)

# 1. 불필요한 항목은 저장하지 않는다 - 에스페란토 단어(A B C)와 변형된 폴란드어 단어(Ap Bp-x Cp)가 수작업으로 변경 되었으면 Overrides.py에 
# Append하고 만약에 변경작업을 하지 않았으면 저장하지 않는다.
# overrides[‘A’] = ‘Ap’는 저장하지 않고, 
# overrides[‘B] = ‘Bp-x’는 저장한다.
diff_indexes = []
for i, word in enumerate(pol_words):
    if word != pol_original_words[i]:
        diff_indexes.append(i)
for diff_index in diff_indexes:
    esp_word = esp_words[diff_index]        
    pol_word = pol_words[diff_index]        
    fileobj = open('exception_pol.tsv' ,'a')
    fileobj.write("%s\t%s\n" % (esp_word, pol_word))
    fileobj.close()

# 2. output.mp3를 ./sound/(voice_name)/(esp_txt).mp3 로 파일 mv/overwrite하기
mp3_file = "../html/sounds/"+voice_name+'/'+esp_txt+'.mp3'
if os.path.exists("./output.mp3"):
    shutil.move("./output.mp3", mp3_file)

