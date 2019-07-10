CREATE TABLE test (
    name varchar(16),
    value integer default 0
);
INSERT INTO test(name, value) VALUES ('test', 0);
#DROP TABLE IF EXISTS test CASCADE;
