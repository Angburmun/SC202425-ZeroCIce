import sys
import Ice
import RedSocial  # Este debe ser el módulo generado por slice2py

def main():
    with Ice.initialize(sys.argv) as communicator:
        # Conectar con los proxies del servidor
        id_proxy = communicator.stringToProxy("idRecursos:default -h 192.168.208.168 -p 10000")
        receptora_proxy = communicator.stringToProxy("receptoraMensajes:default -h 192.168.208.168 -p 10000")

        id_recursos = RedSocial.IdRecursosPrx.checkedCast(id_proxy)
        receptora = RedSocial.ReceptoraMensajesPrx.checkedCast(receptora_proxy)

        if not id_recursos or not receptora:
            print("Error: No se pudo hacer cast a los proxies")
            return 1

        # Llamada a getId
        user_id = id_recursos.getId("u1")
        print(f"ID recibido: {user_id.id}")
        print(type(user_id))

        # Crear un mensaje
        mensaje = receptora.crearMensaje(user_id, "¡Hola mundo ICE!")
        print(f"Mensaje creado: ID={mensaje.id}, texto='{mensaje.content}', likes={mensaje.likes}")

        # Darle un like
        mensaje_liked = receptora.darLike(RedSocial.Id(id=mensaje.id))
        print(f"Después de dar like: ID={mensaje_liked.id}, likes={mensaje_liked.likes}")

        # Obtener lista de mensajes
        lista = receptora.obtenerListaMensajes(user_id)
        print(f"Mensajes del usuario {lista.nombre}:")  
        for m in lista.mensajesUsuario:
            print(f"- {m.id}: {m.content} ({getattr(m, 'likes', 0)} likes)")

if __name__ == "__main__":
    sys.exit(main())
