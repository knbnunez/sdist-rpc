import grpc
import text_pb2
import text_pb2_grpc

def send_text(stub):
    text = input("Ingrese el texto: ")
    request = text_pb2.TextRequest(text=text) # Se crea un objeto TextRequest. Este objeto pertenece al servicio gRPC TextService y se utiliza para empaquetar la solicitud que se enviará al servidor.
    response = stub.SaveText(request) # Se llama al procedimiento SaveText proporcionado por el stub
    print(f"- Almacenado en [{response.index}]")

def get_text_timestamp(stub):
    index = int(input("Ingrese el índice del texto: "))
    request = text_pb2.TextIndex(index=index)
    response = stub.GetTextTimestamp(request)
    if response.timestamp != "Text not found":
        print("Texto:", response.text)
        print("Timestamp:", response.timestamp)
        print("Almacenado en :", response.index)
    else:
        print("Text not found")

def main():
    server_ip = 'localhost'
    port = '50051'
    channel = grpc.insecure_channel(f'{server_ip}:{port}') # Creación del canal de comunicación con el servidor (insercure = sin cifrado)
    stub = text_pb2_grpc.TextServiceStub(channel) # Object Stub para para llamar a los procedimientos de TextService definidos en el servidor, usando el canal de conexión generado arriba

    while True:
        # Presentación de opciones
        print("Elija una opción:")
        print("1. Enviar texto")
        print("2. Solicitar timestamp de un texto")
        print("3. Salir")
        option = input("Opción: ")

        # Verificación de entrada
        if option == "1":  send_text(stub)
        elif option == "2": get_text_timestamp(stub)
        elif option == "3": break
        else: print("Opción inválida, inténtelo denuevo.")

if __name__ == '__main__':
    main()