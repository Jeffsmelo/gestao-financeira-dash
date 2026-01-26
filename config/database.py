from sqlalchemy import create_engine
import urllib.parse 

# 🔐 Dados de conexão
SERVER = "172.16.10.9"
DATABASE = "Protheus12"
USERNAME = "SOMENTE_VIEW"
PASSWORD = "Pr0th3usV13w_USER"
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