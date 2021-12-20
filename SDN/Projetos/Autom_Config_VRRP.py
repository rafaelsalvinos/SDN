from PySimpleGUI import PySimpleGUI as sg, Text, Input, Output
from netmiko import ConnectHandler

# COMPONENTES DA JANELA

sg.theme('SandyBeach')
layout = [

    [sg.Text('---------------------------------------------------------------------------------------------------------')],
    [sg.Text('Acesso ao Equipamento')],
    [sg.Text('IP Mgmt', size=(7, 1)), sg.Input(key='ipmgmt', size=(15, 1))],
    [sg.Text('Usuario', size=(7, 1)), sg.Input(key='usuario', size=(15, 1))],
    [sg.Text('Senha', size=(7, 1)), sg.Input(key='senha', password_char='*', size=(15, 1))],

    [sg.Text('---------------------------------------------------------------------------------------------------------')],
    [sg.Text('Configuração da Interface')],
    [sg.Text('Interface', size=(7, 1)), sg.Combo(['Ethernet0/0', 'Ethernet0/1', 'Ethernet0/2', 'Ethernet0/3'], enable_events=True, size=(15,40), key='interface'), sg.Text('IP Interface', size=(8, 1)), sg.Input(key='ip_interface', size=(15, 1)), sg.Text('Mask', size=(4, 1)), sg.Input(key='mask', size=(15, 1))],
    [sg.Text('---------------------------------------------------------------------------------------------------------')],
    [sg.Text('Configurações de VRRP')],
    [sg.Text('VRRP Group', size=(10, 1)), sg.Input(key='vrrp_group', size=(3, 1)), sg.Text('IP Virtual', size=(7, 1)), sg.Input(key='vip', size=(15, 1)), sg.Text('Prioridade', size=(7, 1)), sg.Input(key='prioridade',  size=(3, 1)),sg.Text('Autenticação VRRP', size=(15, 1)), sg.Input(key='autenticacao_vrrp', size=(10, 1))],

    [sg.Button('Aplicar')],
[sg.Text('---------------------------------------------------------------------------------------------------------')],
    [sg.Text('Troubleshooting')],
    [sg.Text('Comando', size=(7, 1)), sg.Combo(['show vrrp', 'show vrrp brief', 'show vrrp all'], enable_events=True, size=(15,40), key='comando')],
    [sg.Button('Executar')],
    [sg.Text('Output')],
    [sg.Output(key='output', size=(100,40))]
]

# JANELA

janela = sg.Window('Cofiguração de VRRP', layout, size=(700,600))

# LEITURA DOS EVENTOS
while True:
    eventos, valores = janela.read()

# DECLARACAO DE VARIAVEIS

    enderecoip = valores['ipmgmt']
    user = valores['usuario']
    password = valores['senha']
    interface = valores['interface']
    ip_interface = valores['ip_interface']
    mask = valores['mask']
    vrrp_group = valores['vrrp_group']
    vip = valores['vip']
    prioridade = valores['prioridade']
    autenticacao_vrrp = valores['autenticacao_vrrp']
    comando = valores['comando']

# BOTAO APLICAR CONFIGURAÇÃO

    if eventos == 'Aplicar':
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
            # LAÇO PARA EXECUTAR O COMANDO DE CONFIGURAÇÃO PARA O IP DO SWITCH INFORMADO
            for switches in lista_switches:
                try:
                    # ABRINDO CONEXAO SSH
                    connect = ConnectHandler(**switches)
                    # ENTRANDO EM MODO PRIVILEGIADO
                    connect.enable()
                    # EXECUTANDO O COMANDO SHOW RUNNING
                    aplica_config = ('int' + " " + interface, 'ip address' + " " + ip_interface + " " + mask, "vrrp" + " " + vrrp_group + " " + 'ip' + " " + vip, "vrrp" + " " + vrrp_group + " " + 'priority' + " " + prioridade,  "vrrp" + " " + vrrp_group + " " + 'authentication' + " " + autenticacao_vrrp, 'no shutdown')
                    configure = connect.send_config_set(aplica_config)
                    print(configure)
                    valores['output'] = configure
                    # SAIR DO MODO DE ACESSO PRIVILEGIADO DO EQUIPAMENTO
                    connect.exit_enable_mode()
                    # FECHANDO A SESSAO SSH
                    print("Configuração Aplicada com Sucesso")
                    connect.disconnect()
                except:
                    print("Erro ao gerar arquivo de backup do equipamento %s" % switches['host'])

        else:
            sg.popup('Usuário / Senha incorreto')

    if eventos == 'Executar':

        SWITCH1 = {
            'device_type': 'cisco_ios',
            'username': user,
            'host': enderecoip,
            'password': password,  # SENHA
            'secret': password,  # SECRET
        }
        lista_switches = [SWITCH1]
        # LAÇO PARA EXECUTAR O COMANDO SHOW PARA O EQUIPAMENTO INFORMADO
        for switches in lista_switches:
            try:
                # ABRINDO CONEXAO SSH
                connect = ConnectHandler(**switches)
                # ENTRANDO EM MODO PRIVILEGIADO
                connect.enable()
                # EXECUTANDO O COMANDO SHOW
                show = connect.send_command(comando)
                print(show)
                valores['output'] = show
            except:
                print('Equipamento inacessível')

