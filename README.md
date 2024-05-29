
# Monitoramento de Executáveis

Este script Python monitora a execução de programas específicos e os reinicia automaticamente caso sejam fechados. Ele também possui a funcionalidade de iniciar programas em horários específicos. O script é configurado por meio de um arquivo INI chamado config.ini.
## Funcionalidades

- Monitora a execução de programas definidos no arquivo `config.ini`.
- Reinicia automaticamente os programas monitorados caso sejam fechados.
- Permite iniciar programas em horários específicos.
- Possui um ícone na bandeja do sistema para facilitar o acesso.
- Registra logs de eventos em um arquivo chamado `monitoramento.log`.
## Configuração

O script é configurado por meio de um arquivo **INI** chamado `config.ini`. Este arquivo deve estar na mesma pasta que o script Python. A estrutura do arquivo **INI** é a seguinte:

```ini

[CONFIG.ini]

[Executaveis]
executavel1_nome = Nome do programa 1
executavel1_caminho = Caminho para o programa 1
executavel2_nome = Nome do programa 2
executavel2_caminho = Caminho para o programa 2
...

[ExecutaveisEspeciais]
executavel_especial1_nome = Nome do programa especial 1
executavel_especial1_caminho = Caminho para o programa especial 1
...

[Reinicializacao]
horario1 = HH:MM
horario2 = HH:MM
...

[Monitoramento]
intervalo = Segundos
atraso_executaveis = Segundos
atraso_entre_executaveis_especiais = Segundos

[Logs]
habilitar_logs = 0 (0 para desativar, 1 para ativar)
```

## Exemplo de Configuração:

```ini
[Executaveis]
executavel1_nome = WebCharts.exe
executavel1_caminho = C:\GR7\GR7\WebCharts.exe
executavel2_nome = ServerMobile.exe
executavel2_caminho = C:\GR7\GR7\ServerMobile.exe
executavel3_nome = Atualizacao_FTP.exe
executavel3_caminho = C:\GR7\GR7\Atualizacao_FTP.exe

[ExecutaveisEspeciais]
executavel_especial1_nome = GR7_Iniciar.exe
executavel_especial1_caminho = C:\GR7\GR7\GR7_Iniciar.exe

[Reinicializacao]
horario1 = 16:48
horario2 = 18:30

[Monitoramento]
intervalo = 30
atraso_executaveis = 60
atraso_entre_executaveis_especiais = 60

[Logs]
habilitar_logs = 1
```

## Execução:

O script pode ser executado clicando duas vezes no arquivo verificador.exe. O script será executado em segundo plano e monitorará os programas definidos no arquivo `config.ini`. Um ícone será exibido na bandeja do sistema para facilitar o acesso.

## Considerações:

O script foi compilado para um arquivo EXE para facilitar a distribuição e a execução.
O script requer a instalação das bibliotecas psutil, time, os, logging, configparser, pystray, PIL, threading e datetime para funcionar.
O script é compatível com o sistema operacional Windows.
Documentação Detalhada das Funções:

- `configurar_logging(habilitar_logs):` Configura o registro de logs do script.
- `ler_configuracoes():` Lê o arquivo `config.ini` e retorna as configurações do script.
- `verificar_processo(nome):` Verifica se um processo com o nome especificado está em execução.
- `reabrir_executavel(caminho):` Reabre um programa especificado pelo caminho.
- `fechar_executavel(nome):` Fecha um processo com o nome especificado.
- `iniciar_executaveis(executaveis):` Inicia os programas definidos na lista executaveis.
- `iniciar_executaveis_especiais(executaveis_especiais, - - atraso_entre_executaveis_especiais):` Inicia os programas especiais definidos na lista executaveis_especiais com um atraso entre cada um.
- `reiniciar_executaveis_especiais(executaveis_especiais, horarios_reinicio, atraso_
- `criar_icone(icone_path):` Cria um ícone para a bandeja do sistema a partir do arquivo especificado pelo caminho icone_path.
- `quit_action(icon, item):` Função de callback para o item "Sair" do menu da bandeja do sistema. Fecha o script.
- `main() :` Função principal do script. Chama as demais funções para configurar o script, iniciar os programas e monitorar a execução.
## Observações:

A documentação acima descreve as funções principais do script. Para mais detalhes sobre a implementação de cada função, consulte o código-fonte do script.
O script pode ser adaptado para atender às necessidades específicas do usuário. Por exemplo, o usuário pode adicionar novas funções para monitorar outros tipos de arquivos ou realizar outras tarefas.
É recomendável ler o código-fonte do script antes de fazer qualquer modificação.
Conclusão:

O script Python para monitoramento de executáveis é uma ferramenta útil para garantir que os programas específicos estejam sempre em execução. O script é fácil de configurar e usar, e pode ser adaptado para atender às necessidades específicas do usuário.

 ***FIM_DO_CODIGO***
