module RoboInterface{

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

        // More complex movements (examples, adapt to your hexapod's capabilities)
        void setGait(string gaitName);
        void setBodyHeight(int heightPercentage);
        void moveLeg(int legId, Position targetPosition); // For individual leg control

        // Sensor data retrieval
        // SensorData getSensorData();

        // Status
        string getStatus(); // e.g., "Idle", "Moving", "Error"

        // idempotent operations for safety if needed
        idempotent void emergencyStop();
    };

    interface HexapodImage {
        byte[] getSnapshot();
    }
}
