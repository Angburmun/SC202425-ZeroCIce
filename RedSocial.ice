module RedSocial {

    exception idException{
        string razon = "Id Desconocido";
    }

    exception noMensaje{
        string razon = "Eso no es un mensaje";
    }

    class Id{
        string id;
    }

    class Mensaje extends Id{
        string content;      
    }

    class MensajeLike extends Mensaje{
        int likes;
    }

    class Usuario extends Id{
        string nombre;
    }

    sequence<Mensaje> Mensajes;

	class UsuarioLista extends Usuario{
		Mensajes mensajesUsuario;
	}

    interface IdRecursos{
		Id getId(string id) throws idException;
        void recibirMensaje(Mensaje nuevo) throws noMensaje;
	}

	interface ReceptoraMensajes {
		Mensaje crearMensaje(Id userId, string mensaje);
		MensajeLike darLike(Id mensajeId);
		UsuarioLista obtenerListaMensajes(Id userId);
	}
}