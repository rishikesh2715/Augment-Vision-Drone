#include <iostream>
#include <unordered_map>
#include <boost/asio.hpp>

class DroneTelemetry {
public:
    DroneTelemetry(const std::string& port, unsigned int baud_rate)
        : io(), serial(io, port) {
        serial.set_option(boost::asio::serial_port_base::baud_rate(baud_rate));
    }

    void process_serial_data() {
        while (true) {
            // Read from serial port
            uint8_t device_address;
            boost::asio::read(serial, boost::asio::buffer(&device_address, 1));
            
            if (device_address == RADIO_ADDRESS) {
                parse_packet();
            } else {
                std::cout << "Unknown device address: " << device_address << std::endl;
            }
            
            
        }
    }

    

private:
    boost::asio::io_service io;
    boost::asio::serial_port serial;
    static const uint8_t RADIO_ADDRESS = 0xEA;

    
};

int main() {
    DroneTelemetry telemetry("/dev/ttyS0", 115200);
    telemetry.process_serial_data();
    return 0;
}