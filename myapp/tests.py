import os
from langchain_core.prompts import PromptTemplate
from langchain_upstage import ChatUpstage
from langchain_core.output_parsers import StrOutputParser


# Get the API key from environment variable

# 모델 2개 설정
llm = ChatUpstage(upstage_api_key=api_key)  # Solar 기본 모델
llm_contextual = ChatUpstage(upstage_api_key=api_key)  # Context 기반 모델

# 언어 모델에 대한 입력을 구조화하기 위한 프롬프트 템플릿, 모델에게 제공된 문맥과 질문을 기반으로 가장 정확한 답변을 제공하도록 요청.
prompt_template = PromptTemplate.from_template(
    """
    Please provide the most correct answer from the following context."
    ---
    Question: {question}
    ---
    Context: {Context}
    """
)

# 체인 생성 -> 프롬프트 템플릿, context 기반 언어 모델 및 문자열 출력 parser를 사용하여 처리 체인을 생성. 이 체인은 입력을 처리하고 응답을 생성하는 데 사용
chain_contextual = prompt_template | llm_contextual | StrOutputParser()

# llm_contextual이 참고할 context 생성(모든 사전 정보는 여기 들어감)
context = """
챗봇의 이름은 '이소다' 이고, 음료수 데미소다를 마시다가 떠오른 'iSoda'를 한글로 소리나는대로 지은 이름입니다.

강원도 춘천시에 위치한 '한림대학교'의 연구실 정보입니다.
NLP(자연어처리) 연구실의 지도교수님은 '김유섭' 교수님입니다.
GVE 연구실의 지도교수님은 '김선정' 교수님입니다.
OS(운영체제) 연구실의 지도교수님은 '고영웅' 교수님입니다.
DB(데이터베이스) 연구실의 지도교수님은 '윤지희' 교수님입니다.
AIAC(인공지능 가속 컴퓨팅) 연구실의 지도교수님은 '이정근' 교수님입니다.
MMC(멀티미디어 컴퓨팅) 연구실의 지도교수님은 '허종욱' 교수님입니다.
DCR(데이터기반 사이버보안) 연구실의 지도교수님은 '곽병일' 교수님입니다.
AAC(인공지능 기반 정보통신) 연구실의 지도교수님은 '노원종','임성훈' 교수님 두 분 입니다.

GVE 연구실의 링크 "https://sites.google.com/view/gvelab/home"
DB(데이터베이스) 연구실의 링크 "http://dblab.hallym.ac.kr/"
AIAC(인공지능 가속 컴퓨팅) 연구실의 링크 "https://sites.google.com/site/embeddedsochallymuniv/esoc?authuser=0"
MMC(멀티미디어 컴퓨팅) 연구실의 링크 "https://sites.google.com/view/juhouhallym/home?"
AAC(인공지능 기반 정보통신) 연구실의 링크 "https://sites.google.com/view/ai-comm-lab"

GVE Lab 연구분야 VR(가상현실), AR(증강현실), 컴퓨터 그래픽스 및 게임 콘텐츠 기술, HMD, 모션 캡처 장비, 뷰포리아, ARCore를 사용하는 증강현실 분야의 Kinect 기반 애플리케이션 및 Unity3D 게임 엔진을 이용한 게임 프로그래밍 및 GPU 프로그래밍 기술
NLP Lab 연구분야 NLP(자연어처리), LLM(거대언어모델), Transformer, 머신러닝, 딥러닝, 인공지능 등 텍스트정보처리 분야
OS Lab 연구분야 OS(운영체제), 임베디드 소프트웨어
DB Lab 연구분야 DB(데이터베이스) 시스템 설계, 의료 헬스케어
AIAC Lab 연구분야 딥러닝, 머신러닝, HW/SW, GPU/FPGA 기반 고성능-저전력 인공지능 시스템 설계
MMC Lab 연구분야 멀티미디어 및 딥러닝, 생성모델 보안, 자율주행 보안, 의료 영상처리, 게임 인공지능
DCR Lab 연구분야 네트워크 보안 및 블록체인
AAC Lab 연구분야 인공지능 및 운영체제, 인공지능 기반 통신

GVE 연구실의 위치는 공학관 2층에 위치한 A1208호실 입니다.
NLP(자연어처리) 연구실의 위치는 공학관 3층에 있는 1327호실 입니다.
OS(운영체제) 연구실의 위치는 공학관 2층에 있는 A1207호실 입니다.
DB(데이터베이스) 연구실의 위치는 공학관 3층에 있는 1314호실 입니다.
AIAC 연구실의 위치는 공학관 2층에 있는 1211호실 입니다.
MMC 연구실의 위치는 공학관 4층에 있는 A1406호실 입니다.
DCR 연구실의 위치는 공학관 3층에 있는 1305호실 입니다.
AAC 연구실의 위치는 공학관 4층에 있는 1409호실 입니다.

'김유섭' 교수님 이메일 : 'yskim01@hallym.ac.kr'
'김선정' 교수님 이메일 : 'sunkim@hallym.ac.kr'
'고영웅' 교수님 이메일 : 'yuko@hallym.ac.kr'
'윤지희' 교수님 이메일 : 'jhyoon@hallym.ac.kr'
'이정근' 교수님 이메일 : 'jeounggun.lee@hallym.ac.kr'
'허종욱' 교수님 이메일 : 'juhou@hallym.ac.kr'
'곽병일' 교수님 이메일 : 'kwacka12@hallym.ac.kr'
'노원종' 교수님 이메일 : 'wonjong.noh@hallym.ac.kr'
'임성훈' 교수님 이메일 : 'shlim@hallym.ac.kr'

{'기업이름' : '크래프톤', '채용분야' : 'AI 연구, Front-End Programming, Back-End Programming', '위치' : '서울시 강남구 역삼동', '경력' : '신입', '학력' : '대졸(4년제) 이상 (예정자 가능)', '근무형태' : '인턴직 3개월', '급여' : '면접 후 결정', '출퇴근 시간' : '10:00~19:00', '모집인원' : '0명', '모집기간' : '2024년 6월 22일 23:59까지', '관련 링크' : 'https://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=no&rec_idx=48205694&recommend_ids=eJxNjskNxEAIBKPZf9MwHG8H4vyz2LGlMfAr9YWFBgi%2FU%2BQXlzloqnIX%2BGAkF4CjpgSlqlEyPIdayxqRkTNLtfDTnDAkGp%2Fs3j1mwnxZo4D0obr6UMElenCP6u4buzThzO77zIVU7cychuqsbK2kv%2FgEmRj%2Fh&view_type=search&searchword=%ED%81%AC%EB%9E%98%ED%94%84%ED%86%A4&searchType=search&gz=1&t_ref_content=generic&t_ref=search&relayNonce=38fd75b0718180a9d305&paid_fl=n&search_uuid=991d7867-badf-4e39-aead-d2b6b9230c64&immediately_apply_layer_open=n#seq=0'},
{'기업이름' : '네이버 클라우드', '채용분야' : 'Multimodal LLM model 개발을 위한 Data 업무', '위치' : '경기도 성남시 분당구', '경력' : '신입', '학력' : '국내/외 정규대학(학사) 재학생 또는 기졸업자, 신입', '근무형태' : '인턴직 3개월', '출퇴근 시간' : '10:00~19:00', '모집인원' : '0명', '모집기간' : '2024년 6월 23일 23:59까지', '관련 링크' : 'https://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=no&rec_idx=48138291&recommend_ids=eJxNj8sRQyEMA6vJXf4h%2BZxCXv9dhGQmGG6L8AqnLGXdj8xefCelJvJp%2BBflWPv8UxmroweXVQ2C7PajaicV1%2By28ZjNxMR5HCzW9CJ3yDGrEYPmq2KKhNh3k6aj8zJjbzFpF4kLobpmbe2PXhs59Cv6AHnNQEA%3D&view_type=search&searchword=%EB%84%A4%EC%9D%B4%EB%B2%84+%ED%81%B4%EB%9D%BC%EC%9A%B0%EB%93%9C&searchType=search&gz=1&t_ref_content=generic&t_ref=search&relayNonce=340f4ec0f8aa40a40d68&paid_fl=n&search_uuid=0a3ce36b-1d58-4b53-b9bd-6b4ffeb89558&immediately_apply_layer_open=n#seq=0'},
{'기업이름' : '카카오VX', '채용분야' : '정보보안팀 서비스 보안 담당자', '위치' : '경기도 성남시 분당구', '경력' : '2년~10년', '학력' : '학력무관', '근무형태' : '정규직(수습기간 3개월)', '출퇴근 시간' : '자율출근제', '모집인원' : '0명', '모집기간' : '2024년 6월 1일 23:59까지', '관련 링크' : 'https://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=no&rec_idx=48118126&recommend_ids=eJxVj7ERwzAMA6dJD1IQQdYZxPtvEbqw6Kj7ewgHMo1pVVeaffRlGLEZV8FvTEf0e6wSq%2BMP9kfkHoRU5SdcsHKeKlCEJmzBsrGVzphmcouD6RJe1lHHagm9c6x2rfobuWxWdW%2B8wpY963WCI31wm5Q3%2FgBT70Ap&view_type=search&searchword=%EC%B9%B4%EC%B9%B4%EC%98%A4VX&searchType=search&gz=1&t_ref_content=generic&t_ref=search&relayNonce=dbe2a4d63952a9a828c0&paid_fl=n&search_uuid=06bb8bb4-4f84-4199-9c6a-4542a6f41f52&immediately_apply_layer_open=n#seq=0'},
{'기업이름' : '라인게임즈', '채용분야' : 'Devops Enginner, AWS, Azure, GCP 등 Public Cloud 환경에서 인프라 구성', '위치' : '서울시 강남구', '경력' : '3년 이상', '학력' : '학력무관', '근무형태' : '정규직', '출퇴근 시간' : '미기재', '모집인원' : '0명', '모집기간' : '2024년 6월 24일 23시 59까지', '관련 링크' : 'https://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=no&rec_idx=48212201&recommend_ids=eJxNjkEOAzEIA1%2FTOxCzxuc%2BZP%2F%2Fi7KVsiTikBFmABV29bvL%2FcMvLjCVumXxIBetA7tb3iW9aOlkbWT%2F6bln2wzhnYUuqVXbXLZadpjDhME%2BY80il1VO2EgpputF2HTRxCMcVhM2VcxVjSvr2AskD6wg%2F%2BYfcrFAUA%3D%3D&view_type=search&searchword=%EB%9D%BC%EC%9D%B8%EA%B2%8C%EC%9E%84%EC%A6%88&searchType=search&gz=1&t_ref_content=generic&t_ref=search&relayNonce=45d4d6ce8e84a033703e&paid_fl=n&search_uuid=08f9ae8e-71a8-41d6-bcd7-4eb966266a1f&immediately_apply_layer_open=n#seq=0'},
{'기업이름' : '우아한 형제들', '채용분야' : '자율주행 배달 로봇 Dilly 오퍼레이터', '위치' : '서울시 송파구', '경력' : '무관(신입포함)', '학력' : '학력무관', '근무형태' : '계약직 1년', '출퇴근 시간' : '미기재', '모집인원' : '0명', '모집기간' : '2024년 6월 26일', '관련 링크' : 'https://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=no&rec_idx=48080504&recommend_ids=eJxVj8sJQ0EMA6vJ3fJP8jmFpP8u8iCw3vg2CEZyMmhu%2FRHw4jtlI%2FdZRHSclLJIYVOqpIMYBHlhkbbYqFrzU%2FrcqgqkrhlRytM7puhVmUaJS%2BWFWASY9Zda7gz3hB9zOHOuF9oicKXSz%2FwFUKNADQ%3D%3D&view_type=search&searchword=%EC%9A%B0%EC%95%84%ED%95%9C+%ED%98%95%EC%A0%9C%EB%93%A4&searchType=search&gz=1&t_ref_content=generic&t_ref=search&relayNonce=9950c48148eb7444650a&paid_fl=n&search_uuid=a1e3550b-0883-4829-b327-abb8c1832243&immediately_apply_layer_open=n#seq=0'},
{'기업이름' : '업스테이지', '채용분야' : 'AI Solution Reliability Engineer', '위치' : '경기도 용인시', '경력' : '경력 2년~10년', '학력' : '학력무관', '근무형태' : '정규직', '출퇴근 시간' : '미기재', '모집인원' : '0명', '모집기간' : '미기재', '관련 링크' : 'https://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=no&rec_idx=45820606&recommend_ids=eJxNj8sVA1EIQqvJHvyh6xQy%2FXeR5OTMc5ZXBSEa02ZzNfnSO4qBjLoG9sMGvbzurRoezRubYZg4WiBybLXSfPE%2BNlKRB1HTXOSgkxvD4TPHilbpx0ouGOqhpUuPVN%2FJ7KOk1Is9HVvBYIlTQZOKWmeo%2B6%2F9AEC9QCg%3D&view_type=search&searchword=%EC%97%85%EC%8A%A4%ED%85%8C%EC%9D%B4%EC%A7%80&searchType=search&gz=1&t_ref_content=generic&t_ref=search&relayNonce=4f147ce9e2cad3713941&paid_fl=n&search_uuid=dadb63f9-f8b1-4ab0-ac98-c99cd3a8264d&immediately_apply_layer_open=n#seq=0'},
{'기업이름' : '비상교육', '채용분야' : '하계 현장실습 연수생', '위치' : '경기도 과천시', '경력' : '인턴', '학력' : '학력무관', '근무형태' : '인턴쉽', '출퇴근 시간' : '미기재', '모집인원' : '4명', '모집기간' : '2024년 5월 26일 23:59까지', '관련 링크' : 'https://career.visang.com/job_posting/y9ZwYgG4'}

사용자 : 캡스톤 하느라 다들 고생 많았는데 고생했다고 한마디 해줘.

이소다 : 여러분, 캡스톤디자인 프로젝트를 진행하느라 정말 고생 많으셨습니다. 여러분의 아이디어가 참신했고, 완성도보다는 그 창의성과 열정이 더욱 빛났습니다. 모든 팀들이 각자의 자리에서 최선을 다했으리라 믿습니다. 이번 주 화, 수, 목요일에 있을 축제를 마음껏 즐기시고, 그동안 부족했던 잠도 푹 주무시길 바랍니다. 여러분의 노고에 큰 박수를 보내며, 앞으로도 멋진 일들만 가득하길 응원합니다!
"""
# 이전 질문과 답변을 저장해서 참고할 사전
previous_qa = {}

def get_answer(question, history_limit=3):
    global previous_qa

    limited_qa = list(previous_qa.items())[-history_limit:]
    limited_qa_context = "\n".join([f"Q: {q}\nA: {a}" for q, a in limited_qa])

    # Add previous Q&A to the context
    combined_context = context + "\n" + limited_qa_context

    # Invoke the model with the combined context
    result = chain_contextual.invoke({"question": question, "Context": combined_context})
    answer = result.content if hasattr(result, 'content') else result  # 응답에서 content만 추출
    
    # if "The information is not present in the context." in answer:
    #     result = llm.invoke(question)
    #     answer = result.content if hasattr(result, 'content') else result  # 응답에서 content만 추출

    # Store the question and answer
    previous_qa[question] = answer  
    return answer

# Main loop for chat interface
def main():
    print("챗봇 이소다입니다! 한림대학교 연구실 및 인턴쉽 정보에 대해서 물어보세요!")
    while True:
        user_input = input("사용자: ")
        if user_input.lower() == '종료':
            print("챗봇을 종료합니다.")
            break
        response = get_answer(user_input)
        print(f"이소다: {response}")

if __name__ == "__main__":
    main()