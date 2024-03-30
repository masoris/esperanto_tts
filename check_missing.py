import os

courses = "../memlingo/courses"
sounds = "../memlingo/sounds"

def find_pattern_files(directory, pattern):
    mp3_files = []
    
    # 디렉토리 안의 모든 항목에 대해 반복
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 파일이 .mp3 확장자를 가지고 있는지 확인
            if file.endswith(pattern):
                # *.mp3 파일을 찾았으므로 경로를 mp3_files 리스트에 추가
                mp3_files.append(os.path.join(root, file))
    
    return mp3_files

# find_mp3_files 함수를 호출하여 *.mp3 파일을 찾고 결과를 출력
mp3s = find_pattern_files(sounds, '.mp3')
mp3_dict = {}
for mp3_file in mp3s:
    row = mp3_file.split('/')
    mp3_dict[row[-1][0:-4]] = True
    # print(row[-1])

tsvs = find_pattern_files(courses, '.tsv')
for tsv_file in tsvs:
    fp = open(tsv_file, "r")
    for line in fp:
        row = line.split('\t')
        esp = row[1]
        if not esp in mp3_dict:
            print(esp)
            # pass
    fp.close()
