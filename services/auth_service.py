# services/auth_service.py
import os
import json

# 🔐 Usuário administrador
# NUNCA hardcode senhas reais aqui. Configure via variáveis de ambiente.
USUARIO_MASTER = os.environ['USUARIO_MASTER']
SENHA_MASTER = os.environ['SENHA_MASTER']

# 🔗 Mapeamento simples usuário → CC.
# NUNCA hardcode senhas reais aqui. Carregue de uma variável de ambiente
# (JSON) ou de um arquivo local fora do controle de versão (.gitignore).
#
# Exemplo de variável de ambiente (uma linha, JSON válido):
#   USUARIOS_CC='{"1011": ["xxxx"], "1012": ["xxxx"], ...}'
#
# Ou aponte USUARIOS_CC_FILE para um arquivo .json local (recomendado
# para dicionários grandes como este).
usuarios_cc_file = os.environ.get('USUARIOS_CC_FILE')
if usuarios_cc_file:
    with open(usuarios_cc_file, 'r', encoding='utf-8') as f:
        USUARIOS_CC = json.load(f)
else:
    USUARIOS_CC = json.loads(os.environ['USUARIOS_CC'])


def autenticar(usuario, senha):
    """
    Valida usuário e senha.
    Retorna um dict com dados do usuário ou None.
    """

    if not usuario or not senha:
        return None

    # 🔐 Admin
    if usuario == USUARIO_MASTER:
        if senha == SENHA_MASTER:
            return {
                "usuario": usuario,
                "perfil": "admin",
            }
        return None

    # 👤 Usuário comum
    senha_correta = USUARIOS_CC.get(usuario)

    if not senha_correta:
        return None

    # senha_correta é lista → ['8462']
    if senha == senha_correta[0]:
        return {
            "usuario": usuario,
            "perfil": "usuario",
        }

    return None


def is_master(usuario):
    return usuario == USUARIO_MASTER


def get_cc_permitidos(usuario):
    """
    Retorna uma LISTA de CCs permitidos para o usuário.
    """

    if not usuario:
        return []

    if is_master(usuario):
        # Admin vê tudo
        return []

    # Usuário comum vê apenas o próprio CC
    return [usuario]