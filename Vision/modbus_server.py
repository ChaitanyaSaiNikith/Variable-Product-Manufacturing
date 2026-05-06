import threading
import logging
from vision_utils import RESULT_CODES
from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusSlaveContext,
    ModbusServerContext,
)

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.client.sync import ModbusTcpClient

HOST = '0.0.0.0'
CLIENT = "127.0.0.1"
PORT = 502 
REGISTER_ADDRESS = 0


# Modbus Internal State
_context = None
_server_thread = None


def _build_context():
    """Create a Modbus data store with one holding register initialised to 0."""
    # 10 registers of headroom; only index 0 is used
    block = ModbusSequentialDataBlock(0, [0] * 10)
    slave = ModbusSlaveContext(hr=block)        # hr = holding registers
    return ModbusServerContext(slaves=slave, single=True)

def set_result(vision_result):
    code = RESULT_CODES.index(vision_result)

    client = ModbusTcpClient(host = CLIENT, port = PORT)
    client.connect()
    client.write_register(0, code)
    client.close()
    print(f"[modbus] {vision_result}: {code} written to {REGISTER_ADDRESS}")

def read_register():
    client = ModbusTcpClient(host = CLIENT, port = PORT)
    result = client.read_holding_registers(adress= 0, count = 1)
    print("Modbus Register: value " + result)


def start(host = HOST, port = PORT):
    global _context, _server_thread
    if _server_thread and _server_thread.is_alive():
        print("[modbus] Server already running.")
        return
    try:
        _context = _build_context()
        print(" Context : " + {_context})
        print(" ContextSlaves : " + {_context.slaves})
    except Exception as e:
        print(e)

    identity = ModbusDeviceIdentification()
    identity.VendorName  = "VisionPC"
    identity.ProductCode = "UR5-Vision"
    identity.ProductName = "Lid Classifier"

    def _run():
        logging.basicConfig()
        StartTcpServer(context=_context, identity=identity, address=(host, port))

    _server_thread = threading.Thread(target=_run, daemon=True, name="modbus-server")
    _server_thread.start()
    print(f"[modbus] Server listening on {host}:{port}")


# Start Server 
if __name__ == "__main__":
    start()
    while(True):
        a = 0
    
    #TEST CODE
    import time
    print("Cycling through results every 3 s — connect a Modbus client to verify.")
    for result in ("unknown", "tall", "short", "tall", "short"):
        time.sleep(3)
        set_result(result)

    print("Done. Press Ctrl-C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass