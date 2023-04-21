import sys, esp_polish_transcription

if __name__ == "__main__":
    if (len(sys.argv) < 4):
        print("Usage: %s 'esp_txt' 'pol_txt' 'male1'" % sys.argv[0])
        sys.exit(0)

esp_txt = sys.argv[1]
pol_txt = sys.argv[2]
voice_name = sys.argv[3]

print("esp_txt: %s\npol_txt: %s\nvoice_name: %s" % (esp_txt, pol_txt, voice_name))
#esp_txt pol_txt를 공백 구분으로 쪼개서
if esp_txt == '' or pol_txt == '':
    sys.exit(0)

esp_lines=esp_txt.split(' ')
pol_lines=pol_txt.split(' ')

if len(esp_lines) != len(pol_lines):
    sys.exit(0)

#esp[i] pol[i] 각 쌍에 대해서 
#pol[i]가 esp[i]의 transcription 결과면 무시하고

fileobj = open('exception_pol.tsv' ,'at')
for i in range(len(esp_lines)):
    if esp_polish_transcription.esp_to_polish(esp_lines[i]) != pol_lines[i]:
        #그렇지 않으면 exception.py에
        #overrides[esp[i]] = pol[i] 라인을 append해준다
        fileobj.write("\n%s\t%s" % (esp_lines[i], pol_lines[i]))
fileobj.close()


#output.mp3를 ./sound/(voice_name)/(esp_txt).mp3 로 파일 mv/overwrite하기
