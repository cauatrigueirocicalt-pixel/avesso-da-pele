# ============================================================
# TESTES DO BANCO DE DADOS
# Projeto: O Avesso da Pele
# ============================================================

import sqlite3
from pathlib import Path


# Localiza a pasta do projeto.
PASTA_PROJETO = Path(__file__).resolve().parent

# Localiza o arquivo do banco.
CAMINHO_BANCO = PASTA_PROJETO / "avesso_da_pele.db"


def mostrar_resultado(nome_teste, aprovado, detalhes=""):
    """
    Mostra se um teste foi aprovado ou reprovado.
    """

    if aprovado:
        situacao = "APROVADO"
    else:
        situacao = "REPROVADO"

    print(f"{nome_teste}: {situacao}")

    if detalhes:
        print("  Detalhes:", detalhes)


def testar_banco():
    """
    Executa todos os testes do banco.
    """

    print("=" * 65)
    print("TESTES DO BANCO DE DADOS")
    print("=" * 65)

    # --------------------------------------------------------
    # TESTE 1: O ARQUIVO EXISTE?
    # --------------------------------------------------------

    banco_existe = CAMINHO_BANCO.exists()

    mostrar_resultado(
        "Teste 1 - Arquivo do banco",
        banco_existe,
        str(CAMINHO_BANCO)
    )

    # Se o banco não existir, o restante não pode continuar.
    if not banco_existe:
        print("\nExecute primeiro:")
        print("py criar_banco.py")
        return

    # Abre a conexão.
    conexao = sqlite3.connect(CAMINHO_BANCO)

    # Ativa chaves estrangeiras.
    conexao.execute("PRAGMA foreign_keys = ON")

    # Permite acessar os resultados pelo nome da coluna.
    conexao.row_factory = sqlite3.Row

    cursor = conexao.cursor()

    # --------------------------------------------------------
    # TESTE 2: INTEGRIDADE DO ARQUIVO
    # --------------------------------------------------------

    cursor.execute("PRAGMA integrity_check")

    resultado_integridade = cursor.fetchone()[0]

    mostrar_resultado(
        "Teste 2 - Integridade do banco",
        resultado_integridade == "ok",
        resultado_integridade
    )

    # --------------------------------------------------------
    # TESTE 3: TABELAS EXISTENTES
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
        """
    )

    tabelas_encontradas = [
        linha["name"]
        for linha in cursor.fetchall()
    ]

    tabelas_necessarias = {
        "tema",
        "reflexao",
        "participacao"
    }

    tabelas_aprovadas = tabelas_necessarias.issubset(
        set(tabelas_encontradas)
    )

    mostrar_resultado(
        "Teste 3 - Tabelas obrigatórias",
        tabelas_aprovadas,
        ", ".join(tabelas_encontradas)
    )

    # --------------------------------------------------------
    # TESTE 4: QUANTIDADE DE TEMAS
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT COUNT(*) AS quantidade
        FROM tema
        """
    )

    quantidade_temas = cursor.fetchone()["quantidade"]

    mostrar_resultado(
        "Teste 4 - Quantidade de temas",
        quantidade_temas == 4,
        f"Foram encontrados {quantidade_temas} temas."
    )

    # --------------------------------------------------------
    # TESTE 5: QUANTIDADE DE REFLEXÕES
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT COUNT(*) AS quantidade
        FROM reflexao
        """
    )

    quantidade_reflexoes = cursor.fetchone()["quantidade"]

    mostrar_resultado(
        "Teste 5 - Quantidade de reflexões",
        quantidade_reflexoes == 8,
        f"Foram encontradas {quantidade_reflexoes} reflexões."
    )

    # --------------------------------------------------------
    # TESTE 6: NOMES DOS TEMAS
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT nome
        FROM tema
        ORDER BY id_tema
        """
    )

    nomes_encontrados = [
        linha["nome"]
        for linha in cursor.fetchall()
    ]

    nomes_esperados = [
        "Memória",
        "Identidade",
        "Racismo estrutural",
        "Educação"
    ]

    mostrar_resultado(
        "Teste 6 - Nomes dos temas",
        nomes_encontrados == nomes_esperados,
        ", ".join(nomes_encontrados)
    )

    # --------------------------------------------------------
    # TESTE 7: PESQUISA DO TEMA MEMÓRIA
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT nome, pergunta
        FROM tema
        WHERE nome = ?
        """,
        ("Memória",)
    )

    tema_memoria = cursor.fetchone()

    memoria_encontrada = (
        tema_memoria is not None
        and tema_memoria["nome"] == "Memória"
    )

    mostrar_resultado(
        "Teste 7 - Pesquisa do tema Memória",
        memoria_encontrada
    )

    if tema_memoria is not None:
        print("  Pergunta:", tema_memoria["pergunta"])

    # --------------------------------------------------------
    # TESTE 8: RELACIONAMENTO ENTRE TEMA E REFLEXÃO
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            tema.nome,
            reflexao.mensagem
        FROM reflexao
        JOIN tema
            ON tema.id_tema = reflexao.id_tema
        ORDER BY
            tema.id_tema,
            reflexao.id_reflexao
        """
    )

    relacionamentos = cursor.fetchall()

    relacionamento_aprovado = (
        len(relacionamentos) == 8
    )

    mostrar_resultado(
        "Teste 8 - Relacionamento tema/reflexão",
        relacionamento_aprovado,
        f"{len(relacionamentos)} relações encontradas."
    )

    print("\nREFLEXÕES RELACIONADAS:")

    for linha in relacionamentos:
        print(f"- {linha['nome']}: {linha['mensagem']}")

    # --------------------------------------------------------
    # TESTE 9: CHAVES ESTRANGEIRAS
    # --------------------------------------------------------

    cursor.execute("PRAGMA foreign_key_check")

    erros_chave_estrangeira = cursor.fetchall()

    mostrar_resultado(
        "Teste 9 - Chaves estrangeiras",
        len(erros_chave_estrangeira) == 0,
        f"{len(erros_chave_estrangeira)} erro(s) encontrado(s)."
    )

    # --------------------------------------------------------
    # TESTE 10: INSERÇÃO DE PARTICIPAÇÃO
    # --------------------------------------------------------

    # Insere uma participação de teste.
    cursor.execute(
        """
        INSERT INTO participacao (palavra)
        VALUES (?)
        """,
        ("Memória",)
    )

    # Guarda o identificador gerado.
    id_teste = cursor.lastrowid

    # Confirma temporariamente a inserção.
    conexao.commit()

    # Pesquisa o registro inserido.
    cursor.execute(
        """
        SELECT palavra
        FROM participacao
        WHERE id_participacao = ?
        """,
        (id_teste,)
    )

    participacao = cursor.fetchone()

    insercao_aprovada = (
        participacao is not None
        and participacao["palavra"] == "Memória"
    )

    mostrar_resultado(
        "Teste 10 - Inserção de participação",
        insercao_aprovada,
        f"Registro temporário de número {id_teste}."
    )

    # --------------------------------------------------------
    # LIMPEZA DO TESTE
    # --------------------------------------------------------

    # Apaga somente o registro criado pelo próprio teste.
    cursor.execute(
        """
        DELETE FROM participacao
        WHERE id_participacao = ?
        """,
        (id_teste,)
    )

    conexao.commit()

    # Confirma que o teste não deixou dados falsos.
    cursor.execute(
        """
        SELECT COUNT(*) AS quantidade
        FROM participacao
        WHERE id_participacao = ?
        """,
        (id_teste,)
    )

    quantidade_restante = cursor.fetchone()["quantidade"]

    mostrar_resultado(
        "Teste 11 - Limpeza do registro temporário",
        quantidade_restante == 0
    )

    # --------------------------------------------------------
    # FINALIZAÇÃO
    # --------------------------------------------------------

    conexao.close()

    print("\n" + "=" * 65)
    print("TESTES FINALIZADOS")
    print("=" * 65)


if __name__ == "__main__":
    testar_banco()
