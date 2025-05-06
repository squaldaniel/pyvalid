import os
import sys
import socket
import platform
import getpass
from uuid import getnode
import subprocess

def get_hd_serial():
    try:
        output = subprocess.check_output("wmic diskdrive get SerialNumber", shell=True, text=True)
        lines = [line.strip() for line in output.splitlines() if line.strip() and "SerialNumber" not in line]
        return lines[0] if lines else "N/A"
    except Exception:
        return "Erro ao obter serial"

def get_mac_address():
    mac = getnode()
    mac_str = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
    return mac_str

def get_memory_capacity():
    try:
        output = subprocess.check_output("wmic computersystem get TotalPhysicalMemory", shell=True, text=True)
        lines = [line.strip() for line in output.splitlines() if line.strip() and "TotalPhysicalMemory" not in line]
        if lines:
            total_bytes = int(lines[0])
            total_gb = round(total_bytes / (1024 ** 3), 2)
            return f"{total_gb} GB"
        else:
            return "Não identificado"
    except Exception:
        return "Erro ao obter memória"

def get_output_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def gerar_report():
    output_dir = get_output_dir()
    report_path = os.path.join(output_dir, "report.txt")

    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"Nome do Computador: {socket.gethostname()}\n")
            f.write(f"Nome do Usuário: {getpass.getuser()}\n")
            f.write(f"Sistema Operacional: {platform.system()}\n")
            f.write(f"Versão SO: {platform.version()}\n")
            f.write(f"Arquitetura: {'x64' if '64' in platform.architecture()[0] else 'x86'}\n")
            f.write(f"Endereço MAC: {get_mac_address()}\n")
            f.write(f"Serial do HD: {get_hd_serial()}\n")
            f.write(f"Memória RAM: {get_memory_capacity()}\n")
    except Exception as e:
        print(f"Erro ao escrever o arquivo: {e}")

if __name__ == "__main__":
    gerar_report()
