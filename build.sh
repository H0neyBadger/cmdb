docker stop cmdb
docker rm cmdb
docker build -t cmdb:latest .
docker run -dit -p 8087:8080/tcp --name cmdb cmdb:latest
docker logs cmdb
