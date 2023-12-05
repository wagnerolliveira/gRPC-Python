import grpc
from concurrent import futures
import gRPC_pb2
import gRPC_pb2_grpc
from pymongo import MongoClient
import json


mongo_collection = None
mongo_client = None

class MyApiServicer(gRPC_pb2_grpc.MyApiServicer):
    global mongo_client
    global mongo_collection

    def __init__(self, config):
        self.config = config

    def SendDataToServer(self, request, context):
        # Inserir dados no MongoDB
        mongo_collection.insert_one({
            'MT_CODIGO': request.MT_CODIGO,
            'MT_IMPLEMENTACAO': request.MT_IMPLEMENTACAO,
            'MT_FQN': request.MT_FQN,
            'CF_CODIGO': request.CF_CODIGO,
            'MT_PACOTE': request.MT_PACOTE,
            'MT_CLASSE': request.MT_CLASSE,
            'MT_METODO': request.MT_METODO,
            'MT_METODOSPLITCAMEL': request.MT_METODOSPLITCAMEL,
            # Adicione mais campos conforme necessário
        })

        return gRPC_pb2.DataResponse(status='Data received and inserted into MongoDB successfully.')

def serve():
    global mongo_client
    global mongo_collection

    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    # Conectar ao MongoDB
    mongo_client = MongoClient(config["mongo"]["host"], config["mongo"]["port"])
    mongo_db = mongo_client[config["mongo"]["dbname"]]
    mongo_collection = mongo_db[config["mongo"]["collection"]]
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    gRPC_pb2_grpc.add_MyApiServicer_to_server(MyApiServicer(config), server)
    # Obter o host e a porta do arquivo de configuração
    grpc_host = config["grpc_server"]["host"]
    grpc_port = config["grpc_server"]["port"]

    server.add_insecure_port(f'[::]:{grpc_port}')
    print("Server started, listening on port 50051...")
    server.start()
    server.wait_for_termination()

    # Fechar conexão com o MongoDB
    mongo_client.close()

if __name__ == '__main__':
    serve()
