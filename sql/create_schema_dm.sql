alter session set "_ORACLE_SCRIPT"=true;

create user dw_ensino_superior
  identified by dw_ensino_superior
  default tablespace DADOS_ENSISUP
  temporary tablespace TEMP_ENSISUP
  profile DEFAULT;

grant connect to dw_ensino_superior;
grant resource to dw_ensino_superior;
grant create view to dw_ensino_superior;

ALTER USER dw_ensino_superior quota unlimited on DADOS_ENSISUP;