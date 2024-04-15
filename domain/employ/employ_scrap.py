from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from domain.employ.employ_schema import EmployScrap
import time


# 특정 키워드로 채용 정보를 가져와 EmployScrap 값들을 리턴하는 함수 정의
def get_employ_by_wanted(keyword):
    # Playwright 시작
    p = sync_playwright().start()

    # Chromium 브라우저 실행
    browser = p.chromium.launch(headless=False)

    # 새로운 페이지 열기
    page = browser.new_page()

    # 키워드를 이용하여 채용 정보 검색 결과 페이지 - 포지션 탭으로 이동
    page.goto(f"https://www.wanted.co.kr/search?query={keyword}&tab=position")

    # 페이지가 로드될 때까지 스크롤 다운 반복
    for x in range(5):
        time.sleep(3)  # 3초 대기
        page.keyboard.down("End")  # End 키를 눌러 페이지의 끝까지 스크롤 다운

    # 페이지의 HTML 내용 가져오기
    content = page.content()

    # 브라우저 닫기
    browser.close()

    # Playwright 종료
    p.stop()

    # BeautifulSoup을 사용하여 HTML 내용 파싱
    soup = BeautifulSoup(content, "html.parser")

    # 채용 정보가 담긴 요소들을 찾아서 jobs 리스트에 저장
    jobs = soup.find_all("div", class_="JobCard_container__FqChn")

    # 채용 정보를 저장할 리스트 초기화
    jobs_db = []
    for job in jobs:
        # 채용 정보에서 포지션과 회사 이름 추출
        position = job.find("strong", class_="JobCard_title__ddkwM").text
        company_name = job.find("span", class_="JobCard_companyName__vZMqJ").text

        # 추출된 정보를 데이터베이스에 저장할 형식으로 변환하여 jobs_db 리스트에 추가
        jobs_db.append(EmployScrap(keyword, company_name, position))

    # 데이터베이스에 저장할 채용 정보가 담긴 리스트 반환
    return jobs_db
