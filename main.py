import sqlite3
import flet as ft


# Função para inicializar o banco de dados
def init_db():
    with sqlite3.connect('dados.db') as conexao:
        cursor = conexao.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS localidades (
            pib INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            localidade TEXT NOT NULL
        )
        ''')
        conexao.commit()


# Função para inserir dados no banco
def inserir_dados(pib, nome, localidade):
    with sqlite3.connect('dados.db') as conexao:
        cursor = conexao.cursor()
        cursor.execute('''
        INSERT INTO localidades (pib, nome, localidade) VALUES (?, ?, ?)
        ''', (pib, nome, localidade))
        conexao.commit()


# Função para consultar dados
def consultar_dados():
    with sqlite3.connect('dados.db') as conexao:
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM localidades')
        return cursor.fetchall()

# Função para deletar dados pelo PIB
def deletar_dados(pib):
    with sqlite3.connect('dados.db') as conexao:
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM localidades WHERE pib = ?', (pib,))
        conexao.commit()
    return cursor.rowcount > 0  # Retorna True se algo foi deletado
# Inicializa o banco de dados
init_db()


# Função principal do app Flet
def main(page: ft.Page):
    page.title = "App com Flet e SQLite"

    # Adicionar dados
    def adicionar_dados(e):
        pib = int(pib_input.value)
        nome = nome_input.value
        localidade = localidade_input.value
        inserir_dados(pib, nome, localidade)
        pib_input.value = ""
        nome_input.value = ""
        localidade_input.value = ""
        page.add(ft.Text("Dados inseridos com sucesso!", color="green"))

    # Consultar dados
    def mostrar_dados(e):
        dados = consultar_dados()
        resultados.clean_async()
        page.update()
        for linha in dados:
            resultados.controls.append(ft.Text(f"PIB: {linha[0]}, Nome: {linha[1]}, Localidade: {linha[2]}"))
        page.update()

    # Deletar dados pelo PIB fornecido
    def deletar_dados_interface(e):
        pib = int(pib_input.value)
        if deletar_dados(pib):
            page.add(ft.Text(f"Registro com PIB {pib} deletado com sucesso!", color="green"))
        else:
            page.add(ft.Text(f"Registro com PIB {pib} não encontrado.", color="red"))
        pib_input.value = ""
        mostrar_dados(None)  # Atualiza a exibição dos dados

    # Interface do Flet
    pib_input = ft.TextField(label="PIB",hint_text="Digite o PIB")
    nome_input = ft.TextField(label="Nome", hint_text="Digite o Nome")
    localidade_input = ft.TextField(label="Localidade", hint_text="Digite a Localidade")

    adicionar_button = ft.ElevatedButton("Adicionar Dados", on_click=adicionar_dados)
    consultar_button = ft.ElevatedButton("Consultar Dados", on_click=mostrar_dados)
    deletar_button = ft.ElevatedButton("Deletar Dados", on_click=deletar_dados_interface)
    resultados = ft.Column()



    page.add(pib_input, nome_input, localidade_input, adicionar_button, consultar_button,deletar_button, resultados)


ft.app(target=main)
