import grpc
import gRPC_pb2
import gRPC_pb2_grpc
import psycopg2
import json


def get_data_from_postgres(config):
    # Conectar ao PostgreSQL
    postgres_conn = psycopg2.connect(
        host=config["postgres"]["host"],
        dbname=config["postgres"]["dbname"],
        user=config["postgres"]["user"],
        password=config["postgres"]["password"],
        port=config["postgres"]["port"]
    )
    postgres_cursor = postgres_conn.cursor()

    # Definir a instrução SQL
    sql_query = """
        SELECT "MT_CODIGO", "MT_IMPLEMENTACAO", "MT_FQN", "CF_CODIGO", "MT_PACOTE", "MT_CLASSE", "MT_METODO", "MT_METODOSPLITCAMEL"
        FROM public."METODO";
    """
    # Executar a consulta SQL
    postgres_cursor.execute(sql_query)
    
    # Obter todos os resultados
    rows = postgres_cursor.fetchall()
    
    # Fechar conexões
    postgres_cursor.close()
    postgres_conn.close()

    return rows


def run():
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    
    # Obter o host e a porta do servidor gRPC do arquivo de configuração
    grpc_host = config["grpc_server_connection"]["host"]
    grpc_port = config["grpc_server_connection"]["port"]

    # Criar o canal gRPC usando as informações do arquivo de configuração
    with grpc.insecure_channel(f'{grpc_host}:{grpc_port}') as channel:
        stub = gRPC_pb2_grpc.MyApiStub(channel)

        # Obter dados do PostgreSQL
        data_rows = get_data_from_postgres(config)
        # Enviar cada registro para o servidor gRPC
        for row in data_rows:
            data_request = gRPC_pb2.DataRequest(
                MT_CODIGO=row[0],
                MT_IMPLEMENTACAO=row[1],
                MT_FQN=row[2],
                CF_CODIGO=row[3],
                MT_PACOTE=row[4],
                MT_CLASSE=row[5],
                MT_METODO=row[6],
                MT_METODOSPLITCAMEL=row[7],
            )

            response = stub.SendDataToServer(data_request)
            print(f"Received response from server: {response}")


if __name__ == '__main__':
    run()
