# estrazione dei dati
import pandas as pd
import logging
import psycopg2
from typing import Dict, List

# Classe per connessione a postrges
class PostgresConnector:
    def __init__(self, host:str, database:str, user:str, password:str):
        self.connection_params = { # definiamo i parametri da passare alla connessione
            'host': host,
            'database':database,
            'user':user,
            'password':password
        }
        self.logger = logging.getLogger(__name__) # logger per tracciare le operazioni, name è il nome del modulo
    
    def connect(self):        
        """Stabilisce una connessione al database PostgreSQL utilizzando i parametri forniti."""
        try: 
            conn = psycopg2.connect(**self.connection_params) # connessione al database
            return conn
        except Exception as e:
            self.logger.error(f"Errore durante la connessione al database: {e}")
            raise
        
    def fetch_credi_risk_dataset(self) -> pd.DataFrame:
        """Recupera i dati delle opportunità dal database e li restituisce come DataFrame."""
        query = """SELECT * FROM credit_risk;""" # query per recuperare i dati
        try:
            with self.connect() as conn:
                df = pd.read_sql_query(query, conn) # esegue la query e restituisce un DataFrame
                self.logger.info(f"Dati recuperati con successo: {len(df)} record")
                return df
        except Exception as e:
            self.logger.error(f"Errore {e}")
            raise
    # query personalizzata def execute_query(self, query:str) -> pd.DataFrame:...
    