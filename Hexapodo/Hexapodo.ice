module RoboInterface{
    sequence<byte> ByteSeq;

    enum MovementDirection{
        FOWARD,
        BACKWARD,
        LEFT,
        RIGHT,
        TURNLEFT,
        TURNRIGHT
    }


    interface HexapodController {
        // Basic movement commands
        void move(MovementDirection direction, string speed); // Speed could be a percentage
        void stop();

        ByteSeq getSnapshot();
    };
};
