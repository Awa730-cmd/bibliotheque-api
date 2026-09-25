Question 1 : Choix du sujet et justification
Sujet retenu : Sujet A — API de gestion de bibliothèque.

On a choisi la bibliothèque parce que c'est un sujet simple à comprendre mais avec de vraies règles métier : la limite de 3 livres par membre, la vérification de la disponibilité et la différence entre les rôles. Ça nous a permis de manipuler des cas réels de réponses HTTP, comme renvoyer un code 409 Conflict quand un livre ne peut pas être emprunté.

Question 2 : Tableau des ressources et justification des écarts

Ressource : User

URL Collection : /api/v1/auth/register

URL Élément : /api/v1/auth/me

Méthodes autorisées : POST, GET

Codes de succès : 201 (création), 200 (lecture)

Justification des écarts : L'accès à la ressource utilisateur passe uniquement par les routes d'authentification (register, login, me) au lieu d'un CRUD ouvert pour des raisons de sécurité.
-----------------------------------------------------------------------------------------------
Ressource : Book

URL Collection : /api/v1/books

URL Élément : /api/v1/books/<id>

Méthodes autorisées : GET, POST, PUT, DELETE

Codes de succès : 200 (succès), 201 (créé), 204 (supprimé)

Justification des écarts : Les opérations de modification (POST, PUT, DELETE) sont strictement réservées au rôle staff.
---------------------------------------------------------------------------------------------------------
Ressource : Author

URL Collection : /api/v1/authors

URL Élément : /api/v1/authors/<id>

Méthodes autorisées : GET, POST

Codes de succès : 200 (succès), 201 (créé)

Justification des écarts : Ajout de l'endpoint /api/v1/authors/<id>/books pour récupérer directement la liste des livres d'un auteur.
--------------------------------------------------------------------------------------------------------
Ressource : Loan

URL Collection : /api/v1/loans

URL Élément : /api/v1/loans/<id>

Méthodes autorisées : GET, POST, PUT

Codes de succès : 200 (succès), 201 (créé)

Justification des écarts : Suppression (DELETE) désactivée pour préserver l'historique d'emprunt. La restitution s'effectue via PUT /api/v1/loans/<id>/return.

Question 3 : Codes d'erreur fréquents et situations métier
401 Unauthorized : Un utilisateur tente d'accéder à la route d'emprunt (POST /api/v1/loans) ou à son profil (/me) sans fournir un en-tête Authorization: Bearer <token> valide.
-----------------------------------------------------------------------------------------------------
403 Forbidden : Un utilisateur ayant le rôle member tente d'ajouter un nouveau livre dans le catalogue via POST /api/v1/books, action strictement réservée au rôle staff.
------------------------------------------------------------------------------------------------------
409 Conflict : Un membre tente d'emprunter un livre dont l'attribut available vaut False, ou tente un emprunt alors qu'il a déjà 3 emprunts actifs en cours.

Question 4 : Schémas JSON standardisés
Réponse d'erreur unique : {
  "error": "Le livre sélectionné n'est pas disponible actuellement.",
  "code": 409
}
-----------------------------------------------------------------------------
Réponse de collection paginée : {
  "data": [
    { "id": 1, "title": "Les Misérables", "available": true }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total_items": 25,
    "total_pages": 3
  }
}
------------------------------------------------------------------------------------
Question 5 : Modèle de données et stratégies de chargement (Lazy vs Eager)
Relations et Cardinalités : 
User (1) <---> (N) Loan (Clé étrangère user_id dans Loan). 
Book (1) <---> (N) Loan (Clé étrangère book_id dans Loan).  
Author (1) <---> (N) Book (Clé étrangère author_id dans Book). 

Choix des stratégies de chargement (Lazy vs Eager)
Lazy Loading (Chargement différé - lazy='select'): Utilisé pour les relations User.loans et Author.books. Les emprunts d'un utilisateur ou les livres d'un auteur ne sont récupérés en base de données que si on en a réellement besoin. Cela évite de charger des données inutiles lors d'une simple affichage de profil.
--------------------------------------------------------------------------------------------------------
Eager Loading (Chargement immédiat - joinedload): Utilisé dans le LoanService lors de la récupération des emprunts. On charge directement les informations du livre et de l'utilisateur dans une seule et unique requête SQL, ce qui évite de ralentir l'application en multipliant les requêtes (problème du N+1).

# API REST de Gestion de Bibliothèque (Bibliotheque-API)

API REST modulaire et sécurisée conçue avec Flask, permettant de gérer un catalogue universitaire et le flux complet des emprunts de livres.

---

## 🚀 Fonctionnalités
- **Authentification & Sécurité** : Inscription, connexion, jetons JWT (Access/Refresh), contrôle d'accès basé sur les rôles (`member` vs `staff`).
- **Gestion du Catalogue** : CRUD complet des livres et des auteurs avec pagination et recherche.
- **Gestion des Emprunts** : Réservation, retour, limite de 3 emprunts simultanés, blocage des livres indisponibles.
- **Documentation OpenAPI** : Interface Swagger UI accessible sur `/docs/`.
- **Santé de l'Application** : Endpoint `/health` avec contrôle en temps réel de la connexion à la base de données.

---

## 🛠️ Stack Technique
- **Backend** : Python 3.13, Flask
- **ORM & Migrations** : SQLAlchemy, Flask-Migrate (Alembic)
- **Validation & Sérialisation** : Marshmallow
- **Authentification** : Flask-JWT-Extended
- **Tests & Couverture** : Pytest, Pytest-Cov (Couverture ≥ 70%)
- **Conteneurisation** : Docker, Docker Compose

---

## Installation et Lancement

# Avec Docker Compose (Recommandé)

1.  S'assurer que **Docker Desktop** est démarré.
2. Lancer l'application :
   ```bash 
   docker compose up -d --build 
   ```

L'API est accessible sur : http://localhost:5000
Pour Vérifier l'état du service : http://localhost:5000/health