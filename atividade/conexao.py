from sqlalchemy import create_engine, URL, text 
from sqlalchemy.orm import  sessionmaker

url = URL.create("postgresql+psycopg2", database="contatos_db")
engine = create_engine(url)

SessionLocal = sessionmaker(bind=engine)