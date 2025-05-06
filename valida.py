import os
import sys
import socket
import platform
import getpass
from uuid import getnode
import subprocess
import csv
import zipfile

def get_hd_serial():
    try:
        output = subprocess.check_output("wmic diskdrive get SerialNumber", shell=True, text=True)
        lines = [line.strip() for line in output.splitlines() if line.strip() and "SerialNumber" not in line]
        return lines[0] if lines else "N/A"
    except Exception:
        return "erro_ao_obter_serial"

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
            return "nao_identificado"
    except Exception:
        return "erro_ao_obter_memoria"

def get_output_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def gerar_csv_e_zip():
    output_dir = get_output_dir()
    csv_path = os.path.join(output_dir, "report.csv")
    zip_path = os.path.join(output_dir, "validacao.zip")

    # Dados a serem salvos
    dados = {
        "nome_computador": socket.gethostname(),
        "nome_usuario": getpass.getuser(),
        "sistema_operacional": platform.system(),
        "versao_so": platform.version(),
        "arquitetura": "x64" if "64" in platform.architecture()[0] else "x86",
        "endereco_mac": get_mac_address(),
        "serial_hd": get_hd_serial(),
        "memoria_ram": get_memory_capacity()
    }

    # Escreve CSV
    try:
        with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=dados.keys())
            writer.writeheader()
            writer.writerow(dados)
    except Exception as e:
        print(f"Erro ao escrever CSV: {e}")
        return

    # Compacta em .zip
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(csv_path, arcname='report.csv')
        os.remove(csv_path)  # Remove o CSV após compactar
    except Exception as e:
        print(f"Erro ao compactar ZIP: {e}")

if __name__ == "__main__":
    gerar_csv_e_zip()
 