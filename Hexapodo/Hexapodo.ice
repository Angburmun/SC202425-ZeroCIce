module RoboInterface{
    sequence<byte> ByteSeq;

    enum MovementDirection{
        FOWARD,
        BACKWARD,
        LEFT,
        RIGHT,
        TURN_LEFT,
        TURN_RIGHT
    }


    interface HexapodController {
        // Basic movement commands
        void move(MovementDirection direction, int speed); // Speed could be a percentage
        void stop();

        ByteSeq getSnapshot();
    };
};
