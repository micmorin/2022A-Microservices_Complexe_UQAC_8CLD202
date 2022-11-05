FROM mysql

ENV MYSQL_ROOT_PASSWORD fakepassword
ENV MYSQL_DATABASE IoTDatabase
ENV MYSQL_USER IoTUser
ENV MYSQL_PASSWORD IoTPassword

EXPOSE 3306

COPY ./sql /docker-entrypoint-initdb.d/