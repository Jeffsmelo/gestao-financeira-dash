import os
from sqlalchemy import create_engine
import urllib.parse 

# 🔐 Dados de conexão
# IMPORTANTE: nunca commitar credenciais reais. Configure estas variáveis de
# ambiente antes de rodar a aplicação (ex.: arquivo .env + python-dotenv,
# ou variáveis de ambiente do sistema/CI).
SERVER = os.environ['DB_SERVER']
DATABASE = os.environ['DB_DATABASE']
USERNAME = os.environ['DB_USERNAME']
PASSWORD = os.environ['DB_PASSWORD']
DRIVER = "ODBC Driver 18 for SQL Server"

# 🔧 String de conexão ODBC
connection_string = (
    f"DRIVER={{{DRIVER}}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

params = urllib.parse.quote_plus(connection_string)

# 🚀 Engine SQLAlchemy
engine = create_engine(
    f"mssql+pyodbc:///?odbc_connect={params}",
    pool_pre_ping=True,
    pool_recycle=3600
)