from datetime import datetime

from pydantic import BaseModel, field_validator


# 조회시, 응답 스펙 정의
class Employ(BaseModel):
    id: int
    platform: str
    keyword: str
    company_name: str
    position: str
    create_date: datetime


# 등록시, 요청 스펙 정의
class EmployCreate(BaseModel):
    keyword: str
    company_name: str
    position: str

    # 빈 문자열 검증
    @field_validator('keyword', 'company_name', 'position')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Required value")
        return v


# 스크래핑으로 추출한 데이터 클래스 정의
class EmployScrap:
    def __init__(self, keyword, company_name, position):
        self.keyword = keyword
        self.company_name = company_name
        self.position = position
