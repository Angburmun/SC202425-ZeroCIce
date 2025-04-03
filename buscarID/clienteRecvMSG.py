import sys
import Ice
import RedSocial

def main():
    with Ice.initialize(sys.argv) as communicator:
        # Conectar al servidor
        id_proxy = communicator.stringToProxy("idRecursos:default -h 192.168.208.168 -p 10000")
        id_recursos = RedSocial.IdRecursosPrx.checkedCast(id_proxy)

        print("Conectado")

        if not id_recursos:
            print("Error: No se pudo hacer cast a los proxies")
            return 1

        # Llamada a getId
        try:
            user_id = id_recursos.getId(input())
            print(f"ID recibido: {user_id.id}")
            print(type(user_id))

            if isinstance(user_id, RedSocial.Mensaje):
                print("Esto es un mensaje")
        except RedSocial.idException as ex:
            print("An exception was raised")
            print(ex)

if __name__ == "__main__":
    sys.exit(main())
