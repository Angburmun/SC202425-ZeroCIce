module RoboInterface{
    sequence<byte> ByteSeq;

    enum MovementDirection{
        FOWARD,
        BACKWARD,
        LEFT,
        RIGHT,
        STOP
    }

    struct Position{
        float x; 
	    float y;
	    float z;
    }

    interface HexapodController {
        // Basic movement commands
        void move(MovementDirection direction, int speed); // Speed could be a percentage
        void stop();

        ByteSeq getSnapshot();
    };
};
