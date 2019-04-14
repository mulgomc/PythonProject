#cmd_list : 명령어의 종류
cmd_list = ['A', 'D', 'F', 'M', 'P', 'R', 'S', 'Q', 'W']
#db_attribute : 데이터의 속성명칭
db_attribute = ['일련번호', '학생 id', '이름', '생년월일', '중간고사', '기말고사', '평균', 'Grade']
#db_data : 실질적인 데이터, 각 사람별로 nested list 형식으로 저장됨, 생년월일은 모두 각각 따로 저장됨
db_data = []
#생년월일 체크를 위한 윤년 계산기
def leap_year(year):
    if (year%4==0 and year%100!=0) or year%400==0:
        return True
    return False
#올바른 생년월일인지 판별하는 함수
def valid_date(y,m,d):
    cal = [31,28,31,30,31,30,31,31,30,31,30,31]
    if y<0:
        return False
    if m<0 or m>12:
        return False
    if d<0 or (leap_year(y) and m==2 and d>29) or (leap_year(y) and m!=2 and d>cal[m-1]) or ((not leap_year(y)) and d>cal[m-1]):
        return False
    return True
#파일의 포멧이 잘못되었을때 에러를 출력하는 함수
def print_format_error(num, chk):
    print(f"file format error in {db_attribute[chk]} on line {num}!")
#파일의 데이터가 잘못되었을때 에러를 출력하는 함수
def print_data_error(num, chk):
    print(f"file data error in {db_attribute[chk]} on line {num}!")
#파일의 한줄을 파싱하는 함수
def parse_file(num, line):    
    temp = []
    chk = 0
    try:        
        temp.append(int(line[0])); chk+=1        
        temp.append(str(line[1])); chk+=1        
        temp.append(str(line[2])); chk+=1        
        temp.append(int(line[3].split('-')[0]))
        temp.append(int(line[3].split('-')[1]))
        temp.append(int(line[3].split('-')[2])); chk+=1  
        temp.append(int(line[4])); chk+=1        
        temp.append(int(line[5])); chk+=1        
        if len(line)>=7:
            temp.append(float(line[6])); chk+=1        
        if len(line)==8:
            temp.append(str(line[7])); chk+=1        
    except:
        print_format_error(num, chk)
        return [-1]
    
    if not valid_date(temp[3], temp[4], temp[5]):
        print_data_error(num, 3)
        return [-1]

    if temp[6]<0 or temp[6]>100:
        print_data_error(num, 4)
        return [-1]

    if temp[7]<0 or temp[7]>100:
        print_data_error(num, 5)
        return [-1]

    if len(temp)>=9:
        if (temp[8]<0 or temp[8]>100) or (temp[8]!=(temp[6]+temp[7])/2):
            print_data_error(num, 6)
            return [-1]   
    return temp
#파일 전체를 읽는 함수
def read_file():
    f_data = result = []    
    global db_data
    try:
        with open('data.txt', 'r') as f:
            f_data = f.readlines()
    except:
        print('Could not open file.')
    for num, i in zip(range(len(f_data)), f_data):        
        line = parse_file(num+1, i.replace('\n',"").split('\t'))   
        if line==[-1]:
            return [-1]
        else:
            result.append(line)
    db_data = result
#사용자로부터 적합한 명령 입력을 요구하는 함수
def input_cmd():
    while True:
        try:
            x = str(input("Choose one of the options below : ")).upper()
        except:
            print("Wrong input\n")
            continue
        if x in cmd_list:
            return x
        print("Wrong input\n")

#!!!각 명령별 작업 코드!!!!
def pcs_a():
    print("Process A")
def pcs_d():
    print("Process D")
def pcs_f():
    print("Process F")
def pcs_m():
    print("Process M")
def pcs_p():
    print("Process P")
    #테스트용 대충 인쇄
    for i in db_data:
        print(i)
def pcs_r():
    print("Process R")
    #테스트용 대충 읽기
    read_file()
def pcs_s():
    print("Process S")
def pcs_q():
    print("Process Q")
def pcs_w():
    print("Process W")

while True:
    cmd = input_cmd()
    if cmd == 'A':
        pcs_a()
    elif cmd == 'D':
        pcs_d()
    elif cmd == 'F':
        pcs_f()
    elif cmd == 'M':
        pcs_m()
    elif cmd == 'P':
        pcs_p()
    elif cmd == 'R':
        pcs_r()
    elif cmd == 'S':
        pcs_s()
    elif cmd == 'Q':
        break
    elif cmd == 'W':
        pcs_w()
    print('')