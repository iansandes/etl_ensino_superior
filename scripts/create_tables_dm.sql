CREATE TABLE dm_cursos (
  id_curso NUMBER(6) NOT NULL,
  nome_curso VARCHAR2(100)
);

ALTER TABLE
  dm_cursos
ADD
  CONSTRAINT dm_curso_pk PRIMARY KEY (id_curso);

CREATE TABLE dm_departamentos (
  id_departamento NUMBER(6) NOT NULL,
  nome_departamento VARCHAR2(100)
);

ALTER TABLE
  dm_departamentos
ADD
  CONSTRAINT dm_departamento_pk PRIMARY KEY (id_departamento);

CREATE TABLE dm_disciplinas (
  id_disciplina NUMBER(6) NOT NULL,
  nome_disciplina VARCHAR2(100)
);

ALTER TABLE
  dm_disciplinas
ADD
  CONSTRAINT dm_disciplinas_pk PRIMARY KEY (id_disciplina);

CREATE TABLE dm_tempo (
  id_tempo NUMBER(6) NOT NULL,
  semestre VARCHAR2(15)
);

ALTER TABLE
  dm_tempo
ADD
  CONSTRAINT dm_tempo_pk PRIMARY KEY (id_tempo);

CREATE TABLE ft_reprovacoes (
  id_curso NUMBER(6) NOT NULL,
  id_disciplina NUMBER(6) NOT NULL,
  id_departamento NUMBER(6) NOT NULL,
  id_tempo NUMBER(8) NOT NULL,
  qtd_alunos NUMBER(10),
  qtd_alunos_cotistas NUMBER(10),
  qtd_alunos_reprovados NUMBER(10),
  qtd_alunos_cotistas_reprovados NUMBER(10)
);

ALTER TABLE
  ft_reprovacoes
ADD
  CONSTRAINT ft_reprovacoes_pk PRIMARY KEY (
    id_curso,
    id_disciplina,
    id_departamento,
    id_tempo
  );

ALTER TABLE
  ft_reprovacoes
ADD
  CONSTRAINT ft_reprovacoes_dm_curso_fk FOREIGN KEY (id_curso) REFERENCES dm_cursos (id_curso);

--  ERROR: FK name length exceeds maximum allowed length(30) 
ALTER TABLE
  ft_reprovacoes
ADD
  CONSTRAINT ft_reprovacoes_dm_departamento_fk FOREIGN KEY (id_departamento) REFERENCES dm_departamentos (id_departamento);

--  ERROR: FK name length exceeds maximum allowed length(30) 
ALTER TABLE
  ft_reprovacoes
ADD
  CONSTRAINT ft_reprovacoes_dm_disciplinas_fk FOREIGN KEY (id_disciplina) REFERENCES dm_disciplinas (id_disciplina);

ALTER TABLE
  ft_reprovacoes
ADD
  CONSTRAINT ft_reprovacoes_dm_tempo_fk FOREIGN KEY (id_tempo) REFERENCES dm_tempo (id_tempo);