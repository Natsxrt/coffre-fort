# Plan — Coffre-fort numérique Zero-Trust

> Objectif : seul l'utilisateur peut chiffrer/déchiffrer. Les serveurs ne connaissent jamais la clé et ne stockent que des données chiffrées et un hash d'authentification.

## 1. Stack

| Couche | Choix | Pourquoi |
|---|---|---|
| Client | HTML + JS vanilla | Pas de build |
| Crypto client | libsodium.js (`libsodium-wrappers-sumo`, vendoré) | Une seule lib pour Argon2id + XChaCha20-Poly1305 (WASM, rapide) |
| KDF | Argon2id (m=64 MiB, t=3, p=1) | Memory-hard, résistant au GPU |
| Séparation des clés | HKDF-SHA256 (WebCrypto) | Deux clés indépendantes, à sens unique |
| Chiffrement | XChaCha20-Poly1305 | Chiffrement authentifié, rapide en logiciel ; nonce de 24 o tirable au hasard sans risque de collision |
| Hash serveur | Argon2id (`argon2-cffi`) | Standard pour stocker un secret d'auth |
| Jeton | JWT EdDSA (Ed25519) (`PyJWT`) | L'auth signe, le vault vérifie sans pouvoir forger |
| Services | 2 × FastAPI | Léger |
| BDD | 2 × SQLite | Un vol = une seule moitié des infos |
| Entrée | nginx (proxy + statiques) | Une origine, pas de CORS |
| Run | docker-compose (3 conteneurs) | Une commande |

## 2. Schéma crypto

```
mot de passe + kdf_salt
   │ Argon2id
   ▼
masterKey ──HKDF "enc"──► KEK
          └─HKDF "auth"─► authKey ──► auth-service ──Argon2id──► auth_hash

vaultKey        = 32 o aléatoires
wrappedVaultKey = XChaCha20-Poly1305(KEK, vaultKey)      → auth.db
entrée          = XChaCha20-Poly1305(vaultKey, données)  → vault.db
```

- Le hash stocké (`auth_hash`) vient de la branche `auth`, la clé de chiffrement de la branche `enc` : ils sont différents et l'un ne permet pas de retrouver l'autre.
- La vaultKey permet de changer de mot de passe sans re-chiffrer le coffre (on ré-enveloppe 32 o).

## 3. Architecture

```
navigateur ──HTTPS──► nginx ──/auth/*──► auth-service  (clé privée, auth.db)
                            └─/vault/*─► vault-service (clé publique, vault.db)
```

Les deux services ne se parlent pas. Le `sub` du JWT (UUID) est le seul lien entre les bases.

## 4. Données

**auth.db** — `id (UUID)`, `email`, `kdf_salt`, `kdf_params`, `auth_hash`, `wrapped_vault_key`, `wrap_nonce`, `created_at`

**vault.db** — `id`, `owner_id`, `type (text|file)`, `enc_meta`, `meta_nonce`, `enc_data (BLOB)`, `data_nonce`, `size`, `created_at`, `updated_at`

Titres et noms de fichiers sont dans `enc_meta` (chiffrés).

## 5. API

| Service | Route | Rôle |
|---|---|---|
| auth | `POST /auth/prelogin` | email → sel + params |
| auth | `POST /auth/register` | email, sel, params, authKey, wrappedVaultKey |
| auth | `POST /auth/login` | authKey → JWT + wrappedVaultKey |
| auth | `POST /auth/change-password` | ancienne/nouvelle authKey, nouveau sel, nouvelle wrappedVaultKey |
| vault | `GET/POST /vault/items` | Liste / création |
| vault | `GET/PUT/DELETE /vault/items/{id}` | Si `owner_id == sub` |

## 6. Flux

- **Inscription** : génère sel + vaultKey → dérive KEK + authKey → enveloppe vaultKey → `/register`.
- **Connexion** : `/prelogin` → dérive KEK + authKey → `/login` → JWT + wrappedVaultKey → déballe vaultKey en mémoire.
- **Entrée** : chiffre (nonce aléatoire) → `/vault/items` avec `Bearer <JWT>`.
- **Changement de mdp** : nouvelle KEK → ré-enveloppe vaultKey → `/change-password`. Coffre inchangé.

## 7. Étapes

1. Squelette : docker-compose, nginx, script clés Ed25519, schémas SQLite.
2. `crypto.js` : Argon2id, HKDF, wrap/unwrap, encrypt/decrypt (libsodium).
3. auth-service : prelogin, register, login, JWT.
4. vault-service : vérif JWT, CRUD filtré par `owner_id`.
5. Front auth (clés en mémoire, jamais localStorage).
6. Entrées texte.
7. Fichiers (fichier entier, limite 20 Mo).
8. Changement de mot de passe.
9. Durcissement : CSP, `textContent`, rate limit login.
10. Doc technos/algos + vérif : rien en clair dans les `.db`.

## 8. Arborescence

```
coffre-fort/
├── docker-compose.yml
├── nginx/nginx.conf
├── scripts/gen-keys.sh
├── auth-service/   (main.py, db.py, Dockerfile, requirements.txt)
├── vault-service/  (main.py, security.py, db.py, Dockerfile, requirements.txt)
├── frontend/       (index.html, app.js, api.js, crypto.js, vendor/libsodium)
├── data/           (auth.db, vault.db)
└── docs/technos-algos.md
```
