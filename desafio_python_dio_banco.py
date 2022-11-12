
AGENCIA = "0001"
limite_saques = 0
lista_saldo = list()
lista_deposito = list()
lista_saque = list()
dicionario_usuario = dict()
lista_usuario = list()
lista_contas = list()

def menu(nome):
    menu = f'''
================================
        CLIENTE:. {nome}
================================
[d]     Depositar
[s]     saque
[e]     Extrato
[nc]    Nova conta
[lc]    Listar contas
[nu]    Novo usuário
[q]     Sair
================================
=>> '''
    op = input(menu)
    return op

def ftexto(texto,sinal = "="):
    tamanho = len(texto) + 4
    print(sinal * tamanho)
    print(texto.center(tamanho))
    print(sinal * tamanho)

def confereint(valor,/):
    try:
        valor = float(valor)
        return valor
    except:
        ftexto('Erro, coloque um número válido')
        return 0

def depositar(valor,saque=False,/):
    valor = confereint(valor)
    if saque and lista_deposito != []:
        lista_deposito.append(0)
    elif valor > 0:
        ftexto(">>> Deposito realizado com sucesso! <<<",'-')
        ftexto(f'---> Foi depositado R$ {valor:.2f} em sua conta <---')
        lista_deposito.append(valor)
        if lista_saldo != []:
            saldo = lista_saldo[-1]
            saldo += valor
            lista_saldo.append(saldo)
        else:
            lista_saldo.append(valor)
    else:
        ftexto('Valor inválido')

def saque(*,saque, depositar=False):
    saque = confereint(saque)
    if depositar:
        lista_saque.append(0)
    else:
        if lista_saldo != []:
            saldo = lista_saldo[-1]
            total = saldo - saque
            if saldo > 0 and total >= 0 and saque > 0:
                if saque <= 500:
                    ftexto(">>> Saque realizado com sucesso! <<<",'-')
                    ftexto(f'---> Foi sacado R$ {saque:.2f} da sua conta <---')
                    saldo -= saque
                    lista_saque.append(saque)
                    lista_saldo.append(saldo)
                    return True
                else:
                    ftexto('>>>>> Seu limite de saques é de até R$ 500,00 <<<<<','+')
                    return False
            else:
                ftexto('>>>>> Saldo insuficiente <<<<<','+')
                return False
        else:
            ftexto('>>>>>Verifique se você tem saldo<<<<<','-')
            ftexto('Verifique se Digitou um número válido','-')
            return False

def extrato(nome,/,*,cpf):
    for n in range(len(lista_saldo)):
        ftexto(f'{n+1}° Movimentação do usuario {nome} de CPF {cpf}','-')
        print(f'Você depositou: R$ {lista_deposito[n]:.2f}')
        print(f'Você sacou: R$ {lista_saque[n]:.2f}')
        print(f'Seu Saldo: R$ {lista_saldo[n]:.2f}\n')

def novousuario(nome,cpf,/,*,data_nascimento):
    usuario = {'Nome':nome,'CPF':cpf,'data_nascimento':data_nascimento}
    lista_usuario.append(usuario)
    dicionario_usuario.update(usuario)

def novaconta(cpf, agencia, numero_conta, **dusuario):
    if cpf == dusuario.get('CPF'):
        ftexto('-----> Nova conta criada com sucesso! <---- -')
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": dusuario.get('Nome')}
    else:
        if verificaduplicacao(cpf):
            ftexto('>>>>> Esse CPF não esta registrado <<<<<')
        return False

def listar_contas(contas):
    for conta in lista_contas:
        print("-----------------------")
        print(f"Agência: {conta['agencia']}")
        print(f"C/C:     {conta['numero_conta']}")
        print(f"Titular: {conta['usuario']}")
        print("-----------------------")

def verificaduplicacao(cpf):
    if validacaocpf(cpf):
        if lista_usuario == []:
            return True
        else:
            for cp in range(len(lista_usuario)):
                lista_usuario[cp].get('CPF')
                if lista_usuario[cp].get('CPF') not in cpf:
                    return True
                else:
                    ftexto('>>>>> CPF Duplicado <<<<<','+')
                    return False
            return False

def verificadono(cpf):
    if validacaocpf(cpf):
        if dicionario_usuario.get('CPF') == cpf:
            return True
        else:
            for cp in range(len(lista_usuario)):
                lista_usuario[cp].get('CPF')
                if lista_usuario[cp].get('CPF') in cpf:
                    ftexto('>>>>> CPF Duplicado <<<<<','+')
                    return False
                else:
                    ftexto('>>>>> CPF não cadastrado <<<<<','+')
                    return False
    else:
        return False

def validacaocpf(cpf):
    cpf.replace(" ", "").replace(".","").replace("-","")
    try:
        cpfint = int(cpf)#so pra saber se tinha letra, e entraria no except
        #ja que nao deu erro volto para string
        if len(cpf)==11:
            return True
        else:
            ftexto(">>>>> Erro, o CPF deve conter 11 Digitos <<<<<")
            return False
    except:
        ftexto(">>>>> Erro, coloque somente numeros <<<<<")
        return False

def primeiraconta():
    ftexto('===> Crie primeiro uma conta <===','-')
    ftexto('----- CADASTRO- ----','=')
    nome=str(input("Digite o seu nome: "))
    cpf=str(input("Digite o seu CPF: "))
    verificarcpf = verificaduplicacao(cpf)
    if verificarcpf:
        data_nascimento=str(input("Digite a sua data de nascimento: "))
        novousuario(nome,cpf,data_nascimento=data_nascimento)
        return True


while True:
    if dicionario_usuario == {}:
        primeiraconta()
    else:
        opcao = menu(dicionario_usuario.get('Nome'))
        if opcao == 'd':
            valor = input('Qual o valor do deposito? ')
            depositar(valor)
            saque(saque = 0, depositar = True)

        elif opcao == 's':
            if limite_saques < 3:
                valor = input('Qual o valor do saque? ')
                if saque(saque=valor):
                    depositar(0,True)
                    limite_saques += 1
            else:
                ftexto('>>>>> Já completou seu limite de saques <<<<<',"+")

        elif opcao == 'e':
            extrato(dicionario_usuario.get('Nome'),cpf=dicionario_usuario.get('CPF'))

        elif opcao == 'nc':
            ftexto('----> Criando nova conta <----')
            cpf=str(input("Digite o seu CPF: "))
            verificarcpf = verificadono(cpf)
            if verificarcpf:
                numero_conta = len(lista_contas)+1
                conta = novaconta(cpf=cpf, agencia=AGENCIA, numero_conta=numero_conta, **dicionario_usuario)
                lista_contas.append(conta)

            elif verificarcpf == "cpfduplicado":

                ftexto(">>>>> Esse CPF não corresponde ao seu <<<<<",'-')

        elif opcao == 'lc':
            if lista_contas != []:
                listar_contas(lista_contas)
            else:
                ftexto(">>> Você só tem a conta padrão, Crie uma conta com [nc] <<<")

        elif opcao == 'nu':
            if primeiraconta():
                print("entrou")
                lista_saldo.clear()
                lista_saque.clear()
                lista_deposito.clear()
                conta.clear()
                lista_contas.clear()
                limite_saques = 0

        elif opcao == 'q':
            break
