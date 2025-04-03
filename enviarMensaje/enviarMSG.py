import sys
import Ice
import RedSocial  # Este debe ser el módulo generado por slice2py

def main():
    with Ice.initialize(sys.argv) as communicator:
        # Conectar con los proxies del servidor
        id_proxy = communicator.stringToProxy("idRecursos:default -h 192.168.208.168 -p 10000")
        id_recursos = RedSocial.IdRecursosPrx.checkedCast(id_proxy)

        if not id_recursos:
            print("Error: No se pudo hacer cast a los proxies")
            return 1

        mensajeNuevo = RedSocial.Mensaje("u1", "Buenas tardes por las tardes")
        id_recursos.recibirMensaje(mensajeNuevo)


if __name__ == "__main__":
    sys.exit(main())
