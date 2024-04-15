from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

# 위에서 정의한 employ_schema, employ_crud 참조 + employ_scrap 추가
from domain.employ import employ_schema, employ_crud, employ_scrap

# prefix 설정
router = APIRouter(
    prefix="/api/employ"
)


# 채용 정보 전체 조회 API
@router.get("/list", response_model=list[employ_schema.Employ])  # employ_schema.py 에서 정의한 응답 스펙 기재
def employ_list(db: Session = Depends(get_db)):
    return employ_crud.employ_list(db)


# 채용 정보 수동 등록 API
@router.post("/manual/create")
def employ_manual_create(create_request: employ_schema.EmployCreate,  # employ_schema.py 에서 정의한 요청 스펙 파라미터
                         db: Session = Depends(get_db)):
    employ_crud.employ_create(db, create_request, "MANUAL")


# 채용 정보 원티드 갱신 API
@router.put("/scrap/wanted/{keyword}")
def employ_scrap_wanted_create(keyword: str, db: Session = Depends(get_db)):
    platform = "WANTED"

    # 스크랩 한 원티드의 채용 정보
    employs = employ_scrap.get_employ_by_wanted(keyword)

    if employs:
        # 갱신전, 키워드와 플랫폼으로 기존 채용 정보 삭제
        employ_crud.employ_delete(db, keyword, platform)

        for employ in employs:
            # 스크랩한 채용 정보 저장
            employ_crud.employ_scrap_renew(db, employ, platform)
