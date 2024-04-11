from sqlalchemy import Column, Integer, String, DateTime

from database import Base


class Employ(Base):
	__tablename__ = "employ"

	id = Column(Integer, primary_key=True)
	platform = Column(String, nullable=False)
	keyword = Column(String, nullable=False)
	company_name = Column(String, nullable=False)
	position = Column(String, nullable=False)
	create_date = Column(DateTime, nullable=False)