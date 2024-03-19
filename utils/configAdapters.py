from pymeasure.adapters import VXI11Adapter

# # ------> NETWORK CONFIGURATION <-----
# def config_vxi11adapter(IP:str, GPIB:int): # IP address and GPIB code for the adapters
#     return VXI11Adapter(f"TCPIP::{IP}::gpib0,{GPIB}::INSTR")

def config_vxi11adapters(instrument_gpib_mapping: dict[str, int], gateway_ip):
    adapter_dict = {key: None for key in instrument_gpib_mapping}
    for instrument_name, gpib in instrument_gpib_mapping.items():
        adapter_dict[instrument_name] = VXI11Adapter(f"TCPIP::{gateway_ip}::gpib0,{gpib}::INSTR")
    return adapter_dict
