from sqlalchemy import String, Integer, select, update, delete, BigInteger
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from conexao import engine, SessionLocal

class Base(DeclarativeBase):
    pass

class Contato(Base):
    __tablename__ = "contatos_db"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100) )
    telefone: Mapped[int] = mapped_column(BigInteger)

Base.metadata.create_all(engine)
def criar(sessao):
   nome_c = str(input("DIgite seu nome"))
   telefone_c = input("Digite seu telefone")
   contato = Contato(
     nome = nome_c, 
           telefone = telefone_c
           )
   sessao.add(contato)
   sessao.commit()


def ler(sessao):
   resultado = sessao.execute(select(Contato.nome, Contato.telefone)).all()
   if resultado is None:
     print("Sem Registros")
   else:
    for nome, telefone in resultado:
     formatado = (f"+{str(telefone)[:2]}"  f"({str(telefone)[2:4]})" f" {str(telefone)[4:9]}-{str(telefone)[9:]}")
     print(f"Nome:{nome}\nTelefone: {formatado}")

def atualizar(sessao):
   print(".")
   # Em pendência pra construir.

def deletar(sessao):
   print(".")
   # Em pendẽncia a construnção
   

def menu():
  print("""---- MENU ----
              1 -- CREATE
              2 -- READ
              3 -- UPDATE
              4 -- DELETE
              0 -- EXIT""")
  return int(input("ANS: "))


def main():
  acoes = {
    1: criar,
    2: ler,
    3: atualizar,
    4: deletar
}
  with SessionLocal() as sessao: 
   while True:
    try: 
      opcao = menu()
    except ValueError:
      print("Valor errado")
      continue

    if opcao == 0:
      print("Saindo . . .")
      break
    
    if opcao in acoes:
      acoes[opcao](sessao)
    else:
      print("Essa Função não existe")
      
   
if __name__ == "__main__":
   main()
   