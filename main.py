from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
from datetime import datetime
import email.utils

app = FastAPI()

# 네이버 API 키 입력
CLIENT_ID = "YfL62brrcsweO43koExo"
CLIENT_SECRET = "ii4Re0Lin2"


# 템플릿 및 정적 파일 설정
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def format_date(rfc_date):
    """
    날짜 문자열 형식으로 변환
    """
    try:
        parsed_date = email.utils.parsedate_to_datetime(rfc_date)  # RFC 2822 날짜 파싱
        return parsed_date.strftime("%Y년 %m월 %d일")  # 원하는 포맷으로 변환
    except Exception:
        return "날짜 정보 없음"

@app.get("/", response_class="HTMLResponse")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/results", response_class="HTMLResponse")
async def search_results(request: Request, query: str = Query(...)):
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=20"
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }

    response = requests.get(url, headers=headers)
    news_data = response.json().get("items", []) if response.status_code == 200 else []

    # 날짜 포맷 변환 적용
    for news in news_data:
        news["formatted_date"] = format_date(news.get("pubDate", ""))

    return templates.TemplateResponse(
        "result.html",
        {"request": request, "query": query, "news_list": news_data}
    )
