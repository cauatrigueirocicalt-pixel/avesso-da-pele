# ============================================================
# APLICAÇÃO WEB
# Projeto: O Avesso da Pele
# ============================================================

# random será utilizado para escolher uma reflexão aleatória.
import random

# sqlite3 permite acessar o banco SQLite.
import sqlite3

# Path ajuda a localizar a pasta do projeto.
from pathlib import Path

# Importações do Flask.
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for
)


# ------------------------------------------------------------
# 1. LOCALIZAÇÃO DOS ARQUIVOS
# ------------------------------------------------------------

# Localiza a pasta na qual app.py está salvo.
PASTA_PROJETO = Path(__file__).resolve().parent

# Localiza o arquivo do banco.
CAMINHO_BANCO = PASTA_PROJETO / "avesso_da_pele.db"


# ------------------------------------------------------------
# 2. CRIAÇÃO DA APLICAÇÃO
# ------------------------------------------------------------

# Cria a aplicação Flask.
app = Flask(__name__)

# A chave permite utilizar mensagens temporárias com flash().
# Para este projeto local, utilizaremos uma frase simples.
app.secret_key = "projeto-avesso-da-pele-2026"


# ------------------------------------------------------------
# 3. CONEXÃO COM O BANCO
# ------------------------------------------------------------

def conectar_banco():
    """
    Abre uma conexão com o banco SQLite.
    """

    # Se o banco ainda não existir, apresenta um erro claro.
    if not CAMINHO_BANCO.exists():
        raise FileNotFoundError(
            "O banco avesso_da_pele.db não foi encontrado. "
            "Execute primeiro: py criar_banco.py"
        )

    # Abre a conexão.
    conexao = sqlite3.connect(CAMINHO_BANCO)

    # Ativa o funcionamento das chaves estrangeiras.
    conexao.execute("PRAGMA foreign_keys = ON")

    # Permite acessar as colunas pelo nome.
    # Exemplo: tema["nome"].
    conexao.row_factory = sqlite3.Row

    return conexao


# ------------------------------------------------------------
# 4. PÁGINA INICIAL
# ------------------------------------------------------------

@app.route("/")
def inicio():
    """
    Mostra a página inicial e os temas cadastrados.
    """

    # Abre a conexão.
    conexao = conectar_banco()

    # Consulta os temas.
    temas = conexao.execute(
        """
        SELECT
            id_tema,
            nome,
            resumo
        FROM tema
        ORDER BY id_tema
        """
    ).fetchall()

    # Fecha a conexão.
    conexao.close()

    # Envia os temas para index.html.
    return render_template(
        "index.html",
        temas=temas
    )


# ------------------------------------------------------------
# 5. PÁGINA DE UM TEMA
# ------------------------------------------------------------

@app.route("/tema/<int:id_tema>")
def exibir_tema(id_tema):
    """
    Consulta um tema usando o número recebido no endereço.
    """

    conexao = conectar_banco()

    # Procura o tema selecionado.
    tema = conexao.execute(
        """
        SELECT *
        FROM tema
        WHERE id_tema = ?
        """,
        (id_tema,)
    ).fetchone()

    # Procura as reflexões relacionadas ao tema.
    reflexoes = conexao.execute(
        """
        SELECT
            id_reflexao,
            mensagem
        FROM reflexao
        WHERE id_tema = ?
        ORDER BY id_reflexao
        """,
        (id_tema,)
    ).fetchall()

    conexao.close()

    # Se o tema não existir, volta à página inicial.
    if tema is None:
        flash(
            "O tema solicitado não foi encontrado.",
            "erro"
        )

        return redirect(
            url_for("inicio")
        )

    # Envia o tema e as reflexões para tema.html.
    return render_template(
        "tema.html",
        tema=tema,
        reflexoes=reflexoes
    )


# ------------------------------------------------------------
# 6. BUSCA
# ------------------------------------------------------------

@app.route("/buscar")
def buscar():
    """
    Pesquisa uma palavra nos conteúdos do banco.
    """

    # Recebe o termo enviado pelo formulário.
    # strip() remove espaços do início e do final.
    termo = request.args.get(
        "termo",
        ""
    ).strip()

    # Começa com uma lista vazia.
    resultados = []

    # Só pesquisa quando o termo não está vazio.
    if termo:
        conexao = conectar_banco()

        # Os sinais de porcentagem permitem encontrar
        # o termo no meio de um texto.
        padrao = f"%{termo}%"

        resultados = conexao.execute(
            """
            SELECT
                id_tema,
                nome,
                resumo
            FROM tema
            WHERE nome LIKE ?
               OR resumo LIKE ?
               OR relacao_obra LIKE ?
               OR relacao_tecnologia LIKE ?
               OR pergunta LIKE ?
            ORDER BY nome
            """,
            (
                padrao,
                padrao,
                padrao,
                padrao,
                padrao
            )
        ).fetchall()

        conexao.close()

    # Envia o termo e os resultados para busca.html.
    return render_template(
        "busca.html",
        termo=termo,
        resultados=resultados
    )


# ------------------------------------------------------------
# 7. REFLEXÃO ALEATÓRIA
# ------------------------------------------------------------

@app.route("/reflexao")
def reflexao_aleatoria():
    """
    Escolhe uma reflexão armazenada no banco.
    """

    conexao = conectar_banco()

    # JOIN relaciona reflexao e tema.
    reflexoes = conexao.execute(
        """
        SELECT
            reflexao.mensagem,
            tema.nome AS tema
        FROM reflexao
        JOIN tema
            ON tema.id_tema = reflexao.id_tema
        ORDER BY reflexao.id_reflexao
        """
    ).fetchall()

    conexao.close()

    # Escolhe uma reflexão se a lista não estiver vazia.
    if reflexoes:
        reflexao = random.choice(reflexoes)
    else:
        reflexao = None

    return render_template(
        "reflexao.html",
        reflexao=reflexao
    )


# ------------------------------------------------------------
# 8. PARTICIPAÇÃO DO VISITANTE
# ------------------------------------------------------------

@app.route(
    "/participar",
    methods=["GET", "POST"]
)
def participar():
    """
    Mostra o formulário e registra a palavra escolhida.
    """

    # Somente essas palavras poderão ser gravadas.
    palavras_permitidas = [
        "Memória",
        "Identidade",
        "Respeito",
        "Justiça",
        "Resistência",
        "Responsabilidade"
    ]

    # POST significa que o formulário foi enviado.
    if request.method == "POST":

        # Recebe a palavra selecionada.
        palavra = request.form.get(
            "palavra",
            ""
        )

        # Confere se a escolha é permitida.
        if palavra not in palavras_permitidas:
            flash(
                "Escolha uma das palavras apresentadas.",
                "erro"
            )

            return redirect(
                url_for("participar")
            )

        conexao = conectar_banco()

        # Registra a participação.
        conexao.execute(
            """
            INSERT INTO participacao (palavra)
            VALUES (?)
            """,
            (palavra,)
        )

        # Confirma a gravação.
        conexao.commit()

        # Fecha a conexão.
        conexao.close()

        flash(
            "Participação registrada. Obrigado por contribuir!",
            "sucesso"
        )

        # Depois do registro, abre os resultados.
        return redirect(
            url_for("resultados")
        )

    # GET significa apenas abrir a página.
    return render_template(
        "participar.html",
        palavras=palavras_permitidas
    )


# ------------------------------------------------------------
# 9. RESULTADOS
# ------------------------------------------------------------

@app.route("/resultados")
def resultados():
    """
    Conta quantas vezes cada palavra foi escolhida.
    """

    conexao = conectar_banco()

    # Agrupa palavras iguais e conta os registros.
    contagens = conexao.execute(
        """
        SELECT
            palavra,
            COUNT(*) AS quantidade
        FROM participacao
        GROUP BY palavra
        ORDER BY
            quantidade DESC,
            palavra ASC
        """
    ).fetchall()

    # Conta o total de participações.
    total = conexao.execute(
        """
        SELECT COUNT(*) AS quantidade
        FROM participacao
        """
    ).fetchone()["quantidade"]

    conexao.close()

    return render_template(
        "resultados.html",
        contagens=contagens,
        total=total
    )


# ------------------------------------------------------------
# 10. TRATAMENTO DE ERRO
# ------------------------------------------------------------

@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    """
    Trata endereços inexistentes.
    """

    flash(
        "A página solicitada não existe.",
        "erro"
    )

    return redirect(
        url_for("inicio")
    )


# ------------------------------------------------------------
# 11. INÍCIO DO SERVIDOR
# ------------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("PROJETO O AVESSO DA PELE")
    print("=" * 60)
    print("Abra o navegador em:")
    print("http://127.0.0.1:5000")
    print("=" * 60)

    # debug=True ajuda durante o desenvolvimento.
    app.run(debug=True)