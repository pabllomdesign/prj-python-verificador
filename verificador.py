import psutil
import time
import os
import logging
import configparser
import pystray
from pystray import MenuItem as item
from PIL import Image
import threading
from datetime import datetime

class CustomConfigParser(configparser.ConfigParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def read(self, filenames, encoding=None):
        with open(filenames, 'r', encoding=encoding) as f:
            lines = f.readlines()
        lines = [line for line in lines if not line.strip().startswith('--')]
        self.read_string(''.join(lines))

def configurar_logging(habilitar_logs):
    if habilitar_logs:
        logging.basicConfig(filename='monitoramento.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.disable(logging.CRITICAL)

def ler_configuracoes():
    config = CustomConfigParser()
    config.read('config.ini')
    executaveis = []
    for key in config['Executaveis']:
        if key.endswith('_nome'):
            base_key = key[:-5]
            nome = config['Executaveis'][base_key + '_nome']
            caminho = config['Executaveis'][base_key + '_caminho']
            executaveis.append({"nome": nome, "caminho": caminho})
    executaveis_especiais = []
    for section in config.sections():
        if section.startswith('ExecutaveisEspeciais'):
            especiais = {}
            for key, value in config.items(section):
                especiais[key] = value
            executaveis_especiais.append(especiais)
    intervalo = int(config['Monitoramento']['intervalo'])
    atraso_executaveis = int(config['Monitoramento']['atraso_executaveis'])
    atraso_entre_executaveis_especiais = int(config['Monitoramento']['atraso_entre_executaveis_especiais'])
    horarios_reinicio = [config['Reinicializacao'][key] for key in config['Reinicializacao']]
    habilitar_logs = int(config['Logs']['habilitar_logs'])
    return executaveis, executaveis_especiais, intervalo, atraso_executaveis, atraso_entre_executaveis_especiais, horarios_reinicio, habilitar_logs

def verificar_processo(nome):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == nome:
            return True
    return False

def reabrir_executavel(caminho):
    try:
        os.startfile(caminho)
        logging.info(f"{os.path.basename(caminho)} foi reaberto.")
    except Exception as e:
        logging.error(f"Erro ao tentar abrir o executável {os.path.basename(caminho)}: {e}")

def fechar_executavel(nome):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == nome:
            proc.kill()
            logging.info(f"{nome} foi fechado.")
            return

def iniciar_executaveis(executaveis):
    for exe in executaveis:
        if not verificar_processo(exe["nome"]):
            logging.info(f"{exe['nome']} não está em execução. Tentando abrir...")
            reabrir_executavel(exe["caminho"])

def iniciar_executaveis_especiais(executaveis_especiais, atraso_entre_executaveis_especiais):
    for especiais in executaveis_especiais:
        for key, value in especiais.items():
            if key.endswith('_nome'):
                nome = value
                caminho = especiais[key[:-5] + '_caminho']
                time.sleep(atraso_entre_executaveis_especiais)
                reabrir_executavel(caminho)
                logging.info(f"{nome} foi iniciado após o tempo especificado.")

def reiniciar_executaveis_especiais(executaveis_especiais, horarios_reinicio, atraso_entre_executaveis_especiais):
    while True:
        try:
            now = datetime.now()
            for horario in horarios_reinicio:
                if now.strftime('%H:%M') == horario:
                    iniciar_executaveis_especiais(executaveis_especiais, atraso_entre_executaveis_especiais)
                    logging.info(f"Executáveis especiais reiniciados às {horario}.")
            time.sleep(60)  # Verificar a cada minuto
        except Exception as e:
            logging.error(f"Erro ao reiniciar os executáveis especiais: {e}")

def monitorar_executaveis(executaveis, intervalo):
    while True:
        try:
            for exe in executaveis:
                em_execucao = verificar_processo(exe["nome"])
                if not em_execucao:
                    logging.warning(f"{exe['nome']} foi fechado.")
                    reabrir_executavel(exe["caminho"])
            time.sleep(intervalo)
        except Exception as e:
            logging.error(f"Erro no monitoramento dos executáveis: {e}")

def criar_icone(icone_path):
    return Image.open(icone_path)

def quit_action(icon, item):
    icon.stop()
    os._exit(0)  # Força a saída do programa

def main():
    executaveis, executaveis_especiais, intervalo, atraso_executaveis, atraso_entre_executaveis_especiais, horarios_reinicio, habilitar_logs = ler_configuracoes()
    configurar_logging(habilitar_logs)
    logging.info("Iniciando o monitoramento dos executáveis.")
    iniciar_executaveis(executaveis)

    # Executa o monitoramento dos executáveis regulares em uma thread separada
    monitor_thread = threading.Thread(target=monitorar_executaveis, args=(executaveis, intervalo))
    monitor_thread.daemon = True
    monitor_thread.start()

    # Executa a reinicialização dos executáveis especiais em uma thread separada
    reinicio_thread = threading.Thread(target=reiniciar_executaveis_especiais, args=(executaveis_especiais, horarios_reinicio, atraso_entre_executaveis_especiais))
    reinicio_thread.daemon = True
    reinicio_thread.start()

    # Executa a verificação e inicialização dos executáveis especiais
    iniciar_executaveis_especiais(executaveis_especiais, atraso_entre_executaveis_especiais)

    # Cria o ícone da bandeja
    icone_path = 'icone.ico'
    menu = (item('Sair', quit_action),)
    icon = pystray.Icon("Monitoramento", criar_icone(icone_path), "Monitoramento de Executáveis", menu)
    icon.run()

if __name__ == "__main__":
    main()
