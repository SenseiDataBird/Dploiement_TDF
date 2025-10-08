"""
Script de Sauvegarde des Modèles et Artefacts
À exécuter depuis le notebook de la Phase 2
"""

import joblib
import json
import os
import sys
from datetime import datetime

# Naviguer vers le dossier du notebook Phase 2
notebook_dir = "../../2. Modeling"
if os.path.exists(notebook_dir):
    os.chdir(notebook_dir)
    print(f"📂 Répertoire de travail : {os.getcwd()}\n")
else:
    print("⚠️ Assurez-vous d'exécuter ce script depuis le dossier de déploiement")

# Vérifier que les variables existent
try:
    # Ces variables doivent exister dans le notebook de la Phase 2
    model_xgb
    onehot_encoder
    mae
    r2
    df_ml
except NameError as e:
    print(f"❌ Erreur : Variable manquante - {e}")
    print("\n💡 Ce script doit être exécuté depuis le notebook Phase 2")
    print("   où les variables model_xgb, onehot_encoder, mae, r2 et df_ml sont définies")
    sys.exit(1)

# Créer le dossier modeles/ dans le dossier de déploiement
modeles_dir = "../3. Deploiement/2 B2B_TDF_Use_Case_Eric_Déploiement_Correction/modeles"
os.makedirs(modeles_dir, exist_ok=True)

print("🔧 Sauvegarde des modèles en cours...\n")

# 1. Sauvegarder le modèle XGBoost
model_path = os.path.join(modeles_dir, "xgboost_model.joblib")
joblib.dump(model_xgb, model_path)
print(f"✅ Modèle XGBoost sauvegardé : {model_path}")

# 2. Sauvegarder l'encodeur OneHot
encoder_path = os.path.join(modeles_dir, "onehot_encoder.joblib")
joblib.dump(onehot_encoder, encoder_path)
print(f"✅ Encodeur OneHot sauvegardé : {encoder_path}")

# 3. Sauvegarder les métadonnées (simplifiées)
metadata = {
    'date_entrainement': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'mae': float(mae),
    'r2': float(r2),
    'features': ['phase', 'client', 'macro_produit', 'produit', 'mois_creation']
}

metadata_path = os.path.join(modeles_dir, "metadata.json")
with open(metadata_path, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, indent=4, ensure_ascii=False)
print(f"✅ Métadonnées sauvegardées : {metadata_path}")

print("\n🎉 Tous les artefacts ont été sauvegardés avec succès!")
print("\nFichiers créés :")
print(f"  - {model_path}")
print(f"  - {encoder_path}")
print(f"  - {metadata_path}")

