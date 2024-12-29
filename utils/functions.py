def validar_e_formatar_cpf(cpf):
    """
    Valida e formata o CPF.
    - Aceita apenas números.
    - Verifica se o CPF tem exatamente 11 dígitos.
    - Retorna o CPF formatado (XXX.XXX.XXX-XX) se válido, ou None se inválido.
    """
    cpf = ''.join(filter(str.isdigit, cpf))  # Remove qualquer caractere que não seja número
    if len(cpf) != 11:
        return None

    # Formatar CPF como XXX.XXX.XXX-XX
    cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf_formatado
