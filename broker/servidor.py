import sys
import Ice
import RedSocial  # Este es el archivo generado por slice2py

database = {}
database["i1"] = RedSocial.Id("i1")
database["i2"] = RedSocial.Mensaje("i2", "Soy un mensaje")
database["i3"] = RedSocial.Usuario("i3", "Jose Antonio")

class IdRecursosI(RedSocial.IdRecursos):
    def getId(self, id, current=None):
        print(f"getId llamado con id: {id}")
        if id in database:
            return database[id]
        raise RedSocial.idException

    def recibirMensaje(self, mensaje, current=None):
        if isinstance(mensaje, RedSocial.Mensaje):
            print(f"Se ha recibido el siguiente mensaje: {mensaje}")
        else:
            raise RedSocial.noMensaje

with Ice.initialize(sys.argv) as communicator:
    adapter = communicator.createObjectAdapterWithEndpoints("ServidorAdapter", "default -p 10000")
    
    id_recursos = IdRecursosI()
    proxy_local = adapter.add(id_recursos, Ice.stringToIdentity("idRecursos"))
    proxy_id_recursos = RedSocial.IdRecursosPrx.checkedCast(proxy_local)

    adapter.activate()

    # 🔌 CONECTARSE AL BROKER Y SUSCRIBIRSE
    proxy_broker = communicator.stringToProxy("PubSubMensajes:default -h 192.168.208.168 -p 10100")
    broker = RedSocial.PubSubMensajesPrx.checkedCast(proxy_broker)

    if not broker:
        raise RuntimeError("No se pudo conectar al broker.")

    # 📨 SUSCRIBIR EL SERVIDOR COMO CLIENTE
    broker.addSus(proxy_id_recursos)

    print("\nCadenas de conexión para el cliente:")
    print(f"  idRecursos: {proxy_local}")

    print("Servidor ICE corriendo... Ctrl+C para salir.")
    print("\nCadenas de conexión ICE para el cliente:")
    print("  idRecursos: idRecursos:default -p 10000")
    print("  IP: 192.168.208.168")

    communicator.waitForShutdown()
