create tablespace dados_ensisup
  logging
  datafile '\u01\app\oracle\oradata\XE\dados\dados_ensisup.dbf' 
  size 500m 
  autoextend on 
  next 100m maxsize 3072m
  extent management local;


create tablespace indices_ensisup
  logging
  datafile '\u01\app\oracle\oradata\XE\dados\indices_ensisup.dbf' 
  size 200m 
  autoextend on 
  next 10m maxsize 1024m
  extent management local;  

create temporary tablespace temp_ensisup
  tempfile '\u01\app\oracle\oradata\XE\dados\temp_ensisup.dbf' 
  size 50m 
  autoextend on 
  next 10m maxsize 200m
  extent management local;

create user ensino_superior
  identified by ensino_superior
  default tablespace DADOS_ENSISUP
  temporary tablespace TEMP_ENSISUP
  profile DEFAULT;

grant connect to ensino_superior;
grant resource to ensino_superior;
grant create view to ensino_superior;

ALTER USER ensino_superior quota unlimited on DADOS_ENSISUP;