# https://eo.wikipedia.org/wiki/Vortoj_por_grandegaj_nombroj

import sys, re

def simple_number(number_str:str) -> str:
    '''
    자리수를 무시하고 숫자를 하나하나 읽어주는 함수.
    입력: "1234567.89"
    출력: "unu du tri kvar kvin ses sep punkto ok naŭ"
    '''
    num_words = {'0': "nul", '1': "unu", '2': "du", '3': "tri", '4': "kvar", '5': "kvin",
                 '6': "ses", '7': "sep", '8': "ohk", '9': "nał", ',': "komo", '.': "punkto"}
    if number_str == "":
        return ""

    result = ""
    for i in number_str:
        result += num_words[i]+" "
    
    return result.strip()

def number_to_words(number_str:str) -> str:
    '''
    실수를 에스페란토로 읽어주는 함수.
    입력: "1234567.89"
    출력: "unu miliono ducent tridek kvar mil kvincent sesdek sep punkto ok naŭ"
    주의사항: 최대 '2 triiliono' 미만의 숫자(1999999999999999999.999...)까지 변환 가능.
        콤마가 포함되었거나, 점이 2개 이상 있는 경우 오류가 발생하지 않고, simple_number 함수에 의해 처리됨.
    '''
    n = number_str #정수 부분 int
    m = "" #소수점 이하 str
    final = ""

    if n == "":
        return ""

    if n.count('.') >= 2 or n.count(',') >= 1:
        return simple_number(n)

    if n.count('.') == 1: # 소수점이 하나 있을 경우
        n = n.split('.')
        (n, m) = (int(n[0]), n[1]) # 정수와 소수점 이하 분리하기

    if len(m) > 0: #소수점 이하 처리
        final = " punkto " + simple_number(m)
    
    n = int(n)

    if n == 0:
        return "nul"

    # Define the number mappings
    num_words = {0: "", 1: "unu", 2: "du", 3: "tri", 4: "kvar", 5: "kvin",
                 6: "ses", 7: "sep", 8: "ohk", 9: "nał"}

    def words_under_1000(number):
        if number < 10:
            return num_words[number]
        elif number < 100:
            return num_words[number // 10] + "dek" + (" " + num_words[number % 10] if number % 10 != 0 else "")
        else:
            return num_words[number // 100] + "cent" + (" " + words_under_1000(number % 100) if number % 100 != 0 else "")

    # Build the word representation
    result = ""
    if n >= 1000000000000000000:
        result += simple_number(str (n // 1000000000000000000)) + " triiliono "
        n %= 1000000000000000000
    if n >= 2000000000000000:
        result += words_under_1000(n // 1000000000000000) + " duiliardoj "
        n %= 1000000000000000
    elif n >= 1000000000000000:
        result += words_under_1000(n // 1000000000000000) + " duiliardo "
        n %= 1000000000000000
    if n >= 2000000000000:
        result += words_under_1000(n // 1000000000000) + " duilionoj "
        n %= 1000000000000
    elif n >= 1000000000000:
        result += words_under_1000(n // 1000000000000) + " duiliono "
        n %= 1000000000000
    if n >= 2000000000:
        result += words_under_1000(n // 1000000000) + " miliardoj "
        n %= 1000000000
    elif n >= 1000000000:
        result += words_under_1000(n // 1000000000) + " miliardo "  
        n %= 1000000000      
    if n >= 2000000:
        result += words_under_1000(n // 1000000) + " milionoj "
        n %= 1000000
    elif n >= 1000000:
        result += words_under_1000(n // 1000000) + " miliono "
        n %= 1000000
    if n >= 1000:
        result += words_under_1000(n // 1000) + " mil "
        n %= 1000
    if n > 0:
        result += words_under_1000(n)
    result = result + final

    return result.strip()


#ChatGPT로 만듬
def separate_letters_and_numbers(s:str) -> list:
    '''
    문자와 숫자를 분리하는 파이썬 코드
    입력: a123bc456
    출력: ["a", 123, "bc", 456]
    '''
    result = []
    current = ""

    for char in s:
        if char.isdigit() and (not current.isdigit()):
            if current:
                result.append(current)
            current = char
        elif not char.isdigit() and current.isdigit():
            result.append(int(current))
            current = char
        else:
            current += char

    # Add the last accumulated segment
    if current:
        if current.isdigit():
            result.append(int(current))
        else:
            result.append(current)

    return result

#ChatGPT 
def is_only_float(s:str) -> bool:
    '''입력된 문자열에 실수만 포함되어있는지 알아내는 함수'''
    pattern = r'^-?\d+(\.\d+)?$'
    return bool(re.match(pattern, s))

#ChatGPT
def is_only_numbers(s:str) -> bool:
    '''문자열에 숫자만 있는가?'''
    return all(char.isdigit() for char in s)

def number_to_words_with_text(text:str) -> str:
    '''
    숫자와 문자가 섞여 있는 string 에서 숫자를 에스페란토로 바꾸어 주는 함수
    입력: "1234567.89 personoj"
    출력: "unu miliono ducent tridek kvar mil kvincent sesdek sep.okdek naŭ personoj"
    주의사항: 소수점 이하가 있는 실수는 제대로 처리하지 못한다. 실수 처리는 number_to_words 함수를 이용할 것.
    '''
    text_list = separate_letters_and_numbers(text)
    result = ""
    for i in text_list:
        i = str(i)
        if is_only_numbers(i):
            result+= number_to_words(i)
        else:
            result+= i
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("USAGE: %s text with numbers" % sys.argv[0])
        sys.exit(0)
    
    text = ' '.join(sys.argv[1:])
    print(number_to_words_with_text(text))

    # number_string = text
    # print(number_to_words(text))