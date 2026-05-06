
CREATE USER 'morales'@'%' identified by '2233';
create USER 'cliente'@'%' identified by '1234';


GRANT SELECT, INSERT ON jabali.* TO 'cliente'@'%';
GRANT ALL PRIVILEGES ON jabali.* TO 'morales'@'%';

FLUSH PRIVILEGES;