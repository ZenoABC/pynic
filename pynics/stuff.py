from subprocess import check_output as run_cmd
from pynics.cnic import NIC

def get_interfaces(*, ip_version: int = 4) -> "list[NIC]":
	resp = run_cmd(f"netsh interface ipv{ip_version} show interfaces", encoding="850")

	intrfcs = []
	for line in resp.splitlines()[3:-1]:		
		resp = [n for n in line.split(" ") if n]
		name = " ".join(resp[4:])
		data = [int(n) for n in resp[:3]] + ["connected" == resp[3], name]
		intrfcs.append(NIC(*data))
	return intrfcs