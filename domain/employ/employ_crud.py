from datetime import datetime
from models import Employ
from sqlalchemy.orm import Session
from sqlalchemy import and_
from domain.employ.employ_schema import EmployCreate, EmployScrap


# 채용 정보 전체 조회
def employ_list(db: Session):
    return db.query(Employ) \
        .order_by(Employ.create_date.desc()) \
        .all()


# 채용 정보 등록
def employ_create(db: Session, create_request: EmployCreate, platform: str):
    db.add(Employ(platform=platform,
                  keyword=create_request.keyword,
                  company_name=create_request.company_name,
                  position=create_request.position,
                  create_date=datetime.now()))
    db.commit()


# 채용 정보 삭제 By 키워드, 플랫폼
def employ_delete(db: Session, keyword: str, platform: str):
    db.query(Employ) \
        .filter(and_(Employ.keyword == keyword, Employ.platform == platform)) \
        .delete(synchronize_session=False)
    db.commit()


# 스크래핑 채용 정보 등록
def employ_scrap_renew(db: Session, create_request: EmployScrap, platform: str):
    db.add(Employ(platform=platform,
                  keyword=create_request.keyword,
                  company_name=create_request.company_name,
                  position=create_request.position,
                  create_date=datetime.now()))
    db.commit()
