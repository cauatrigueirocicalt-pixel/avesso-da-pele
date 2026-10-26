# ============================================================
# CRIAÇÃO DO BANCO DE DADOS
# Projeto: O Avesso da Pele
# ============================================================

# sqlite3 permite criar e acessar bancos SQLite.
import sqlite3

# Path ajuda a localizar corretamente a pasta do projeto.
from pathlib import Path


# ------------------------------------------------------------
# 1. LOCALIZAÇÃO DO BANCO
# ------------------------------------------------------------

# __file__ representa o arquivo criar_banco.py.
# resolve() encontra o caminho completo.
# parent representa a pasta em que o arquivo está salvo.
PASTA_PROJETO = Path(__file__).resolve().parent

# Define o nome e o local do banco.
CAMINHO_BANCO = PASTA_PROJETO / "avesso_da_pele.db"


# ------------------------------------------------------------
# 2. FUNÇÃO PRINCIPAL
# ------------------------------------------------------------

def criar_banco():
    """
    Cria o banco, cria as tabelas e insere os dados iniciais.
    """

    print("=" * 60)
    print("CRIAÇÃO DO BANCO DE DADOS")
    print("=" * 60)

    # Abre uma conexão com o banco.
    # Se o arquivo não existir, o SQLite cria automaticamente.
    conexao = sqlite3.connect(CAMINHO_BANCO)

    # Ativa a verificação das chaves estrangeiras.
    conexao.execute("PRAGMA foreign_keys = ON")

    # O cursor envia comandos SQL ao banco.
    cursor = conexao.cursor()

    # --------------------------------------------------------
    # 3. CRIAÇÃO DAS TABELAS
    # --------------------------------------------------------

    # executescript permite executar vários comandos SQL.
    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS tema (
            id_tema INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            resumo TEXT NOT NULL,
            relacao_obra TEXT NOT NULL,
            relacao_tecnologia TEXT NOT NULL,
            pergunta TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS reflexao (
            id_reflexao INTEGER PRIMARY KEY AUTOINCREMENT,
            mensagem TEXT NOT NULL,
            id_tema INTEGER NOT NULL,

            FOREIGN KEY (id_tema)
                REFERENCES tema(id_tema)
        );

        CREATE TABLE IF NOT EXISTS participacao (
            id_participacao INTEGER PRIMARY KEY AUTOINCREMENT,
            palavra TEXT NOT NULL,
            data_registro TEXT NOT NULL
                DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

    print("Tabelas verificadas ou criadas com sucesso.")

    # --------------------------------------------------------
    # 4. VERIFICAÇÃO DOS DADOS
    # --------------------------------------------------------

    # Conta quantos temas já existem.
    cursor.execute("SELECT COUNT(*) FROM tema")

    # fetchone() recebe apenas uma linha.
    quantidade_temas = cursor.fetchone()[0]

    # Os dados só serão inseridos se a tabela estiver vazia.
    # Isso evita duplicação quando o programa for executado
    # novamente.
    if quantidade_temas == 0:

        # ----------------------------------------------------
        # 5. DADOS DA TABELA TEMA
        # ----------------------------------------------------

        temas = [
            (
                "Memória",

                "Pedro reconstrói a trajetória do pai por meio "
                "de lembranças, relatos, objetos e lacunas.",

                "Recordar Henrique impede que sua vida seja "
                "reduzida apenas às circunstâncias de sua morte.",

                "A tecnologia pode preservar registros, mas "
                "nenhum banco de dados representa completamente "
                "uma vida.",

                "Quais histórias podem desaparecer quando não "
                "são registradas ou compartilhadas?"
            ),

            (
                "Identidade",

                "A identidade reúne história, afetos, escolhas, "
                "profissão, relações e pertencimento.",

                "O romance mostra o conflito entre quem Henrique "
                "é e os estereótipos projetados sobre ele.",

                "Sistemas digitais também podem reduzir pessoas "
                "a perfis, rótulos e categorias.",

                "O que não pode ser compreendido apenas pela "
                "aparência ou pelos dados de uma pessoa?"
            ),

            (
                "Racismo estrutural",

                "O racismo aparece em práticas cotidianas, "
                "instituições, abordagens e expectativas sociais.",

                "A trajetória de Henrique revela que a "
                "discriminação não se limita a ofensas explícitas.",

                "Um sistema pode reproduzir injustiças quando "
                "utiliza dados ou regras discriminatórias.",

                "Uma tecnologia pode reproduzir preconceitos "
                "mesmo sem utilizar palavras ofensivas?"
            ),

            (
                "Educação",

                "A escola aparece como espaço de formação e "
                "possibilidade, mas também de desgaste e "
                "desigualdade.",

                "Henrique é professor e encontra na literatura "
                "uma forma de ampliar a percepção dos estudantes.",

                "Computadores não transformam a educação sozinhos; "
                "é preciso objetivo, mediação e inclusão.",

                "O que transforma uma tecnologia em uma "
                "verdadeira ferramenta de aprendizagem?"
            )
        ]

        # Insere todos os temas.
        # Cada ponto de interrogação recebe um valor da lista.
        cursor.executemany(
            """
            INSERT INTO tema (
                nome,
                resumo,
                relacao_obra,
                relacao_tecnologia,
                pergunta
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            temas
        )

        print("Temas inseridos.")

        # ----------------------------------------------------
        # 6. DADOS DA TABELA REFLEXAO
        # ----------------------------------------------------

        reflexoes = [
            (
                "A memória combate o apagamento.",
                1
            ),

            (
                "Preservar uma história também é reconhecer "
                "a humanidade de quem a viveu.",
                1
            ),

            (
                "Nenhum dado representa uma pessoa por inteiro.",
                2
            ),

            (
                "A aparência não revela toda uma trajetória.",
                2
            ),

            (
                "Uma tecnologia responsável considera quem será "
                "afetado por suas decisões.",
                3
            ),

            (
                "Reconhecer uma estrutura injusta é o primeiro "
                "passo para transformá-la.",
                3
            ),

            (
                "Educação e escuta podem transformar maneiras "
                "de enxergar o outro.",
                4
            ),

            (
                "A tecnologia só educa quando existe intenção "
                "pedagógica.",
                4
            )
        ]

        cursor.executemany(
            """
            INSERT INTO reflexao (
                mensagem,
                id_tema
            )
            VALUES (?, ?)
            """,
            reflexoes
        )

        print("Reflexões inseridas.")

    else:
        print("Os dados iniciais já estavam cadastrados.")
        print("Nenhum tema foi duplicado.")

    # --------------------------------------------------------
    # 7. CONFIRMAÇÃO E FECHAMENTO
    # --------------------------------------------------------

    # commit confirma as alterações.
    conexao.commit()

    # Fecha a conexão.
    conexao.close()

    print("\nBanco preparado com sucesso!")
    print("Local:", CAMINHO_BANCO)


# ------------------------------------------------------------
# 8. EXECUÇÃO
# ------------------------------------------------------------

# Executa a função apenas quando este arquivo for iniciado
# diretamente.
if __name__ == "__main__":
    criar_banco()
