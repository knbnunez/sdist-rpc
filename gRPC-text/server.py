# import grpc
# from concurrent import futures
# import datetime
# import text_pb2
# import text_pb2_grpc

# class TextServiceServicer(text_pb2_grpc.TextServiceServicer):
#     def __init__(self):
#         self.texts = []  # Lista para almacenar textos y sus timestamps

#     def SaveText(self, request, context):
#         current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Timestamp
#         self.texts.append((request.text, current_time))  # Almacena el texto y su timestamp
#         print(f"- Texto recibido: {request.text}; Tiempo: {current_time}; Almacenado en: [{len(self.texts)-1}]")
#         return text_pb2.TextResponse(index=len(self.texts)-1) # Retorna el timestamp para el texto recibido (almacenado)

#     def GetTextTimestamp(self, request, context):
#         try:
#             index = int(request.index)
#             if 0 <= index < len(self.texts):
#                 print(f"Petición de texto recibida: [{request.index}] {self.texts[index]}")
#                 text, timestamp = self.texts[index] # Recupero el índice y su timestamp
#                 return text_pb2.TextResponse(timestamp=timestamp, text=text) # Y respondo
#             else:
#                 print(f"Petición incorrecta [{request.index}]")
#                 return text_pb2.TextResponse(timestamp="Text not found", text="")
#         except ValueError:
#             print(f"Petición incorrecta [{request.index}]")
#             return text_pb2.TextResponse(timestamp="Invalid index", text="")

import grpc
from concurrent import futures
import datetime
import text_pb2
import text_pb2_grpc

class TextServiceServicer(text_pb2_grpc.TextServiceServicer):
    def __init__(self):
        self.texts_by_client = {}  # Diccionario para almacenar textos y sus timestamps por client

    def SaveText(self, request, context):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Timestamp
        client = context.peer()  # Obtener la dirección del client que envió la solicitud
        if client not in self.texts_by_client:
            self.texts_by_client[client] = []  # Inicializar una lista para el client si es la primera vez que envía un texto
        self.texts_by_client[client].append((request.text, current_time))  # Almacena el texto y su timestamp en el diccionario del client
        index = len(self.texts_by_client[client]) - 1  # Índice en la lista del client
        print(f"- Texto recibido de {client}: {request.text}; Tiempo: {current_time}; Almacenado en: [{index}]")
        return text_pb2.TextResponse(index=index)  # Retorna el timestamp para el texto recibido (almacenado)

    def GetTextTimestamp(self, request, context):
        try:
            client = context.peer()  # Obtener la dirección del client que envía la solicitud
            if client in self.texts_by_client:
                index = int(request.index)
                if 0 <= index < len(self.texts_by_client[client]):
                    print(f"Solicitud de texto recibida de {client}: [{index}] {self.texts_by_client[client][index]}")
                    text, timestamp = self.texts_by_client[client][index]  # Recupero el índice y su timestamp
                    return text_pb2.TextResponse(timestamp=timestamp, text=text)  # Y respondo
                else:
                    print(f"Solicitud incorrecta de {client} [{request.index}]")
                    return text_pb2.TextResponse(timestamp="Text not found", text="")
            else:
                print(f"Solicitud incorrecta de {client} [{request.index}]")
                return text_pb2.TextResponse(timestamp="client not found", text="")
        except ValueError:
            print(f"Solicitud incorrecta de {client} [{request.index}]")
            return text_pb2.TextResponse(timestamp="Invalid index", text="")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)) # Crea el servidor gRPC y configurar un ThreadPoolExecutor para manejar las solicitudes
    text_pb2_grpc.add_TextServiceServicer_to_server(TextServiceServicer(), server) # Registra la implementación del servicio TextService en el servidor. TextServiceServicer() es la clase que contiene la implementación de los procedimientos del servicio
    server.add_insecure_port('[::]:50051') # Agregar un puerto inseguro (sin cifrado) al servidor. '[::]:50051' indica que escuchará en todas las interfaces (de red disponibles en la máquina) en el puerto 50051. '[::]' hace referencia a notación en IPv6
    server.start()
    print("Servicio en línea...")
    server.wait_for_termination() # Puede ser por un mensaje del cliente o un simple Ctrl+C

if __name__ == '__main__':
    serve()