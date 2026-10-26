# ============================================================
# TESTE DO AMBIENTE
# Projeto: O Avesso da Pele
# ============================================================

# Importa a biblioteca sqlite3.
# Ela já acompanha o Python e permite trabalhar com SQLite.
import sqlite3


# Mostra uma linha para organizar a saída.
print("=" * 60)

# Informa o nome do teste.
print("TESTE DO AMBIENTE DO PROJETO")

# Mostra outra linha.
print("=" * 60)


# Cria uma variável com o nome do projeto.
nome_projeto = "O Avesso da Pele: além da superfície"

# Mostra o texto armazenado na variável.
print("Projeto:", nome_projeto)


# Mostra a versão do SQLite disponível no computador.
print("Versão do SQLite:", sqlite3.sqlite_version)


# Faz um pequeno cálculo para testar o funcionamento do Python.
quantidade_grupos = 4
alunos_por_grupo = 4
total_alunos = quantidade_grupos * alunos_por_grupo

print("Quantidade de grupos:", quantidade_grupos)
print("Alunos por grupo:", alunos_por_grupo)
print("Total calculado de alunos:", total_alunos)


# Cria uma lista com os temas do projeto.
temas = [
    "Memória",
    "Identidade",
    "Racismo estrutural",
    "Educação"
]


# Mostra cada tema.
print("\nTemas iniciais:")

for tema in temas:
    print("-", tema)


# Mensagem final.
print("\nPython e SQLite estão funcionando corretamente!")
