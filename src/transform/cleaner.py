import pandas as pd
import logging

logger = logging.getLogger(__name__)


class DataCleaner:
    """Pulizia semplice del dataset Credit Risk"""
    
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Pulisci il dataset"""
        df = df.copy()
        initial_rows = len(df)
        
        # 1. Rimuovi duplicati
        df = df.drop_duplicates()
        logger.info(f"Rimossi {initial_rows - len(df)} duplicati")
        
        # 2. Rimuovi righe con target mancante
        df = df.dropna(subset=['loan_status'])
        
        # 3. Riempi valori nulli con mediana (numerici)
        numeric_cols = ['person_age', 'person_income', 'person_emp_length',
                       'loan_amnt', 'loan_int_rate', 'loan_percent_income',
                       'cb_person_cred_hist_length']
        for col in numeric_cols:
            df[col] = df[col].fillna(df[col].median())
        
        # 4. Riempi valori nulli con moda (categorici)
        categorical_cols = ['person_home_ownership', 'loan_intent', 'loan_grade',
                           'cb_person_default_on_file']
        for col in categorical_cols:
            if df[col].isna().sum() > 0:
                df[col] = df[col].fillna(df[col].mode()[0])
        
        # 5. Converti tipi
        df['person_age'] = df['person_age'].astype('int32')
        df['person_income'] = df['person_income'].astype('int32')
        df['loan_amnt'] = df['loan_amnt'].astype('int32')
        df['loan_int_rate'] = df['loan_int_rate'].astype('float32')
        df['loan_status'] = df['loan_status'].astype('int8')
        df['cb_person_cred_hist_length'] = df['cb_person_cred_hist_length'].astype('int8')
        
        logger.info(f"Pulizia completata - Righe iniziali: {initial_rows}, Finali: {len(df)}")
        return df

