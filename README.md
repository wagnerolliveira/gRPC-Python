Para gerar os arquivos de acordo o arquivo.proto use o seguinte comando:

```bash
python -m grpc_tools.protoc --proto_path=. .\gRPC.proto  --python_out=. --grpc_python_out=.
```