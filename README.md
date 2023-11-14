### Configurando ambiente python

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Configurações gRPC

Para gerar os arquivos de acordo o arquivo.proto use o seguinte comando:

```bash
python -m grpc_tools.protoc --proto_path=. .\gRPC.proto  --python_out=. --grpc_python_out=.
```

### Passo a passo para rodar em ambiente docker:

Criando o ambiente de rede docker

```bash
docker network create grpcnetwork
```

Buildando os arquivos docker

```bash
docker build --no-cache -t 'grpc-server' . -f .\server.dockerfile
docker build --no-cache -t 'grpc-client' . -f .\client.dockerfile
```

Executando os arquivos docker

```bash
docker run --name grpc-server --network=grpcnetwork -p 50051:50051 -it grpc-server
docker run --name grpc-client --network=grpcnetwork -it grpc-client
```
