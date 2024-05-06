from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import TimeoutException
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")  # Sandbox 기능 비활성화
options.add_argument("--disable-dev-shm-usage")  # /dev/shm 파티션 사용 중지
options.add_argument("--disable-gpu")  # GPU 하드웨어 가속 비활성화
options.add_argument("--remote-debugging-port=9222")  # 리모트 디버깅 포트 설
driver = webdriver.Chrome(options=options)
java_lst = ['https://docs.oracle.com/javase/tutorial/java/nutsandbolts/index.html', 'https://docs.oracle.com/javase/tutorial/java/javaOO/index.html', 
 'https://docs.oracle.com/javase/tutorial/java/IandI/index.html', 'https://docs.oracle.com/javase/tutorial/java/data/index.html']
cnt = 0
java_link_lst = []
for i in java_lst:
    driver = webdriver.Chrome(options=options)
    driver.get(url=i)
    sympathy_element = driver.find_element(By.ID, 'Contents')
    sympathy_element4 = sympathy_element.find_elements(By.CSS_SELECTOR, 'div a')

    count = 0
    while count < len(sympathy_element4):
        if sympathy_element4[count].text[:9] == 'Questions':
            sympathy_element4.pop(count)
        else:
            count += 1
    for link in sympathy_element4:
        java_link_lst.append(link.get_attribute('href'))
        print(f"{cnt} : Text: {link.text}, URL: {link.get_attribute('href')}")
        cnt += 1
print(sympathy_element4)
dic = dict()
dic['자료형'] = (1,2)
dic['배열'] = (2,3)
dic['연산자'] = (4,8)
dic['조건문'] = (11,13)
dic['반복문'] = (13,15)
dic['제어문'] = (15,16)
dic['클래스 정의'] = (17,21)
dic['생성자'] = (21,23)
dic['객체 생성'] = (23,25)
dic['객체 사용'] = (25,26)
dic['클래스 심화1'] = (26,30)
dic['클래스 심화2'] = (30,32)
dic['인터페이스'] = (41,44)
dic['상속'] = (48,50)
dic['오버라이딩'] = (50,51)
dic['상속'] = (51,52)
dic['포맷팅 기초1'] = (58,61)
dic['포맷팅 기초2'] = (61,63)
dic['문자열 숫자변환'] = (64,66)
dic['문자열 문자처리'] = (66,67)
dic['문자열 심화'] = (67,69)
def crawling_java(keyword):
    global dic, java_link_lst
    a,b = dic[keyword]
    answer = ''
    for i in range(a,b):
        driver = webdriver.Chrome(options=options)
        link = java_link_lst[i]
        driver.get(url=link)
        element = driver.find_element(By.ID, 'PageContent')
        answer += element.text + '\n\n'
        time.sleep(0.2)
    print(answer)
    return answer
            
def crawling_cpp(keyword):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Sandbox 기능 비활성화
    options.add_argument("--disable-dev-shm-usage")  # /dev/shm 파티션 사용 중지
    options.add_argument("--disable-gpu")  # GPU 하드웨어 가속 비활성화
    options.add_argument("--remote-debugging-port=9222")  # 리모트 디버깅 포트 설
    driver = webdriver.Chrome(options=options)

    keyword_list = ["토큰 및 문자 집합", "식별자", "숫자-부울 및 포인터 리터럴", "문자열 및 문자 리터럴", "사용자 정의 리터럴", "C++ 형식 시스템", "Lvalue 및 Rvalue", "표준 변환", "기본 제공 형식", "데이터 형식 범위", "선언 및 정의", 
                   "const", "constexpr", "이니셜라이저", "기본 제공 연산자, 우선 순위 및 결합성", "할당 연산자", "비트 연산자(&,^,|)", "캐스트 연산자()",
                   "쉼표,조건,delete 연산자", "관계형 연산자(==, !=,>,<,<=,>=)", "시프트 연산자(<<,>>)", "논리 연산자(&&,!,||)", "산술 연산자(+,-,*,/)", 
                   "new 연산자", "포인터 연산자(.*, ->*)", "증감 연산자(++,--)", "캐스팅", "선택문(if-else문)", "선택문(switch)", "반복문", "범위기반for문",
                   "네임스페이스", "열거형", "union", "함수", "함수 오버로드", "연산자 오버로드", "클래스 및 구조체", "멤버 액세스 제어", "생성자", "소멸자", 
                   "상속", "멤버에 대한 포인터", "this 포인터", "람다식", "원시 포인터", "const 및 volatile 포인터", "포인터 new 및 delete 연산자",
                   "스마트 포인터", "unique_ptr", "shared_ptr", "weak_ptr", "예외처리"]

    link_list = [
                 #토큰 및 문자 집합
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/character-sets?view=msvc-170"], 
                 #식별자
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/identifiers-cpp?view=msvc-170"],
                 #숫자-부울 및 포인터 리터럴
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/numeric-boolean-and-pointer-literals-cpp?view=msvc-170"],
                 #문자열 및 문자 리터럴
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/string-and-character-literals-cpp?view=msvc-170"],
                 #사용자 정의 리터럴
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/user-defined-literals-cpp?view=msvc-170"],
                 #C++ 형식 시스템
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/cpp-type-system-modern-cpp?view=msvc-170"],
                 #Lvalue 및 Rvalue
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/lvalues-and-rvalues-visual-cpp?view=msvc-170"],
                 #표준 변환
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/standard-conversions?view=msvc-170"],
                 #기본 제공 형식
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/fundamental-types-cpp?view=msvc-170",
                  "https://learn.microsoft.com/ko-kr/cpp/cpp/nullptr?view=msvc-170"],
                 #데이터 형식 범위
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/data-type-ranges?view=msvc-170"],
                 #선언 및 정의
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/declarations-and-definitions-cpp?view=msvc-170"],
                 #const
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/const-cpp?view=msvc-170"],
                 #constexpr
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/constexpr-cpp?view=msvc-170"],
                 #이니셜라이저
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/initializers?view=msvc-170"],
                 #기본 제공 연산자,우선 순위 및 결합성
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/cpp-built-in-operators-precedence-and-associativity?view=msvc-170"],
                 #할당 연산자
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/assignment-operators?view=msvc-170"],
                 #비트 연산자(&,^,|)
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/bitwise-and-operator-amp?view=msvc-170",
                 "https://learn.microsoft.com/ko-kr/cpp/cpp/bitwise-exclusive-or-operator-hat?view=msvc-170",
                 "https://learn.microsoft.com/ko-kr/cpp/cpp/bitwise-inclusive-or-operator-pipe?view=msvc-170"],
                 #캐스트 연산자()
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/cast-operator-parens?view=msvc-170",
                 "https://learn.microsoft.com/ko-kr/cpp/cpp/explicit-type-conversion-operator-parens?view=msvc-170"],
                 #쉼표,조건,delete 연산자
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/comma-operator?view=msvc-170",
                 "https://learn.microsoft.com/ko-kr/cpp/cpp/conditional-operator-q?view=msvc-170",
                 "https://learn.microsoft.com/ko-kr/cpp/cpp/delete-operator-cpp?view=msvc-170"],
                 #관계형 연산자(==, !=,>,<,<=,>=)
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/equality-operators-equal-equal-and-exclpt-equal?view=msvc-170",
                 "https://learn.microsoft.com/ko-kr/cpp/cpp/relational-operators-equal-and-equal?view=msvc-170"],
                 #시프트 연산자(<<,>>)
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/left-shift-and-right-shift-operators-input-and-output?view=msvc-170"],
                 #논리 연산자(&&,!,||)
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/logical-and-operator-amp-amp?view=msvc-170",
                 "https://learn.microsoft.com/ko-kr/cpp/cpp/logical-negation-operator-exclpt?view=msvc-170",
                 "https://learn.microsoft.com/ko-kr/cpp/cpp/logical-or-operator-pipe-pipe?view=msvc-170"],
                 #산술 연산자(+,-,*,/)
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/multiplicative-operators-and-the-modulus-operator?view=msvc-170",
                 "https://learn.microsoft.com/ko-kr/cpp/cpp/unary-plus-and-negation-operators-plus-and?view=msvc-170",
                 "https://learn.microsoft.com/ko-kr/cpp/cpp/additive-operators-plus-and?view=msvc-170"],
                 #new 연산자
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/new-operator-cpp?view=msvc-170"],
                 #포인터 연산자(.*, ->*)
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/pointer-to-member-operators-dot-star-and-star?view=msvc-170"],
                 #증감 연산자(++,--)
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/postfix-increment-and-decrement-operators-increment-and-decrement?view=msvc-170",
                 "https://learn.microsoft.com/ko-kr/cpp/cpp/prefix-increment-and-decrement-operators-increment-and-decrement?view=msvc-170"],
                 #캐스팅
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/casting?view=msvc-170",
                  "https://learn.microsoft.com/ko-kr/cpp/cpp/casting-operators?view=msvc-170",
                  "https://learn.microsoft.com/ko-kr/cpp/cpp/static-cast-operator?view=msvc-170", 
                  "https://learn.microsoft.com/ko-kr/cpp/cpp/const-cast-operator?view=msvc-170"],
                 #선택문(if-else문)
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/if-else-statement-cpp?view=msvc-170"],
                 #선택문(switch)
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/switch-statement-cpp?view=msvc-170"],
                 #반복문
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/iteration-statements-cpp?view=msvc-170",
                  "https://learn.microsoft.com/ko-kr/cpp/cpp/while-statement-cpp?view=msvc-170",
                  "https://learn.microsoft.com/ko-kr/cpp/cpp/do-while-statement-cpp?view=msvc-170",
                  "https://learn.microsoft.com/ko-kr/cpp/cpp/for-statement-cpp?view=msvc-170"],
                 #범위기반for문
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/range-based-for-statement-cpp?view=msvc-170"],
                 #네임스페이스
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/namespaces-cpp?view=msvc-170"],
                 #열거형
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/enumerations-cpp?view=msvc-170"],
                 #union
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/unions?view=msvc-170"],
                 #함수
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/functions-cpp?view=msvc-170"],
                 #함수 오버로드
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/function-overloading?view=msvc-170"],
                 #연산자 오버로드
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/operator-overloading?view=msvc-170",
                  "https://learn.microsoft.com/ko-kr/cpp/cpp/general-rules-for-operator-overloading?view=msvc-170"],
                 #클래스 및 구조체
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/classes-and-structs-cpp?view=msvc-170",
                  "https://learn.microsoft.com/ko-kr/cpp/cpp/class-cpp?view=msvc-170",
                  "https://learn.microsoft.com/ko-kr/cpp/cpp/struct-cpp?view=msvc-170"],
                 #멤버 액세스 제어
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/member-access-control-cpp?view=msvc-170"],
                 #생성자
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/constructors-cpp?view=msvc-170"],
                 #소멸자
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/destructors-cpp?view=msvc-170"],
                 #상속
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/inheritance-cpp?view=msvc-170",
                  "https://learn.microsoft.com/ko-kr/cpp/cpp/inheritance-keywords?view=msvc-170",
                  "https://learn.microsoft.com/ko-kr/cpp/cpp/single-inheritance?view=msvc-170"],
                 #멤버에 대한 포인터
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/pointers-to-members?view=msvc-170"],
                 #this 포인터
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/this-pointer?view=msvc-170"],
                 #람다식
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/lambda-expressions-in-cpp?view=msvc-170"],
                 #원시 포인터
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/raw-pointers?view=msvc-170"],
                 #const 및 volatile 포인터
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/const-and-volatile-pointers?view=msvc-170"],
                 #포인터 new 및 delete 연산자
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/new-and-delete-operators?view=msvc-170"],
                 #스마트 포인터
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/smart-pointers-modern-cpp?view=msvc-170"],
                 #unique_ptr
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/how-to-create-and-use-unique-ptr-instances?view=msvc-170"],
                 #shared_ptr
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/how-to-create-and-use-shared-ptr-instances?view=msvc-170"],
                 #weak_ptr
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/how-to-create-and-use-weak-ptr-instances?view=msvc-170"],
                 #예외처리
                 ["https://learn.microsoft.com/ko-kr/cpp/cpp/exception-handling-in-visual-cpp?view=msvc-170",
                  "https://learn.microsoft.com/ko-kr/cpp/cpp/errors-and-exception-handling-modern-cpp?view=msvc-170"]]

    print(f"키워드 : {keyword_list}")
    print("==========================================================================================")

    index = -1
    information_str = ""

    if keyword in keyword_list:
        index = keyword_list.index(keyword)
    else:
        print("해당 키워드가 존재하지 않습니다.")


    if index != -1:
        for n in link_list[index]:
            try:
                driver.get(url=n)
                element = driver.find_element(By.CSS_SELECTOR, 'div.content')
                information_str += element.text
                information_str += "\n\n"
            except TimeoutException:
                print(f"타임아웃 발생: {n}")
                
    if len(information_str) > 5000:
        information_str = information_str[:5000]
    
    return information_str
    
def crawling_python(keyword):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Sandbox 기능 비활성화
    options.add_argument("--disable-dev-shm-usage")  # /dev/shm 파티션 사용 중지
    options.add_argument("--disable-gpu")  # GPU 하드웨어 가속 비활성화
    options.add_argument("--remote-debugging-port=9222")  # 리모트 디버깅 포트 설
    driver = webdriver.Chrome(options=options)

    driver.get(url="https://docs.python.org/ko/3.11/tutorial/index.html")

    element = driver.find_element(By.CSS_SELECTOR, 'div.toctree-wrapper.compound')
    a_element = element.find_elements(By.CSS_SELECTOR, 'ul > li.toctree-l1 > a')

    keyword_list = []
    link_list = []

    for n in a_element:
        item = ''.join([char for char in n.text if not char.isdigit() and char != ' ' and char != "."])
        keyword_list.append(item)

    for n in a_element:
        link_list.append(n.get_attribute('href'))

    print(f"키워드 : {keyword_list}")
    
    index = -1
    information_str = ""

    if keyword in keyword_list:
        index = keyword_list.index(keyword)
    else:
        print("해당 키워드가 존재하지 않습니다.")


    if index != -1:
        try:
            driver.get(url=link_list[index])
            element = driver.find_element(By.CSS_SELECTOR, 'div.bodywrapper')
            information_str += element.text
        except TimeoutException:
            print("타임아웃 발생")
    print(information_str)
    return information_str   
    
crawl_lst = ['dummy', crawling_java, crawling_cpp, crawling_python]
    