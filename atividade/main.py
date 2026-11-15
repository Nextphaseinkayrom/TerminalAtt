from sqlalchemy import String, Integer, select, update, delete, BigInteger
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
import time

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
   print("Área de CREATE")
   nome_c = str(input("DIgite seu nome"))
   telefone_c = input("Digite seu telefone")
   contato = Contato(
     nome = nome_c, 
           telefone = telefone_c
           )
   sessao.add(contato)
   sessao.commit()


def ler(sessao):
   print("Área de READ")
   resultado = sessao.execute(select(Contato.nome, Contato.telefone)).all()
   if resultado is None:
     print("Sem Registros")
   else:
    for nome, telefone in resultado:
     formatado = (f"+{str(telefone)[:2]}"  f" ({str(telefone)[2:4]})" f" {str(telefone)[4:9]}-{str(telefone)[9:]}")
     print(f"Nome:{nome}\nTelefone: {formatado}")

def atualizar(sessao):
   print("Área de UPDATE")
   print("Deseja atualizar o  nome da pessoa ou o telefone")
   pg_c = int(input("1: Nome \n 2: Telefone\nANS=/ "))
   if pg_c == 1:
      localizador_nome =  str(input("Digite o nome da pessoa=/ "))
      up = sessao.scalars(select(Contato).where(Contato.nome == localizador_nome)).all()
      if not up:
       print("Não encontramos o nome desta pessoa")
      else:
       print("Encontramos o nome do individuo")
       pg_m = input("Qual será o novo nome a ser colocado=/ ")
       sessao.execute(update(Contato).where(Contato.nome == localizador_nome).values(nome=pg_m))
       sessao.commit()
    
   if pg_c == 2:
       
       localizador_telefone = int(input("Digite o numero de telefone"))
       up_2 = sessao.scalars(select(Contato).where(Contato.telefone == localizador_telefone)).all()
       if up_2 is None:
        print("Não encontramos nenhum resultado. .")
       else:
        print("Encontramos o sujeito")
        pg_m_2 = int(input("Digite o novo numero de telefone"))
        up_2 = sessao.execute(update(Contato).where(Contato.telefone == localizador_telefone).values(telefone=pg_m_2))
        sessao.commit()
    

   # Em pendência pra construir.

def deletar(sessao):
   print("Área de Delete (Aviso essa função, apaga os registros em 100%, não sobra nada)\nO id da pessoa está na carteira.")
   pg_d = input("Digite o nome que deseja Deletar\nANS=/ ")
   ativador = sessao.scalars(select(Contato).where(Contato.nome == pg_d)).all()
   if not ativador:
     print("Não encontramos nada. .")
   else:
     print("Encontramos o nome")
     confirmacao = input("Deseja deletar este nome?\nANS: ")
     if confirmacao == "Sim" or "sim" or "s":
       print("Removendo")
       sessao.execute(delete(Contato).where(Contato.nome == pg_d))
       time.sleep(2.3)
       sessao.commit()
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