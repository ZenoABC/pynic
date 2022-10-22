from subprocess import check_output as run_cmd
from typing import Literal

class NIC:
	def __init__(self, index: int, measurement: int, mtu: int, connected: bool, name: str):
		self.index = index
		self.measurement = measurement
		self.mtu = mtu
		self.connected = connected
		self.name = name
	

	def __repr__(self) -> str:
		return f"<NIC index={self.index} connected={self.connected} name='{self.name}'>"
	
	def set(self, *, admin: bool = None, connected: bool = None, new_name: str = None):
		command = f'netsh interface set interface name="{self.name}"'
		if admin != None:
			assert isinstance(admin, bool), f"{admin} is not valid option."
			command += f" admin={'enabled' if admin else 'disabled'}"
		
		if connected != None:
			assert isinstance(connected, bool), f"{connected} is not valid option."
			command += f" connect={'connected' if connected else 'disconnected'}"
		
		if new_name != None:
			command += f" newname={new_name}"
		run_cmd(command)
	
	def set_ipv4(
		self, *, 
		source: Literal["dhcp", "static"], 
		address: str = None, 
		mask: str = None, 
		gateway: str = None, 
		gwmetric: int = None, 
		type: Literal["anycast", "unicast"] = None, 
		sub_interface: str = None, 
		store: Literal["active", "persistent"] = None
	):
		assert source in ["dhcp", "static"], f"{source} is not valid option."
		command = f'netsh interface ipv4 set address name="{self.name}" source={source}'
		if source == "static":
			if address:
				command += f" address={address}"
			if mask:
				command += f" mask={mask}"
			if gateway:
				command += f" gateway={gateway}"
		if gwmetric:
			command += f" gwmetric={gwmetric}"
		if type:
			assert type in ["anycast", "unicast"], f"{type} is not valid option."
			command += f" type={type}"
		if sub_interface:
			command += f" subinterface={sub_interface}"
		if store:
			assert store in ["active", "persistent"], f"{store} is not valid option."
			command += f" store={store}"
		run_cmd(command)
	
	def set_ipv6(
		self, *,
		address: str = None,
		type: Literal["anycast", "unicast"] = None,
		valid_lifetime: str = None,
		preferred_lifetime: str = None,
		store: Literal["active", "persistent"] = None
	):
		command = f'netsh interface ipv6 set address name="{self.name}"'
		if address:
			command += f" address={address}"
		if type:
			assert type in ["unicast", "anycast"], f"{type} is not valid option."
			command += f" type={type}"
		if valid_lifetime:
			command += f" validlifetime={valid_lifetime}"
		if preferred_lifetime:
			command += f" preferredlifetime={preferred_lifetime}"
		if store:
			assert store in ["active", "persistent"], f"{store} is not valid option."
			command += f" store={store}"
		run_cmd(command)