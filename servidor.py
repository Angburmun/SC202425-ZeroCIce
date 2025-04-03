import sys
import Ice
import RedSocial  # Este es el archivo generado por slice2py

class IdRecursosI(RedSocial.IdRecursos):
    def getId(self, id, current=None):
        print(f"getId llamado con id: {id}")
        return RedSocial.Id(id=id)

class ReceptoraMensajesI(RedSocial.ReceptoraMensajes):
    def __init__(self):
        self.mensajes = {}
        self.usuarios = {}

    def crearMensaje(self, userId, mensaje, current=None):
        print(f"crearMensaje llamado por usuario: {userId.id}, mensaje: {mensaje}")
        nuevo = RedSocial.MensajeLike()
        nuevo.id = f"msg{len(self.mensajes)+1}"
        nuevo.content = mensaje
        nuevo.likes = 0
        self.mensajes[nuevo.id] = nuevo
        return nuevo

    def darLike(self, mensajeId, current=None):
        print(f"darLike llamado a mensaje: {mensajeId.id}")
        msg = self.mensajes.get(mensajeId.id)
        if msg:
            msg.likes += 1
            return msg
        raise Exception("Mensaje no encontrado")

    def obtenerListaMensajes(self, userId, current=None):
        print(f"obtenerListaMensajes llamado por usuario: {userId.id}")
        usuario = self.usuarios.get(userId.id)
        if not usuario:
            usuario = RedSocial.UsuarioLista()
            usuario.id = userId.id
            usuario.nombre = f"Usuario {userId.id}"
            usuario.mensajesUsuario = [m for m in self.mensajes.values()]
            self.usuarios[userId.id] = usuario
        return usuario

with Ice.initialize(sys.argv) as communicator:
    adapter = communicator.createObjectAdapterWithEndpoints("ServidorAdapter", "default -p 10000")
    
    id_recursos = IdRecursosI()
    receptora = ReceptoraMensajesI()

    adapter.add(id_recursos, Ice.stringToIdentity("idRecursos"))
    adapter.add(receptora, Ice.stringToIdentity("receptoraMensajes"))

    adapter.activate()

    proxy_id = adapter.getCommunicator().stringToProxy("idRecursos")
    proxy_receptora = adapter.getCommunicator().stringToProxy("receptoraMensajes")

    print("\nCadenas de conexión para el cliente:")
    print(f"  idRecursos: {proxy_id}")
    print(f"  receptoraMensajes: {proxy_receptora}\n")

    print("Servidor ICE corriendo... Ctrl+C para salir.")
    print("\nCadenas de conexión ICE para el cliente:")
    print("  idRecursos: idRecursos:default -p 10000")
    print("  receptoraMensajes: receptoraMensajes:default -p 10000\n")
    print("  IP: 192.168.73.168")

    communicator.waitForShutdown()
