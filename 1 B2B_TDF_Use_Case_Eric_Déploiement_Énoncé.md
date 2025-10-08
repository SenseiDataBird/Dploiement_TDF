# Phase 3 : Déploiement avec Streamlit

## Objectif
Rendre votre modèle XGBoost utilisable par vos collaborateurs non-techniques via une interface web simple.

---

## Prérequis
- Avoir complété les Phases 1 et 2
- Avoir le modèle XGBoost entraîné
- Avoir l'encodeur OneHot sauvegardé

---

## Missions à Accomplir avec l'Aide de Cursor

Vous allez utiliser **Cursor comme assistant IA** pour vous guider dans la création d'une application Streamlit. 

### **Mission 1 : Sauvegarder les Artefacts ML**

**Question :** Comment sauvegarder mon modèle et mes objets de prétraitement pour les réutiliser plus tard ?

**Prompt à donner à Cursor :**
```
J'ai un modèle XGBoost entraîné (variable : model_xgb) et un encodeur OneHot (variable : onehot_encoder) depuis mes notebooks précédents. 

Je veux les sauvegarder pour pouvoir les recharger plus tard dans une application de déploiement. 

Peux-tu me montrer comment :
1. Créer un dossier 'modeles/'
2. Sauvegarder le modèle XGBoost avec joblib
3. Sauvegarder l'encodeur OneHot avec joblib
4. Sauvegarder les métadonnées (MAE, R², liste des features, médiane des délais) dans un fichier JSON

Fournis-moi le code complet à exécuter dans une cellule de notebook.
```

**Résultat attendu :** Un dossier `modeles/` avec 3 fichiers créés

---

### **Mission 2 : Créer l'Application Streamlit**

**Question :** Comment créer une interface web pour que mes collègues puissent utiliser le modèle sans coder ?

**Prompt à donner à Cursor :**
```
Je veux créer une application Streamlit pour déployer mon modèle de prédiction des délais d'opportunités.

L'application doit :
1. Charger le modèle XGBoost depuis 'modeles/xgboost_model.pkl'
2. Charger l'encodeur OneHot depuis 'modeles/onehot_encoder.pkl'
3. Charger les métadonnées depuis 'modeles/metadata.json'
4. Avoir un formulaire avec les champs :
   - Phase (dropdown : Etude, Réalisation)
   - Client (dropdown : Client_1, Client_2, Client_3, Client_4)
   - Produit (dropdown : liste des produits du dataset)
   - Macro Produit (dropdown : Evolution PoP, Nouveau PoP)
   - Mois de création (slider : 1 à 12)
5. Un bouton "Prédire le délai"
6. Afficher le résultat avec un code couleur :
   - Vert si < 30 jours (rapide)
   - Orange si 30-60 jours (moyen)
   - Rouge si > 60 jours (lent)
7. Comparer avec la médiane historique

Crée-moi le fichier complet 'app.py' avec tous les imports nécessaires.
```

**Résultat attendu :** Un fichier `app.py` créé

---

### **Mission 3 : Tester l'Application Localement**

**Question :** Comment lancer mon application Streamlit sur mon ordinateur ?

**Prompt à donner à Cursor :**
```
J'ai créé mon fichier app.py avec Streamlit. 

Peux-tu me donner :
1. La commande pour installer Streamlit (si je ne l'ai pas)
2. La commande pour lancer l'application
3. Comment accéder à l'application dans mon navigateur
4. Comment arrêter l'application

Donne-moi aussi un fichier requirements.txt avec toutes les dépendances nécessaires.
```

**Résultat attendu :** Application qui s'ouvre dans le navigateur à `http://localhost:8501`

---

### **Mission 4 : Créer une Documentation Utilisateur**

**Question :** Comment expliquer à mes collègues comment utiliser cette application ?

**Prompt à donner à Cursor :**
```
Crée-moi un fichier README_UTILISATEUR.md simple pour mes collègues non-techniques.

Il doit expliquer :
1. À quoi sert cette application (prédire les délais d'opportunités)
2. Comment lancer l'application (étape par étape, très simple)
3. Comment remplir le formulaire
4. Comment interpréter les résultats
5. Qui contacter en cas de problème (mettre un placeholder "[Votre Nom]")

Utilise un ton simple et des emojis pour rendre ça engageant.
```

**Résultat attendu :** Un fichier `README_UTILISATEUR.md` créé

---

### **Mission 5 : Créer un Script de Prédiction par Batch**

**Question :** Et si j'ai plusieurs opportunités à prédire en une fois ?

**Prompt à donner à Cursor :**
```
Je veux créer un script Python qui permet de prédire les délais pour plusieurs opportunités en même temps à partir d'un fichier CSV.

Crée-moi un fichier 'predire_batch.py' qui :
1. Charge le modèle et l'encodeur depuis le dossier modeles/
2. Lit un fichier CSV 'nouvelles_opportunites.csv' avec les colonnes : phase, client, produit, macro_produit, mois_creation
3. Applique les prédictions sur toutes les lignes
4. Ajoute une colonne 'delai_predit' 
5. Ajoute une colonne 'statut' (Rapide/Moyen/Lent)
6. Sauvegarde le résultat dans 'opportunites_avec_predictions.csv'

Fournis aussi un exemple de fichier CSV 'nouvelles_opportunites.csv' avec 3 lignes d'exemple.
```

**Résultat attendu :** Scripts pour prédictions automatisées

---

## Checklist de Validation

À la fin, vous devez avoir :
- [ ] Dossier `modeles/` avec 3 fichiers (.pkl + .json)
- [ ] Fichier `app.py` fonctionnel
- [ ] Fichier `requirements.txt`
- [ ] Fichier `README_UTILISATEUR.md`
- [ ] Fichier `predire_batch.py`
- [ ] Fichier exemple `nouvelles_opportunites.csv`
- [ ] Application qui se lance sans erreur

---

## Apprentissages Clés

- **Joblib** : Sérialisation des modèles ML (standard industrie)
- **Streamlit** : Framework pour créer des interfaces web rapidement
- **Déploiement local** : Première étape avant le cloud
- **Documentation** : Essentielle pour l'adoption par les utilisateurs

---

## Pour Aller Plus Loin (Optionnel)

Si vous voulez partager votre application avec des collègues distants :

**Prompt à donner à Cursor :**
```
Comment puis-je partager mon application Streamlit avec des collègues qui ne sont pas sur mon réseau local ?

Explique-moi :
1. Les options gratuites (Streamlit Cloud, Hugging Face Spaces)
2. Comment déployer sur Streamlit Cloud étape par étape
3. Les limitations de la version gratuite
```

---

**Bon déploiement !**

