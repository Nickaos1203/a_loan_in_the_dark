# A Loan in the Dark - Application Django

## Présentation du projet  
**"A Loan in the Dark"** est une application web développée avec Django permettant de gérer des demandes de prêts bancaires. Elle intègre un système d'évaluation des risques pour aider les conseillers à prendre des décisions éclairées.

## Fonctionnalités principales  
### Gestion des utilisateurs  
- Authentification et rôles (clients/conseillers)  
- Profils utilisateurs avec photos  

### Module de prêts  
- Création et modification de demandes  
- Interface dédiée pour les conseillers  

### Système de chat  
- Communication en temps réel avec WebSockets  
- Messages privés entre clients et conseillers  

### Actualités  
- Publication et consultation d'articles  

## Technologies utilisées  
- **Django 5.0.0**  
- **Channels** (WebSockets)  
- **SQL Server / SQLite**  
- **Bootstrap 5**  
- **Docker**  

## Installation et démarrage  
### Sans Docker  
pip install -r requirements.txt  
python temp_sqlite.py  # Pour utiliser SQLite  
python manage.py migrate  
python init_db.py  
python manage.py runserver  

### Avec Docker  
docker build -t loan-django-app .  
docker run -p 8000:8000 loan-django-app  

## Utilisateurs par défaut  
**Conseillers :**  
- vic@staff.fr / password1234  
- nico@staff.fr / password1234  
- leo@staff.fr / password1234  

## Structure du projet  
- **accounts** : Gestion des utilisateurs  
- **loans** : Gestion des demandes de prêt  
- **chat** : Système de messagerie  
- **news** : Actualités  

## Futures améliorations  
- Intégration complète du module de prédiction  
- Amélioration de l'interface utilisateur  

