#한글 줄맞춤 출력을 위한 unicode
import unicodedata
#cmd_list : 명령어의 종류
cmd_list = ['A', 'D', 'F', 'M', 'P', 'R', 'S', 'Q', 'W']
#db_attribute : 데이터의 속성명칭
db_attribute = ['일련번호', '학생 id', '이름', '생년월일', '중간고사', '기말고사', '평균', 'Grade']
#db_data : 실질적인 데이터, 각 사람별로 nested list 형식으로 저장됨, 생년월일은 모두 각각 따로 저장됨
db_data = []

def preformat_cjk (string, width, align='>', fill=' '):
    count = (width - sum(1 + (unicodedata.east_asian_width(c) in "WF")
                         for c in string))
    return {
        '>': lambda s: fill * count + s,
        '<': lambda s: s + fill * count,
        '^': lambda s: fill * (count / 2)
                       + s
                       + fill * (count / 2 + count % 2)
}[align](string)



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
    except:
        print_format_error(num, chk)
        return [-1]
    
    count = sum(1 + (unicodedata.east_asian_width(c) in "WF") for c in temp[1])
    if count>10:
        print(f"Too long name! on line{num}")
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

    temp.append((temp[6] + temp[7]) / 2)
    if temp[8]>=90:
        temp.append('A')
    elif temp[8]>=70:
        temp.append('B')
    elif temp[8]>=50:
        temp.append('C')
    elif temp[8]>=30:
        temp.append('D')
    else :
        temp.append('F')

    return temp
#파일 전체를 읽는 함수
def read_file(filename):
    f_data = result = []    
    global db_data
    try:
        with open(filename, 'r') as f:
            f_data = f.readlines()
    except:
        print('Could not open file.')
    else:
        for num, i in zip(range(len(f_data)), f_data):        
            line = parse_file(num+1, i.replace('\n',"").split('\t'))   
            if line==[-1]:
                return [-1]
            else:
                if str(line[1]) in list(x[1] for x in result):
                    print(f"student ID is doubled in {num+1}")
                    return [-1]
                result.append(line)
        db_data = result

# 최초 파일 DB update(by bong)
# read_file() r을 통한 명시적 읽기 필요(by jang)

# for 'cmd M' function(by bong)
def find_in_sublists(lst, value):
    for sub_i, sublist in enumerate(lst):
        try:
            global f_M
            f_M= [sub_i, sublist.index(value)]
            return f_M
        except ValueError:
            pass

    raise ValueError('%s is not in lists' % value)

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
    global db_data
    while True:
        try:
            addid = str(input("Input Add student ID : "))
            if int(addid)>0 and int(addid)<99999999:
                if addid in list(x[1] for x in db_data):
                    print("student ID is in use")
                else:
                    addid = addid
                    break
            else:
                print("student ID should be in format of ########")
        except:
            print("student ID should be in format of ########")

    
    while True:
        try:
            addname = str(input("Input Add student name : "))            
            count = sum(1 + (unicodedata.east_asian_width(c) in "WF") for c in addname)
            print(count)
            if count<=10:  
                break
            print("The name is too long")
        except:
            print("Error")

    while True:
        try:
            addbirthyear = int(input("Input Add student Year Of Birth : "))
            addbirthmonth = int(input("Input Add student Month Of Birth : "))
            addbirthday = int(input("Input Add student Day Of Birth : "))            
            if valid_date(addbirthyear, addbirthmonth, addbirthday):
               break
        except:
            print("Please input valid date")
        print("Plase input valid date")

    while True:
        try:
            addmid = int(input("Input Add student midscore : "))
            if addmid>=0 and addmid<=100:
                break
        except:
            print("Please input number")
        print("out of score range 0~100")
    while True:
        try:
            addfinal = int(input("Input Add student finalscore : "))
            if addfinal>=0 and addfinal<=100:
                break
        except:
            print("Please input number")
        print("out of score range 0~100")

    index = len(db_data)+1

    values = [index, addid,addname,addbirthyear,addbirthmonth,addbirthday,addmid,addfinal,(addmid+addfinal)/2]
    if values[8]>=90:
        values.append('A')
    elif values[8]>=70:
        values.append('B')
    elif values[8]>=50:
        values.append('C')
    elif values[8]>=30:
        values.append('D')
    else :
        values.append('F')
    db_data.append(values)

def pcs_d():
    print("Process D")
def pcs_f():
    print("Process F")
# modify (by bong)
def pcs_m():
    print("Process M")
    modify_idORname=str(input("Enter the id or name that you want to modify score : "))
    modify_ctg=input("1. 중간고사 \n2. 기말고사 \nEnter the number you want to modify score : ")
    modify_score=int(input("Enter the score you want to input : "))
    while (modify_idORname not in [j for i in db_data for j in i]):
        print("Your first input data is not right")
        break
    find_in_sublists(db_data,modify_idORname)
    if modify_ctg in ["1","2"]:
        if modify_ctg=="1":
            modify_ctg_idx=6
        else:
            modify_ctg_idx=7
    else:
        print("Your second input data is not right")
    db_data[f_M[0]][modify_ctg_idx]=modify_score
    for i in db_data:
        print(i)
# # print (by bong)
def pcs_p(data):
    if data==[]:
        print("No Data!")
    else:
        print("일련번호    학생id       이름       생년월일    중간고사    기말고사     평 균     등급 ")
        for i in data:                
            print(f"   {i[0]:<3} {i[1]:>12} {preformat_cjk(i[2],10)} {i[3]:>8}-{i[4]:02d}-{i[5]:02d} {i[6]:>7} {i[7]:>11} {i[8]:12.1f} {i[9]:>6}")
          

# read (by bong) 파일내용이 [순번, id, 이름, 생년월일]로 구성
def pcs_r():
    print("Process R")
    x=str(input("Enter the file name : "))
    if x=="":
        print("Read file by default name : data.txt")
        x = "data.txt"
    read_file(x)

def pcs_s():
    global db_data
    
    print("Process s")
    while True:
        try :
            input_a = int(input("정렬 기준을 선택해주세요(1.이름, 2.평균점수, 3.Grade) : "))
        except :
            print("Input Error!")
            continue
        else :
            if input_a in [1,2,3]:
                break            
            print("1 ~ 3번까지 숫자만 선택 가능합니다.")
    if input_a == 1:
        print("************************************이름순으로 정렬하겠습니다.************************************")
        db_data = sorted(db_data, key = lambda x : x[2])
        pcs_p(db_data)
    elif input_a ==2:
        print("************************************평균점수순으로 정렬하겠습니다.************************************")
        db_data = sorted(db_data, key = lambda x : x[8],reverse=True)
        pcs_p(db_data)
    elif input_a==3:
        print("************************************Grade순으로 정렬하겠습니다.***********************************")
        db_data = sorted(db_data, key = lambda x : x[8], reverse=True)
        pcs_p(db_data)
    
def pcs_q():
    print("Process Q")
    print("Bye!")
    
def pcs_w():
    print("Process W")
    try:
        with open('report.txt', 'w') as f2:
            print("***********************************************성 적 표***********************************************", file = f2)
            print("  일련번호  학생id         이름       생년월일       중간고사    기말고사     평 균     등급 ", file = f2)
            for i in db_data:         
                print(f"   {i[0]:<3} {i[1]:>12} {preformat_cjk(i[2],10)} {i[3]:>8}-{i[4]:02d}-{i[5]:02d} {i[6]:>7}    {i[7]:>11}   {i[8]:12.1f} {i[9]:>6}", file = f2)
        print("The file has been saved to 'report.txt'.")
    except:
        print('Could not save file.')
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
        pcs_p(db_data)
    elif cmd == 'R':
        pcs_r()
    elif cmd == 'S':
        pcs_s()
    elif cmd == 'Q':
        break
    elif cmd == 'W':
        pcs_w()
    print('')
