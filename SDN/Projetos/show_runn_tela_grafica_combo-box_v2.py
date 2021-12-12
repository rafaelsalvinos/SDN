from PySimpleGUI import PySimpleGUI as sg, Text, Input, Output
from netmiko import ConnectHandler
import datetime

# COMPONENTES DA JANELA

sg.theme('SandyBeach')
layout = [
    [sg.Text('IP', size=(7, 1)), sg.Input(key='ipmgmt')],
    [sg.Text('Usuario', size=(7, 1)), sg.Input(key='usuario')],
    [sg.Text('Senha', size=(7, 1)), sg.Input(key='senha', password_char='*')],
    [sg.Text('Comando', size=(7, 1)), sg.Combo(['show run', 'show ip int brief', 'show ip arp', 'show ip route'], enable_events=True, size=(40,40), key='comando')],
    [sg.Text('Salvar output em...'), sg.Input(key='caminho'), sg.FolderBrowse()],
    [sg.Button('Conectar'), sg.Button('Sair')],
    [sg.Text('Output')],
    [sg.Output(key='output', size=(100,40))]

]

# JANELA

janela = sg.Window('Conexão SSH e outputs para troubleshooting em devices de rede', layout, size=(700,600))

# LEITURA DOS EVENTOS
while True:
    eventos, valores = janela.read()

    enderecoip = valores['ipmgmt']
    user = valores['usuario']
    password = valores['senha']
    comando = valores['comando']
    folder_path = valores['caminho']

# BOTAO SAIR E FECHAMENTO DA TELA

    if eventos == sg.WIN_CLOSE_ATTEMPTED_EVENT or eventos == 'Sair' and sg.popup_yes_no('Deseja realmente sair?') == 'Yes':
        break
        window.close()

    if eventos == 'Conectar':
        if valores['usuario'] == 'admin' and valores['senha'] == 'cisco':
            print('Usuário Autenticado')

            # LISTA SWITCHES
            SWITCH1 = {
                'device_type': 'cisco_ios',
                'username': user,
                'host': enderecoip,
                'password': password,  # SENHA
                'secret': password,  # SECRET
            }

            lista_switches = [SWITCH1]
            # LAÇO PARA EXECUTAR O COMANDO SHOW RUNNING EM CADA EQUPAMENTO DA LISTA
            for switches in lista_switches:
                try:
                    # ABRINDO CONEXAO SSH
                    connect = ConnectHandler(**switches)
                    # ENTRANDO EM MODO PRIVILEGIADO
                    connect.enable()
                    # EXECUTANDO O COMANDO SHOW RUNNING
                    configure = connect.send_command(comando)
                    print(configure)
                    print(folder_path)
                    valores['output'] = configure
                    # NOME DO ARQUIVO COM DATA E HORA
                    NOME_ARQUIVO_BKP = folder_path + "/" + switches['host'] + "_" + datetime.datetime.now().strftime(
                        "%Y-%m-%d_%Hh%Mm%Ss") + ".txt"
                    # ESCREVER NO ARQUIVO A SAIDA DO COMANDO SHOW RUNN
                    with open(NOME_ARQUIVO_BKP, "w") as fh:
                        fh.write(configure)
                    # SAIR DO MODO DE ACESSO PRIVILEGIADO DO EQUIPAMENTO
                    connect.exit_enable_mode()
                    # FECHANDO A SESSAO SSH
                    print("Backup concluído com sucesso")
                    connect.disconnect()
                except:
                    print("Erro ao gerar arquivo de backup do equipamento %s" % switches['host'])

        else:
            sg.popup('Usuário / Senha incorreto')

