from datetime import datetime
import cx_Oracle as db
import petl


from utils import CursorProxy


def open_connection():
    # Estabelece as conexões com os bancos de dados operacional e dimensional
    op_con = db.connect("ensino_superior/ensino_superior@localhost:1521/xe")
    dm_con = db.connect("dw_ensino_superior/dw_ensino_superior@localhost:1521/xe")

    return op_con, dm_con


def get_cursor_dm(dm_con):
    # Retorna o cursor para o banco de dados oracle
    return CursorProxy(dm_con.cursor())


def create_dm_disciplinas(op_con, dm_con):
    # Extrai os dados do banco operacional e insere os dados no banco dimensional

    disciplinas = petl.fromdb(op_con, "select cod_disc, nome_disc from disciplinas")

    dm_disciplinas = petl.rename(
        disciplinas, {"COD_DISC": "ID_DISCIPLINA", "NOME_DISC": "NOME_DISCIPLINA"}
    )

    petl.todb(dm_disciplinas, get_cursor_dm(dm_con), "DM_DISCIPLINAS")


def create_dm_cursos(op_con, dm_con):
    # Extrai os dados do banco operacional e insere os dados no banco dimensional

    cursos = petl.fromdb(op_con, "select cod_curso, nom_curso from cursos")

    dm_cursos = petl.rename(
        cursos, {"COD_CURSO": "ID_CURSO", "NOM_CURSO": "NOME_CURSO"}
    )

    petl.todb(dm_cursos, get_cursor_dm(dm_con), "DM_CURSOS")


def create_dm_departamentos(op_con, dm_con):
    # Extrai os dados do banco operacional e insere os dados no banco dimensional

    departamentos = petl.fromdb(op_con, "select * from departamentos")

    dm_departamentos = petl.rename(
        departamentos, {"COD_DPTO": "ID_DEPARTAMENTO", "NOME_DPTO": "NOME_DEPARTAMENTO"}
    )

    petl.todb(dm_departamentos, get_cursor_dm(dm_con), "DM_DEPARTAMENTOS")


def create_dm_tempo(op_con, dm_con):
    # Extrai os dados do banco operacional e insere os dados no banco dimensional

    semestres = petl.fromdb(op_con, "select distinct semestre from matriculas")

    id_tempo = []

    for tempo in semestres:
        # Ignora o cabeçalho da tabela
        if tempo[0] != "SEMESTRE":
            id_tempo.append(int(tempo[0]))

    dm_tempo = petl.transform.basics.addcolumn(semestres, "ID_TEMPO", id_tempo)

    petl.todb(dm_tempo, get_cursor_dm(dm_con), "DM_TEMPO")


def create_ft_reprovacoes(op_con, dm_con):
    # Extrai os dados do banco operacional e insere os dados no banco dimensional

    matriz_cursos = petl.fromdb(
        op_con,
        "select cod_curso as id_curso, cod_disc as id_disciplina from matrizes_cursos",
    )
    semestres = petl.fromdb(dm_con, "select semestre from dm_tempo")
    reprovacoes = petl.fromdb(
        op_con,
        """select
            a.cotista, 
            c.cod_curso,
            d.cod_dpto,
            m.semestre,
            m.nota,
            m.faltas,
            d.cod_disc,
            d.carga_horaria
          from
            alunos a
            join cursos c on a.cod_curso = c.cod_curso
            join departamentos d on c.cod_dpto = d.cod_dpto
            join matriculas m on a.mat_alu = m.mat_alu
            join disciplinas d on m.cod_disc = d.cod_disc
        """,
    )
    reprovacoes = petl.transform.headers.skip(reprovacoes, 1)
    matriz_cursos = petl.transform.headers.skip(matriz_cursos, 1)
    semestres = petl.transform.headers.skip(semestres, 1)

    id_curso = []
    id_disciplina = []
    id_departamento = []
    id_tempo = []
    qtd_alunos = []
    qtd_alunos_cotistas = []
    qtd_alunos_reprovados = []
    qtd_alunos_cotistas_reprovados = []

    """
    Dicionário de índices

    0 : Flag Cotista
    1 : Código do Curso
    2 : Código do Departamento
    3 : Semestre
    4 : Nota
    5 : Faltas
    6 : Código da Disciplina
    7 : Carga horária da disciplina
    """

    for curso_disciplina in matriz_cursos:
        for semestre in semestres:
            aux_qtd_alunos_cotistas = 0
            aux_qtd_alunos_reprovados = 0
            aux_qtd_alunos_cotistas_reprovados = 0
            aux_depto = 0
            aux_qtd_alunos = 0
            for aluno in reprovacoes:
                if (
                    int(curso_disciplina[0]) == int(aluno[1])
                    and int(curso_disciplina[1]) == int(aluno[6])
                ) and int(semestre[0]) == int(aluno[3]):
                    aux_qtd_alunos += 1
                    if (float(aluno[4]) < 7.0) or (aluno[5] >= (0.25 * aluno[7])):
                        aux_qtd_alunos_reprovados += 1

                    if aluno[0] == "S":
                        aux_qtd_alunos_cotistas += 1
                        if (float(aluno[4]) < 7.0) or (aluno[5] >= (0.25 * aluno[7])):
                            aux_qtd_alunos_cotistas_reprovados += 1

                    aux_depto = aluno[2]
            if aux_qtd_alunos > 0:
                id_curso.append(curso_disciplina[0])
                id_disciplina.append(curso_disciplina[1])
                id_departamento.append(aux_depto)
                id_tempo.append(semestre[0])
                qtd_alunos.append(aux_qtd_alunos)
                qtd_alunos_cotistas.append(aux_qtd_alunos_cotistas)
                qtd_alunos_reprovados.append(aux_qtd_alunos_reprovados)
                qtd_alunos_cotistas_reprovados.append(
                    aux_qtd_alunos_cotistas_reprovados
                )

    ft_reprovacoes = petl.empty()
    ft_reprovacoes = petl.transform.basics.addcolumn(
        ft_reprovacoes, "ID_CURSO", id_curso
    )
    ft_reprovacoes = petl.transform.basics.addcolumn(
        ft_reprovacoes, "ID_DISCIPLINA", id_disciplina
    )
    ft_reprovacoes = petl.transform.basics.addcolumn(
        ft_reprovacoes, "ID_DEPARTAMENTO", id_departamento
    )
    ft_reprovacoes = petl.transform.basics.addcolumn(
        ft_reprovacoes, "ID_TEMPO", id_tempo
    )
    ft_reprovacoes = petl.transform.basics.addcolumn(
        ft_reprovacoes, "QTD_ALUNOS", qtd_alunos
    )
    ft_reprovacoes = petl.transform.basics.addcolumn(
        ft_reprovacoes, "QTD_ALUNOS_COTISTAS", qtd_alunos_cotistas
    )
    ft_reprovacoes = petl.transform.basics.addcolumn(
        ft_reprovacoes, "QTD_ALUNOS_REPROVADOS", qtd_alunos_reprovados
    )
    ft_reprovacoes = petl.transform.basics.addcolumn(
        ft_reprovacoes, "QTD_ALUNOS_COTISTAS_REPROVADOS", qtd_alunos_cotistas_reprovados
    )
    petl.todb(ft_reprovacoes, get_cursor_dm(dm_con), "FT_REPROVACOES")


if __name__ == "__main__":
    # Obtenção das conexões
    op_con, dm_con = open_connection()

    # Apaga dados da tabela de fatos
    dm_cursor = get_cursor_dm(dm_con)
    dm_cursor.execute("delete from ft_reprovacoes")
    # Criação das dimensões e fatos (Extract, Transform, Load)
    create_dm_disciplinas(op_con, dm_con)
    create_dm_cursos(op_con, dm_con)
    create_dm_departamentos(op_con, dm_con)
    create_dm_tempo(op_con, dm_con)
    create_ft_reprovacoes(op_con, dm_con)
