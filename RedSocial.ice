module RedSocial {

    exception idException{
        string razon = "Id Desconocido";
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
	}

	interface ReceptoraMensajes {
		Mensaje crearMensaje(Id userId, string mensaje);
		MensajeLike darLike(Id mensajeId);
		UsuarioLista obtenerListaMensajes(Id userId);
	}
}