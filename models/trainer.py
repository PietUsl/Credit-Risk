"""
Model Trainer - Allena il modello di Credit Risk

Riceve il DataFrame pulito dal cleaner e allena un modello ML
"""

import pandas as pd
import logging
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os

logger = logging.getLogger(__name__)


class ModelTrainer:
    """Allena il modello di Credit Risk"""

    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = None

    def preprocess_data(self, df: pd.DataFrame):
        """Prepara i dati per il modello"""
        df = df.copy()

        # Separa target
        X = df.drop('loan_status', axis=1)
        y = df['loan_status']

        # Encoding delle categoriche
        categorical_cols = ['person_home_ownership', 'loan_intent', 'loan_grade', 'cb_person_default_on_file']

        for col in categorical_cols:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
            X[col] = self.label_encoders[col].fit_transform(X[col])

        # Salva i nomi delle feature
        self.feature_names = X.columns.tolist()

        return X, y

    def train(self, df_clean: pd.DataFrame, test_size=0.2):
        """Allena il modello usando il DataFrame pulito"""
        logger.info("🤖 MODEL: Training del modello...")

        # Preprocessing
        X, y = self.preprocess_data(df_clean)

        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

        # Scaling
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Training
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )

        self.model.fit(X_train_scaled, y_train)

        # Score
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)

        logger.info(".3f")
        logger.info(".3f")

        # Salva il modello
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.model, 'models/credit_risk_model.pkl')
        joblib.dump(self.scaler, 'models/scaler.pkl')
        joblib.dump(self.label_encoders, 'models/label_encoders.pkl')

        logger.info("✅ Modello salvato in models/")

        return {
            'train_score': train_score,
            'test_score': test_score,
            'model': self.model
        }

    def predict(self, df_new: pd.DataFrame):
        """Fa predizioni su nuovi dati"""
        if self.model is None:
            raise ValueError("Modello non allenato!")

        # Preprocessing degli stessi dati
        X, _ = self.preprocess_data(df_new)
        X_scaled = self.scaler.transform(X)

        # Predizioni
        predictions = self.model.predict(X_scaled)
        probabilities = self.model.predict_proba(X_scaled)[:, 1]

        return predictions, probabilities