import re

def is_strong_password(password:str, size:int=8, laguage_msg:str='pt-BR') -> tuple[bool, str]:
    """
    Check if the password is strong.

    Args:
        password str: password.
        size int: Minimum password length.
        laguage_msg: message language

    Returns:
        tuple[bool, str]: True if strong or false if weak + message
    """
    if len(password) < size:
        message = {
            'en': f'The password is not the minimum length required. Minimum {size} characters',
            'pt-BR': f'A senha não tem o comprimento mínimo exigido. Mínimo {size} caracteres',
        }
        return False, message[laguage_msg]

    if not re.search(r'[A-Z]', password):
        message = {
            'en': 'Capital letters are mandatory',
            'pt-BR': 'É obrigatória ter letra maiúscula',
        }
        return False, message[laguage_msg]

    if not re.search(r'[a-z]', password):
        message = {
            'en': 'Lowercase letters are mandatory',
            'pt-BR': 'É obrigatória ter letra minuscula',
        }
        return False, message[laguage_msg]

    if not re.search(r'[0-9]', password):
        message = {
            'en': 'It is mandatory to have a number',
            'pt-BR': 'É obrigatório ter numero',
        }
        return False, message[laguage_msg]

    if not re.search(r'[\W_]', password):
        message = {
            'en': 'Special characters is required',
            'pt-BR': 'Caracteres especiais são obrigatórios',
        }
        return False, message[laguage_msg]
    

    message = {
        'en': 'The password is strong',
        'pt-BR': 'A senha é forte',
    }
    return True, message[laguage_msg]


def min_characters(string:str, min_size) -> bool:
    """
    Checks if the string has the minimum required length.

    Args:
        string str: string.
        min_size int: Minimum size length.

    Returns:
        bool
    """
    if len(string) < min_size:
        return False
    return True


def max_characters(string:str, max_size) -> bool:
    """
    Checks if the string has the maximum required length.

    Args:
        string str: string.
        min_size int: maximum size length.

    Returns:
        bool
    """
    if len(string) > max_size:
        return False
    return True


def validate_cpf(cpf: str) -> bool:
    """
    Checks if the cpf is valid.

    Args:
        cpf str: cpf number.

    Returns:
        bool
    """
    cpf = ''.join(filter(str.isdigit, cpf))

    if len(cpf) != 11:
        return False
    
    if cpf == cpf[0] * 11:
        return False

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    primeiro_digito = (soma * 10 % 11) % 10

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    segundo_digito = (soma * 10 % 11) % 10

    return cpf[-2:] == f"{primeiro_digito}{segundo_digito}"