CREACION DE LA IMAGEN, CONTENEDORES Y SWARM Para replicas de contenedores, para configurar docker y usar cliente, tener activo en entorno virtual

venv\\Scripts\\activate


# Detener y eliminar stack de Swarm
docker stack rm cluster-tsp

# Salir del modo swarm
docker swarm leave --force

# Detener todos los contenedores
docker ps -q | xargs -r docker stop

# Eliminar contenedores detenidos
docker container prune -f

# Eliminar la imagen para forzar un rebuild limpio
docker rmi tsp-api -f


cd TSP-Flask-Docker/api

# Construir la imagen desde Dockerfile
docker build -t tsp-api .

# CORRER LA IMAGEN

docker run -p 5000:5000 --name contenedor-tsp-api tsp-api
docker logs contenedor-tsp-api

#SWARM
cd ..
docker swarm init
docker stack deploy -c docker-compose.yml cluster-tsp
docker stack services cluster-tsp
docker ps
docker logs <Id del contenedor>