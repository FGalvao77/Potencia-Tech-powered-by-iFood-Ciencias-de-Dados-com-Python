import textwrap

def menu():

    MENU = '''
    ============= MENU =============
    \t[D] ==> Depositar
    \t[S] ==> Sacar
    \t[E] ==> Extrato

    \t[AC] ==> Abrir (nova) conta
    \t[LC] ==> Listar contas ativas
    \t[NC] ==> Cadastrar novo cliente
    
    \t[X] ==> Sair
    '''
    return input(MENU).upper()
    #return input(textwrap.dedent(MENU).upper())


def deposito(saldo, valor, extrato, /):
    
    if valor > 0:
        saldo += valor
        extrato += f'Depósito de: \tR$ {valor:.2f}\n'
        print('\nDepósito realizado com SUCESSO!!!')

    else:
        print(f'Operação FALHOU! O valor informado é INVÁLIDO!!!')

    return saldo, extrato


def saque(*, saldo, valor, extrato, limite_valor, numero_saques, limite_saques):

    excedido_saldo = valor > saldo
    excedido_limite = valor > limite_valor
    excedido_saques = numero_saques >= limite_saques

    if excedido_saldo:
        print('\nOperação FALHOU! \nSALDO INSUFICIENTE!!!')
    
    elif excedido_limite:
        print('\nOperação FALHOU! \nSAQUE SUPERIOR AO SEU LIMITE!!!')
        
    elif excedido_saques:
        print('\nOperação FALHOU! \nQUANTIDADE DE SAQUES EXCEDIDO LIMITE DO DIA!!!')
        
    elif valor > 0:
        saldo -= valor
        extrato += f'Saque: \tR$ {valor:.2f}\n'
        numero_saques += 1
        print('\nSaque realizado com SUCESSO!!!')

    else:
        print('\nOperação FALHOU! \nO valor informado é INVÁLIDO. Por favor, tente novamente!!!')

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print('=========== EXTRATO ===========')
    print('Conta sem movimentações.' if not extrato else extrato)
    print(f'\nSaldo: \tR$ {saldo:.2f}')
    print('===============================')


def cadastrar_cliente(clientes):
    cpf = input('Informe o CPF (somente número): ')
    cliente = filtrar_clientes(cpf, clientes)

    if cliente:
        print('Já existe cliente com esse CPF!!!')
        return None

    nome = input('Informe o nome completo: ')
    data_nasc = input('Informe a data de nascimento (dd-mm-aaaa): ')
    endereco = input('Informe o endereço (logradouro, nº - bairro - cidade/sigla estado): ')

    clientes.append({'nome': nome,
                     'data_nascimento': data_nasc,
                     'cpf': cpf,
                     'endereco': endereco})

    print('###### CLIENTE CADASTRADO COM SUCESSO!!! ######')


def filtrar_clientes(cpf, clientes):
    clientes_filtro = [cliente for cliente in clientes if cliente['cpf'] == cpf]
    return clientes_filtro[0] if clientes_filtro else None


def abrir_conta(agencia, num_conta, clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_clientes(cpf, clientes)

    if cliente:
        print('=========== CONTA CRIADA COM SUCESSO!!! ==========')
        return {'agencia': agencia, 
                'numero_conta': num_conta, 
                'cliente': cliente}

    print('Cliente NÃO encontrado! | Encerrando processo de criação da conta!!!')


def listar_contas(contas):
    for conta in contas:
        linha = f'''
            AGÊNCIA: {conta['agencia']}
            C/C: {conta['numero_conta']}
            TITULAR: {conta['cliente']['nome']}
        '''
        print('=' * 100)
        print(textwrap.dedent(linha))
    

def main():
    LIMITE_SAQUES = 3
    AGENCIA = '0001'

    saldo = 0
    limite_valor = 500
    extrato = ''
    numero_saques = 0
    clientes = []
    contas = []

    while True:

        opcao = menu()

        if opcao == 'D':
            valor = float(input('Informe o valor do depósito: '))
            saldo, extrato = deposito(saldo, valor, extrato)

        elif opcao == 'S':
            valor = float(input('Informe o valor do saque: '))
            saldo, extrato = saque(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite_valor=limite_valor,
                numero_saques=numero_saques,
                limite_saques = LIMITE_SAQUES
            )

        elif opcao == 'E':
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == 'NC':
            cadastrar_cliente(clientes)

        elif opcao == 'AC':
            num_conta = len(contas) + 1
            conta = abrir_conta(AGENCIA, num_conta, clientes)

            if conta:
                contas.append(conta)

        elif opcao == 'LC':
            listar_contas(contas)

        elif opcao == 'X':
            print('\n\nSaindo... \nVOLTE SEMPRE!!! :)')
            break

        else:
            print('\nOpção INVÁLIDA!. \nPOR FAVOR! Escolha uma opção válida do MENU e tente novamente ;)')


main()