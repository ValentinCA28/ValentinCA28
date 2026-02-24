# Cours Complet : HTTP, APIs & Sécurité

---

## Module 1 — HTTP/HTTPS : Les Fondamentaux du Web

### 1.1 Qu'est-ce que HTTP ?

HTTP (*HyperText Transfer Protocol*) est le protocole de communication qui régit les échanges de données sur le Web. Il fonctionne selon un modèle **client-serveur** : un client (navigateur, script, application) envoie une **requête**, et un serveur renvoie une **réponse**.

HTTP est un protocole **sans état** (*stateless*) : chaque requête est indépendante. Le serveur ne conserve aucune mémoire des requêtes précédentes, ce qui simplifie l'architecture mais nécessite des mécanismes complémentaires (cookies, sessions, tokens) pour maintenir un contexte utilisateur.

### 1.2 Anatomie d'une requête HTTP

Une requête HTTP se compose de plusieurs éléments :

```
GET /api/users/42 HTTP/1.1
Host: example.com
Accept: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...
```

La **ligne de requête** contient la méthode, le chemin de la ressource et la version du protocole. Les **en-têtes** (*headers*) fournissent des métadonnées : type de contenu accepté, authentification, encodage, etc. Le **corps** (*body*), optionnel, transporte des données (formulaires, JSON, fichiers).

### 1.3 Les méthodes HTTP

Chaque méthode exprime une intention sémantique distincte :

| Méthode | Usage | Idempotent | Corps |
|---------|-------|------------|-------|
| `GET` | Lire une ressource | Oui | Non |
| `POST` | Créer une ressource | Non | Oui |
| `PUT` | Remplacer entièrement une ressource | Oui | Oui |
| `PATCH` | Modifier partiellement une ressource | Non | Oui |
| `DELETE` | Supprimer une ressource | Oui | Optionnel |
| `HEAD` | Comme GET, mais sans le corps de réponse | Oui | Non |
| `OPTIONS` | Découvrir les méthodes supportées | Oui | Non |

L'**idempotence** signifie qu'exécuter la même requête plusieurs fois produit le même résultat. C'est une propriété importante pour la fiabilité : si une requête `PUT` échoue en réseau, on peut la renvoyer sans risque de duplication.

### 1.4 Les codes de statut HTTP

Les réponses incluent un code à trois chiffres indiquant le résultat :

- **1xx — Informationnel** : `100 Continue` — le serveur a reçu les en-têtes et attend le corps.
- **2xx — Succès** : `200 OK` (requête réussie), `201 Created` (ressource créée), `204 No Content` (succès sans contenu retourné).
- **3xx — Redirection** : `301 Moved Permanently`, `304 Not Modified` (le cache est encore valide).
- **4xx — Erreur client** : `400 Bad Request`, `401 Unauthorized` (non authentifié), `403 Forbidden` (authentifié mais non autorisé), `404 Not Found`, `429 Too Many Requests`.
- **5xx — Erreur serveur** : `500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable`.

### 1.5 HTTP vs HTTPS

HTTPS ajoute une couche de chiffrement **TLS** (*Transport Layer Security*) au-dessus de HTTP. Le processus se déroule en plusieurs étapes :

1. Le client initie une connexion et demande le **certificat SSL/TLS** du serveur.
2. Le client vérifie ce certificat auprès d'une **autorité de certification** (CA).
3. Un échange de clés (*handshake*) établit une **clé de session** symétrique.
4. Toutes les données sont ensuite chiffrées avec cette clé.

HTTPS garantit trois propriétés : la **confidentialité** (les données ne peuvent être lues en transit), l'**intégrité** (elles ne peuvent être modifiées sans détection) et l'**authenticité** (le serveur est bien celui qu'il prétend être). Aujourd'hui, l'utilisation de HTTPS est considérée comme obligatoire, même pour des sites non sensibles.

### 1.6 Versions de HTTP

- **HTTP/1.1** : une connexion par requête (ou réutilisation avec `keep-alive`), encodage texte.
- **HTTP/2** : multiplexage (plusieurs requêtes sur une même connexion), compression des en-têtes, push serveur.
- **HTTP/3** : basé sur **QUIC** (UDP au lieu de TCP), réduction de la latence, meilleure résilience aux pertes de paquets.

---

## Module 2 — Consommation d'API en Ligne de Commande

### 2.1 Introduction à cURL

`curl` est l'outil de référence pour interagir avec des APIs depuis le terminal. Il supporte HTTP, HTTPS, FTP et de nombreux autres protocoles.

**Requête GET simple :**

```bash
curl https://jsonplaceholder.typicode.com/posts/1
```

**Avec en-têtes détaillés (option `-v` pour verbose) :**

```bash
curl -v https://jsonplaceholder.typicode.com/posts/1
```

**Requête POST avec un corps JSON :**

```bash
curl -X POST https://jsonplaceholder.typicode.com/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "Mon article", "body": "Contenu ici", "userId": 1}'
```

**Requête PUT :**

```bash
curl -X PUT https://jsonplaceholder.typicode.com/posts/1 \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "title": "Titre modifié", "body": "Nouveau contenu", "userId": 1}'
```

**Requête DELETE :**

```bash
curl -X DELETE https://jsonplaceholder.typicode.com/posts/1
```

### 2.2 Options cURL essentielles

| Option | Description | Exemple |
|--------|-------------|---------|
| `-X` | Spécifie la méthode HTTP | `-X POST` |
| `-H` | Ajoute un en-tête | `-H "Authorization: Bearer TOKEN"` |
| `-d` | Envoie des données (corps) | `-d '{"key":"value"}'` |
| `-o` | Sauvegarde la réponse dans un fichier | `-o response.json` |
| `-i` | Inclut les en-têtes de réponse | |
| `-s` | Mode silencieux (pas de barre de progression) | |
| `-L` | Suit les redirections | |
| `-w` | Format de sortie personnalisé | `-w "%{http_code}"` |

### 2.3 Traitement des réponses avec jq

`jq` est un processeur JSON en ligne de commande, indispensable pour filtrer et transformer les réponses d'API :

```bash
# Extraire un champ spécifique
curl -s https://jsonplaceholder.typicode.com/posts/1 | jq '.title'

# Filtrer une liste
curl -s https://jsonplaceholder.typicode.com/posts | jq '.[0:3] | .[].title'

# Construire un nouvel objet
curl -s https://jsonplaceholder.typicode.com/users/1 | jq '{nom: .name, email: .email}'
```

### 2.4 Autres outils CLI utiles

**HTTPie** offre une syntaxe plus lisible que curl :

```bash
# GET
http https://jsonplaceholder.typicode.com/posts/1

# POST avec JSON (syntaxe simplifiée)
http POST https://jsonplaceholder.typicode.com/posts title="Mon article" body="Contenu" userId:=1
```

**wget** est utile pour télécharger des fichiers ou des réponses volumineuses :

```bash
wget -O data.json https://api.example.com/export
```

---

## Module 3 — Consommation d'API avec Python

### 3.1 La bibliothèque requests

`requests` est la bibliothèque Python standard de facto pour les appels HTTP. Elle offre une API intuitive et gère automatiquement l'encodage, les cookies et les redirections.

```python
import requests

# GET
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
print(response.status_code)   # 200
print(response.json())         # dict Python

# POST
payload = {"title": "Nouveau post", "body": "Contenu", "userId": 1}
response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json=payload  # sérialise automatiquement en JSON + header Content-Type
)
print(response.status_code)   # 201
print(response.json()["id"])  # ID du post créé
```

### 3.2 Gestion des en-têtes et de l'authentification

```python
headers = {
    "Authorization": "Bearer mon_token_secret",
    "Accept": "application/json",
    "User-Agent": "MonApp/1.0"
}

response = requests.get("https://api.example.com/data", headers=headers)

# Authentification Basic
response = requests.get(
    "https://api.example.com/secure",
    auth=("username", "password")  # encodé automatiquement en Base64
)
```

### 3.3 Paramètres de requête et pagination

```python
# Paramètres de requête (query string)
params = {"page": 2, "per_page": 10, "sort": "created_at"}
response = requests.get("https://api.example.com/items", params=params)
# URL résultante : https://api.example.com/items?page=2&per_page=10&sort=created_at

# Pagination automatique
def fetch_all_items(base_url):
    items = []
    page = 1
    while True:
        response = requests.get(base_url, params={"page": page, "per_page": 100})
        data = response.json()
        if not data:
            break
        items.extend(data)
        page += 1
    return items
```

### 3.4 Gestion des erreurs et résilience

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Gestion basique des erreurs
try:
    response = requests.get("https://api.example.com/data", timeout=10)
    response.raise_for_status()  # lève une exception si status >= 400
    data = response.json()
except requests.exceptions.Timeout:
    print("La requête a expiré")
except requests.exceptions.HTTPError as e:
    print(f"Erreur HTTP : {e.response.status_code}")
except requests.exceptions.ConnectionError:
    print("Impossible de se connecter au serveur")
except requests.exceptions.JSONDecodeError:
    print("La réponse n'est pas du JSON valide")

# Retry automatique avec backoff exponentiel
session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))
response = session.get("https://api.example.com/data")
```

### 3.5 Sessions et performance

```python
# Une session réutilise la connexion TCP (keep-alive)
session = requests.Session()
session.headers.update({"Authorization": "Bearer mon_token"})

# Toutes les requêtes partagent les mêmes headers et la même connexion
r1 = session.get("https://api.example.com/users")
r2 = session.get("https://api.example.com/posts")
r3 = session.get("https://api.example.com/comments")
```

### 3.6 Manipulation avancée des données

```python
import requests
import json
from datetime import datetime

# Récupérer et transformer des données
response = requests.get("https://jsonplaceholder.typicode.com/users")
users = response.json()

# Filtrage et transformation
active_emails = [
    {"name": u["name"], "email": u["email"], "city": u["address"]["city"]}
    for u in users
    if u["address"]["city"] != "South Elvis"
]

# Export en fichier JSON formaté
with open("users_filtered.json", "w") as f:
    json.dump(active_emails, f, indent=2, ensure_ascii=False)
```

---

## Module 4 — Développement d'API avec http.server

### 4.1 Présentation

Le module `http.server` est intégré à Python. Il permet de créer un serveur HTTP simple sans aucune dépendance externe. C'est un excellent point de départ pour comprendre les mécanismes fondamentaux avant d'utiliser un framework.

### 4.2 Un serveur minimal

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/api/hello":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {"message": "Bonjour le monde !"}
            self.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not Found"}).encode("utf-8"))

if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), SimpleHandler)
    print("Serveur démarré sur http://localhost:8000")
    server.serve_forever()
```

### 4.3 Gestion des méthodes CRUD

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# Base de données en mémoire
ITEMS = {
    1: {"id": 1, "name": "Python", "category": "language"},
    2: {"id": 2, "name": "Flask",  "category": "framework"},
}
next_id = 3

class APIHandler(BaseHTTPRequestHandler):

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def _read_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        return json.loads(body) if body else {}

    def do_GET(self):
        if self.path == "/api/items":
            self._send_json(list(ITEMS.values()))
        elif self.path.startswith("/api/items/"):
            item_id = int(self.path.split("/")[-1])
            if item_id in ITEMS:
                self._send_json(ITEMS[item_id])
            else:
                self._send_json({"error": "Item not found"}, 404)
        else:
            self._send_json({"error": "Not Found"}, 404)

    def do_POST(self):
        global next_id
        if self.path == "/api/items":
            data = self._read_body()
            item = {"id": next_id, **data}
            ITEMS[next_id] = item
            next_id += 1
            self._send_json(item, 201)

    def do_PUT(self):
        if self.path.startswith("/api/items/"):
            item_id = int(self.path.split("/")[-1])
            if item_id in ITEMS:
                data = self._read_body()
                ITEMS[item_id] = {"id": item_id, **data}
                self._send_json(ITEMS[item_id])
            else:
                self._send_json({"error": "Item not found"}, 404)

    def do_DELETE(self):
        if self.path.startswith("/api/items/"):
            item_id = int(self.path.split("/")[-1])
            if item_id in ITEMS:
                del ITEMS[item_id]
                self._send_json({"message": "Deleted"}, 200)
            else:
                self._send_json({"error": "Item not found"}, 404)

if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000age, mais il présente des limites importantes : pas de routage avancé (il faut parser `self.path` manuellement), pas de middleware, pas de gestion native de CORS, un seul thread par défaut, et aucune validation automatique des données. C'est pourquoi on utilise des frameworks comme Flask en production.

---

## Module 5 — Développement d'API avec Flask

### 5.1 Introduction à Flask

Flask est un micro-framework Python léger et flexible. Il fournit le routage, la gestion des requêtes/réponses, un système de templates, et un écosystème d'extensions riche, tout en restant minimaliste.

```bash
pip install flask
```

### 5.2 Application minimale

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"message": "Bienvenue sur l'API"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

### 5.3 API CRUD complète

```python
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Base de données en mémoire
items = [
    {"id": 1, "name": "Python",  "category": "language",  "level": "beginner"},
    {"id": 2, "name": "Flask",   "category": "framework", "level": "intermediate"},
    {"id": 3, "name": "Docker",  "category": "tool",      "level": "intermediate"},
]
next_id = 4


# --- READ ---

@app.route("/api/items", methods=["GET"])
def get_items():
    # Filtrage par query string
    category = request.args.get("category")
    level = request.args.get("level")
    result = items
    if category:
        result = [i for i in result if i["category"] == category]
    if level:
        result = [i for i in result if i["level"] == level]
    return jsonify(result)


@app.route("/api/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = next((i for i in items if i["id"] == item_id), None)
    if item is None:
        abort(404)
    return jsonify(item)


# --- CREATE ---

@app.route("/api/items", methods=["POST"])
def create_item():
    global next_id
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    data = request.get_json()

    # Validation
    required = ["name", "category", "level"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    item = {
        "id": next_id,
        "name": data["name"],
        "category": data["category"],
        "level": data["level"],
    }
    items.append(item)
    next_id += 1
    return jsonify(item), 201


# --- UPDATE ---

@app.route("/api/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    item = next((i for i in items if i["id"] == item_id), None)
    if item is None:
        abort(404)

    data = request.get_json()
    item["name"]     = data.get("name",     item["name"])
    item["category"] = data.get("category", item["category"])
    item["level"]    = data.get("level",    item["level"])
    return jsonify(item)


# --- DELETE ---

@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    global items
    item = next((i for i in items if i["id"] == item_id), None)
    if item is None:
        abort(404)
    items = [i for i in items if i["id"] != item_id]
    return jsonify({"message": "Deleted"}), 200


# --- Gestion d'erreurs personnalisée ---

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"})_ == "__main__":
    app.run(debug=True, port=5000)
```

### 5.4 Blueprints : structurer une application

Les Blueprints permettent de découper l'application en modules réutilisables :

```
project/
├── app.py
├── routes/
│   ├── __init__.py
│   ├── items.py
│   └── users.py
└── models/
    └── __init__.py
```

```python
# routes/items.py
from flask import Blueprint, jsonify

items_bp = Blueprint("items", __name__, url_prefix="/api/items")

@items_bp.route("/", methods=["GET"])
def get_items():
    return jsonify([])

# app.py
from flask import Flask
from routes.items import items_bp

app = Flask(__name__)
app.register_blueprint(items_bp)
```

### 5.5 Middleware et hooks

Flask offre des points d'accroche pour exécuter du code avant ou après chaque requête :

```python
from flask import g
import time

@app.before_request
def before():
    g.start_time = time.time()

@app.after_request
def after(response):
    duration = time.time() - g.start_time
    response.headers["X-Response-Time"] = f"{duration:.4f}s"
    return response
```

### 5.6 CORS (Cross-Origin Resource Sharing)

Pour permettre à un frontend hébergé sur un domaine différent d'appeler votre API :

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["https://monsite.com"]}})
```

---

## Module 6 — Sécurité & Authentification des APIs

### 6.1 Pourquoi sécuriser une API ?

Une API exposée sans protection est vulnérable à de nombreuses attaques : accès non autorisé aux données, injection de données malveillantes, abus de ressources (DoS), et interception de données sensibles. La sécurité repose sur trois piliers : **authentification** (qui es-tu ?), **autorisation** (qu'as-tu le droit de faire ?) et **chiffrement** (les données sont-elles protégées en transit ?).

### 6.2 API Keys

Le mécanisme le plus simple : une clé unique identifie l'application appelante.

```python
from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)
VALID_API_KEYS = {"sk-abc123secret", "sk-def456secret"}

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")
        if api_key not in VALID_API_KEYS:
            return jsonify({"error": "Invalid or missing API key"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route("/api/data")
@require_api_key
def get_data():
    return jsonify({"data": "Contenu protégé"})
```

Les API keys identifient l'**application** mais pas l'**utilisateur**. Elles ne doivent jamais être exposées côté client (frontend).

### 6.3 Authentification par Token — JWT

Les **JSON Web Tokens** sont le standard moderne pour l'authentification stateless. Un JWT se compose de trois parties encodées en Base64 et séparées par des points : le **header** (algorithme), le **payload** (claims/données) et la **signature**.

```python
import jwt
from datetime import datetime, timedelta, timezone
from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-to-a-random-secret"

# --- Génération du token ---

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    # En production : vérifier en base de données avec hash du mot de passe
    if data.get("username") == "admin" and data.get("password") == "secret":
        token = jwt.encode(
            {
                "sub": data["username"],
              datetime.now(timezone.utc) + timedelta(hours=1),
            },
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401


# --- Vérification du token ---

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing token"}), 401
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            request.user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated


# --- Autorisation par rôle ---

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if request.user.get("role") != role:
                return jsonify({"error": "Insufficient permissions"}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator


@app.route("/api/admin")
@token_required
@role_required("admin")
def admin_panel():
    return jsonify({"message": f"Bienvenue {request.user['sub']}"})
```

### 6.4 OAuth 2.0 — Principes

OAuth 2.0 permet à un utilisateur d'accorder à une application tierce un accès limité à ses ressources sans partager ses identifiants. Le flux le plus courant (*Authorization Code*) se déroule ainsi :

1. L'application redirige l'utilisateur vers le **serveur d'autorisation** (Google, GitHub...).
2. L'utilisateur s'authentifie et consent à partager certaines données (scopes).
3. Le serveur d'autorisation redirige l'utilisateur vers l'application avec un **code d'autorisation**.
4. L'application échange ce code contre un **access token** (et optionnellement un **refresh token**).
5. L'application utilise l'access token pour accéder aux ressources protégées.

### 6.5 Rate Limiting

Limiter le nombre de requêtes protège contre les abus et le déni de service :

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per hour"],
    storage_uri="memory://",
)

@app.route("/api/data")
@limiter.limit("10 per minute")
def get_data():
    return jsonify({"data": "Protégé contre l'abus"})
```

### 6.6 Bonnes pratiques de sécurité

- **Toujours utiliser HTTPS** en production.
- **Ne jamais stocker les mots de passe en clair** : utiliser `bcrypt` ou `argon2`.
- **Valider et assainir toutes les entrées** pour prévenir les injections (SQL, XSS).
- **Utiliser des tokens à durée de vie courte** avec des refresh tokens pour le renouvellement.
- **Appliquer le principe du moindre privilège** : chaque token ne doit donner accès qu'au strict nécessaire.
- **Ajouter des en-têtes de sécurité** : `X-Content-Type-Options`, `X-Frame-Options`, `Strict-Transport-Security`.
- **Logger les accès** et mettre en place des alertes sur les comportements anormaux.

---

## Module 7 — Standards & Documentation avec OpenAPI

### 7.1 Qu'est-ce qu'OpenAPI ?

OpenAPI (anciennement Swagger) est une spécification standardisée pour décrire les APIs REST de façon lisible par les humains et interprétable par les machines. Un fichier OpenAPs méthodes, les paramètres, les schémas de données et les règles d'authentification.

### 7.2 Structure d'un document OpenAPI

```yaml
openapi: 3.0.3
info:
  title: Items API
  description: API de gestion d'items techniques
  version: 1.0.0
  contact:
    name: Équipe API
    email: api@example.com

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: http://localhost:5000
    description: Développement local

paths:
  /items:
    get:
      summary: Liste tous les items
      operationId: getItems
      tags:
        - Items
      parameters:
        - name: category
          in: query
          required: false
          schema:
            type: string
            enum: [language, framework, tool]
          description: Filtrer par catégorie
        - name: page
          in: query
          schema:
            type: integer
            default: 1
      responses:
        "200":
          description: Liste des items
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: "#/components/schemas/Item"
        "401":
          $ref: "#/components/responses/Unauthorized"

    post:
      summary: Crée un nouvel item
      operationId: createItem
      tags:
        - Items
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ItemCreate"
      responses:
        "201":
          description: Item créé
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Item"
        "400":
          description: Données invalides

  /items/{itemId}:
    get:
      summary: Récupère un item par ID
      operationId: getItem
      tags:
        - Items
      parameters:
        - name: itemId
          in: path
          required: true
          schema:
            type: integer
      responses:
        "200":
          description: Détails de l'item
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Item"
        "404":
          description: Item non trouvé

components:
  schemas:
    Item:
      type: object
      properties:
        id:
          type: integer
          readOnly: true
        name:
          type: string
          example: Flask
        category:
          type: string
          enum: [language, framework, tool]
        level:
          type: string
          enum: [beginner, intermediate, advanced]
      required:
        - id
        - name
        - category
        - level

    ItemCreate:
      type: object
      properties:
        name:
          type: string
        category:
          type: string
          enum: [language, framework, tool]
        level:
          type: string
          enum: [beginner, intermediate, advanced]
      required:
        - name
        - category
        - level

  responses:
    Unauthorized:
      description: Authentification requise
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
                example: Missing or invalid token

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
    apiKey:
      type: apiKey
      in: header
      name: X-API-Key
```

### 7.3 Intégration avec Flask (flask-smorest)

`flask-smorest` génère automentation OpenAPI depuis le code :

```python
from flask import Flask
from flask_smorest import Api, Blueprint, abort
from marshmallow import Schema, fields

app = Flask(__name__)
app.config["API_TITLE"] = "Items API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

# Schémas Marshmallow (validation + sérialisation)
class ItemSchema(Schema):
    id       = fields.Int(dump_only=True)
    name     = fields.Str(required=True)
    category = fields.Str(required=True)
    level    = fields.Str(required=True)

blp = Blueprint("items", __name__, url_prefix="/api/items", description="Gestion des items")

@blp.route("/")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        """Liste tous les items"""
        return items

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, new_item):
        """Crée un nouvel item"""
        new_item["id"] = len(items) + 1
        items.append(new_item)
        return new_item

api.register_blueprint(blp)
```

Une fois lancée, l'interface Swagger UI interactive est accessible sur `/docs`.

### 7.4 Outils de l'écosystème OpenAPI

- **Swagger UI** : interface web interactive pour tester les endpoints depuis le navigateur.
- **Swagger Editor** : éditeur en ligne avec validation en temps réel du document OpenAPI.
- **OpenAPI Generator** : génère automatiquement des clients SDK (Python, JS, Java...) et des stubs serveur à partir d'un fichier OpenAPI.
- **Redoc** : alternative à Swagger UI pour une documentation plus lisible et publiable.
- **Postman** : peut importer un fichier OpenAPI pour générer automatiquement une collection de tests.

### 7.5 Bonnes pratiques de documentation

- **Documenter tous les endpoints**, y compris les cas d'erreur.
- **Fournir des exemples réalistes** dans les schémas (`example` dans les propriétés).
- **Utiliser les tags** pour regrouper les endpoints par domaine fonctionnel.
- **Versionner l'API** (dans l'URL `/v1/` ou via un en-tête) et documenter les changements.
- **Décrire les codes d'erreur** et le format des messages d'erreur.
- **Maintenir la documentation synchronisée** avec le code (génération automatique recommandée).

---

## Récapitulatif

| Module | Ce que vous savez faire |
|--------|------------------------|
| 1. HTTP/HTTPS | Comprendre requêtes/réponses, méthodes, codes de statut, TLS |
| 2. CLI | Utiliser curl, jq, HTTPie pour interagir avec des APIs |
| 3. Python requests | Consommer des APIs, gérer erreurs, pagination, sessions |
| 4. http.server | Créer un serveur HTTP basique avec routage manuel |
| 5. Flask | Développer une API REST complète avec validation et blueprints |
| 6. Sécurité | Implémenter API keys, JWT, OAuth 2.0, rate limiting |
| 7. OpenAPI | Documenter et standardiser vos APIs avec Swagger/OpenAPI |

---

*Cours structuré couvrant les 7 objectifs d'apprentissage — De HTTP aux APIs documentées et sécurisées.*
