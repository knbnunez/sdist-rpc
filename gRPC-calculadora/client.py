import grpc
import division_pb2
import division_pb2_grpc

def divide_values(dividend, divisor):
    request = division_pb2.DivideRequest(dividend=dividend, divisor=divisor) # Crea un objeto de petición los valores de dividendo y divisor
    try:
        response = stub.Divide(request) # Llamdo al procedimiento del servidor
        result = response.result # Almacenamiento del resultado contenido en la respuesta
        print(f">>> Resultado de la división: {dividend} / {divisor} = {result} <<<")
    except grpc.RpcError as e:
        print(f"Error de comunicación: {e.details()}")

if __name__ == '__main__':
    server_ip = 'localhost'
    port = '50051'
    channel = grpc.insecure_channel(f'{server_ip}:{port}') # Creación del canal de comunicación con el servidor (insercure = sin cifrado)
    stub = division_pb2_grpc.DivisionServiceStub(channel) # Object Stub para para llamar a los procedimientos de DivisionService definidos en el servidor, usando el canal de conexión generado arriba

    while True:
        # Presentación de opciones
        print("Elija una opción:")
        print("1. Realizar una división")
        print("2. Salir")
        option = input("Opción: ")

        # Verificación de entrada
        if option == "1":
            # Solicitud al usuario de ingreso de valores {dividendo y divisor}
            dividend = float(input("Ingresa el dividendo: "))
            divisor = float(input("Ingresa el divisor: "))
            divide_values(dividend, divisor) # Invocación de función cliente
        elif option == "2":
            break
        else:
            print("Opción inválida, inténtelo nuevamente.") 
