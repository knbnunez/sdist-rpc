import grpc
from concurrent import futures
import division_pb2
import division_pb2_grpc

class DivisionServicer(division_pb2_grpc.DivisionServiceServicer): # Clase que implementa el servicio de división
    
    def Divide(self, request, context): # Implementación del procedimiento de división
        # Obtiene los valores enviados en request (dividendo y divisor)
        dividend = request.dividend
        divisor = request.divisor

        # Verifica si el divisor es cero (división por cero)
        if divisor == 0:
            # Devuelve un error en caso de división por cero
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Divisor cannot be zero.")
            return division_pb2.DivideResponse(result=0.0)

        print("Calculando resultado...")
        result = dividend / divisor # Cálculo
        return division_pb2.DivideResponse(result=result) # Devuelve el resultado de la división

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)) # Crea el servidor gRPC y configurar un ThreadPoolExecutor para manejar las solicitudes
    division_pb2_grpc.add_DivisionServiceServicer_to_server(DivisionServicer(), server) # Registra la implementación del servicio TextService en el servidor. TextServiceServicer() es la clase que contiene la implementación de los procedimientos del servicio
    server.add_insecure_port('[::]:50051') # Agregar un puerto inseguro (sin cifrado) al servidor. '[::]:50051' indica que escuchará en todas las interfaces (de red disponibles en la máquina) en el puerto 50051. '[::]' hace referencia a notación en IPv6
    server.start() # Iniciar el server
    print("Servicio en línea...")
    server.wait_for_termination() # Fnalización del server. Puede ser por un mensaje del cliente o un simple Ctrl+C

if __name__ == '__main__': serve()