# Fondamentaux de la Cryptographie Moderne

## Glossaire des acronymes essentiels

* **AD :** *Associated Data* — Données authentifiées mais laissées en clair (métadonnées liées au message en entrée d'un mode AEAD).
* **AEAD :** *Authenticated Encryption with Associated Data* — Chiffrement symétrique fournissant confidentialité, intégrité et authenticité (incluant des données associées).
* **AES :** *Advanced Encryption Standard* — Standard de chiffrement symétrique par blocs (clés de 128, 192 ou 256 bits, blocs de 128 bits / 16 octets).
* **CBC :** *Cipher Block Chaining* — Mode opératoire de chiffrement par blocs nécessitant un IV imprévisible et un padding (ex. PKCS#7) ; à éviter au profit de l'AEAD.
* **CFB / OFB :** *Cipher Feedback / Output Feedback* — Modes opératoires transformant un chiffrement par blocs en chiffrement par flot (nécessitent un IV imprévisible).
* **CMAC :** *Cipher-based Message Authentication Code* — Code d'authentification de message basé sur un chiffrement par blocs (ex. AES-CMAC).
* **CSPRNG :** *Cryptographically Secure Pseudo-Random Number Generator* — Générateur pseudo-aléatoire cryptographiquement sûr (clés, sels, IV).
* **CTR :** *Counter* — Mode opératoire par compteur transformant un chiffrement par blocs en chiffrement par flot (nécessite un nonce unique par clé, sans padding).
* **DEK :** *Data Encryption Key* — Clé symétrique aléatoire chiffrant directement les données applicatives (fichiers, lignes, champs).
* **DSA :** *Digital Signature Algorithm* — Ancien algorithme de signature basé sur le logarithme discret modulaire (obsolète).
* **ECC :** *Elliptic Curve Cryptography* — Cryptographie basée sur les courbes elliptiques (clés plus courtes à sécurité équivalente).
* **ECDH / ECDHE :** *Elliptic Curve Diffie-Hellman (Ephemeral)* — Échange de clés sur courbe elliptique (avec clés éphémères pour la *Forward Secrecy*).
* **ECDSA :** *Elliptic Curve Digital Signature Algorithm* — Algorithme de signature numérique sur courbe elliptique (ex. sur P-256).
* **ECB :** *Electronic Codebook* — Mode par blocs sans IV ni nonce (déterministe, non sécurisé, interdit en production).
* **EdDSA :** *Edwards-curve Digital Signature Algorithm* — Algorithme de signature sur courbes d'Edwards (ex. **Ed25519**).
* **GCM :** *Galois/Counter Mode* — Mode AEAD combinant le mode CTR et l'authentification Galois (ex. **AES-GCM**, sans padding).
* **GMAC :** *Galois Message Authentication Code* — Variante d'authentification de message issue de GCM.
* **HKDF :** *HMAC-based Extract-and-Expand Key Derivation Function* — Fonction de dérivation de clé (RFC 5869) à partir d'un secret haute entropie (ex. sortie ECDH).
* **HMAC :** *Hash-based Message Authentication Code* — Code d'authentification de message construit avec une fonction de hachage (ex. **HMAC-SHA256**).
* **HSM :** *Hardware Security Module* — Matériel dédié sécurisant la génération, le stockage et l'usage de clés cryptographiques.
* **IKM :** *Input Keying Material* — Secret brut d'entrée fourni à une fonction de dérivation de clé comme HKDF.
* **IV :** *Initialization Vector* — Vecteur d'initialisation (doit être imprévisible dans des modes comme CBC).
* **KDF :** *Key Derivation Function* — Fonction dérivant une ou plusieurs clés cryptographiques à partir d'un secret (mot de passe ou IKM).
* **KEK :** *Key Encryption Key* — Clé servant à chiffrer (*wrapper*) d'autres clés (comme les DEK) dans l'*Envelope Encryption*.
* **KMS :** *Key Management Service* — Service centralisé de gestion et de rotation des clés cryptographiques.
* **MAC :** *Message Authentication Code* — Tag cryptographique vérifiant l'intégrité et l'authenticité d'un message avec une clé partagée.
* **OAEP :** *Optimal Asymmetric Encryption Padding* — Schéma de bourrage probabiliste sécurisé utilisé avec le chiffrement RSA (**RSA-OAEP**).
* **PBKDF2 :** *Password-Based Key Derivation Function 2* — Fonction de dérivation de clé à partir d'un mot de passe (plus ancienne, moins résistante aux GPU qu'Argon2id).
* **PEM / PKCS#8 :** *Privacy-Enhanced Mail / Public-Key Cryptography Standards #8* — Formats d'encodage/structuration de clés et certificats (ex. `-----BEGIN ...-----`).
* **PKCS#7 :** *Public-Key Cryptography Standards #7* — Standard de padding (bourrage) utilisé pour aligner des données sur une taille de bloc fixe (ex. AES-CBC).
* **PRF :** *Pseudorandom Function* — Fonction déterministe à clé dont la sortie est indiscernable d'un aléa uniforme sans la clé (ex. **HMAC**, utilisée dans **HKDF** et **PBKDF2**).
* **PRP :** *Pseudorandom Permutation* — Permutation pseudo-aléatoire réversible à clé (modèle théorique d'un chiffrement par bloc comme **AES**).
* **PSS :** *Probabilistic Signature Scheme* — Schéma de signature probabiliste sécurisé recommandé avec RSA (**RSA-PSS**).
* **RSA :** *Rivest, Shamir & Adleman* — Algorithme asymétrique historique basé sur la factorisation de grands entiers.
* **SHA :** *Secure Hash Algorithm* — Famille de fonctions de hachage cryptographique (**SHA-1** cassé ; **SHA-2** comme SHA-256/SHA-512 ; **SHA-3**).
* **SIV :** *Synthetic Initialization Vector* — Mode résistant à la réutilisation accidentelle du nonce (*Nonce-Misuse Resistant*, ex. **AES-GCM-SIV**).

---

## 1. Les objectifs de sécurité (La triade)

Toute brique cryptographique répond à un ou plusieurs des besoins suivants :

* **Confidentialité :** Seuls les destinataires autorisés peuvent lire la donnée.
* **Intégrité :** La donnée n'a pas été modifiée ou altérée en transit ou au repos.
* **Authenticité :** La donnée provient bien de l'émetteur prétendu.

> **Règle d'or :** Chiffrer ne prouve pas l'origine. Signer ne cache rien.

---

## 2. Hachage & Dérivation de clés

### A. Fonctions de hachage cryptographique (Rapides)

Transforme une donnée de taille arbitraire en une empreinte (*digest*) de taille fixe. Fonction à sens unique (irréversible) et résistante aux collisions.

* **Usage :** Vérification d'intégrité de fichiers, signatures numériques, structures de données. **Jamais pour les mots de passe.**
* **Obsolètes (cassés) :** MD5, SHA-1.
* **Standards actuels :** **SHA-2** (SHA-256, SHA-512), **SHA-3**, **BLAKE2 / BLAKE3**.

### B. Hachage de mots de passe, KDF & PRF

Un mot de passe humain a une faible entropie. Pour contrer les attaques par force brute (GPU/ASIC) et les *Rainbow Tables*, on utilise un **Sel** (valeur aléatoire publique unique par utilisateur) et des fonctions coûteuses en calcul/mémoire.

* **Stockage / vérification de mots de passe :** **Argon2id** (standard recommandé), **bcrypt** (historique, limité en mémoire et tronquant les entrées à 72 octets).
* **KDF (Key Derivation Function) :** Fonction **déterministe** (pour un même secret et un même sel, elle produit toujours la même clé, permettant de retrouver la clé plus tard).
  * *Depuis un mot de passe :* **Argon2id**, **scrypt**, **PBKDF2**.
  * *Depuis un secret brut haute entropie (IKM, ex. ECDH) :* **HKDF** (RFC 5869).
* **PRF (*Pseudorandom Function*) :** Fonction déterministe à clé produisant une sortie pseudo-aléatoire indiscernable d'un vrai hasard sans la clé. En pratique, **HMAC** (ex. `HMAC-SHA256`) joue le rôle de PRF au cœur de constructions comme **HKDF** et **PBKDF2** (à distinguer d'une **PRP**, *Pseudorandom Permutation*, qui est réversible et modélise un chiffrement par bloc comme **AES**).

---

## 3. Chiffrement Symétrique, AEAD & Padding

La **même clé secrète** sert à chiffrer et à déchiffrer. C'est la méthode la plus rapide pour les volumes de données.

### A. Algorithmes et modes de référence

* **AES-GCM :** Standard mondial AEAD, très rapide avec accélération matérielle (AES-NI).
* **ChaCha20-Poly1305 :** Alternative AEAD très performante en logiciel (mobile, systèmes sans accélération AES) et résistante aux *timing attacks*.
* **AES-GCM-SIV :** Mode AEAD conçu pour résister à une réutilisation accidentelle du nonce.

### B. AEAD : Associated Data (AD) vs Tag d'authentification

Il est essentiel de ne pas confondre ces deux éléments dans un chiffrement **AEAD** :

```text
Entrées :  [Clé] + [Nonce/IV] + [Donnée en clair] + [Associated Data (AD, optionnel)]
                                      │
                              (Chiffrement AEAD)
                                      ▼
Sorties :  [Donnée chiffrée (Ciphertext)] + [Tag d'authentification (ex. 16 octets)]
```

* **Associated Data (`additionalData` / AD) — Entrée :** Ce sont des métadonnées **en clair** que l'on fournit au chiffrement (ex. `userId`, identifiant de ligne en base de données, version de clé). Elles ne sont **pas chiffrées**, mais elles sont **authentifiées** : au déchiffrement, il faut fournir exactement les mêmes AD, sinon l'opération échoue (ce qui empêche de déplacer un champ chiffré d'une ligne ou d'un utilisateur à un autre).
* **Tag d'authentification (GCM Tag / Poly1305 Tag) — Sortie :** C'est une empreinte cryptographique générée automatiquement par l'algorithme (généralement 16 octets / 128 bits) qui scelle à la fois le *ciphertext* **et** les *Associated Data*. En WebCrypto (`crypto.subtle.encrypt`), ce tag est automatiquement concaténé à la fin du buffer chiffré retourné.

### C. IV, Nonce et Sel : Ne plus les confondre

Tous ces paramètres sont **publics** (non secrets) et servent à éviter que deux opérations identiques produisent un résultat identique.

| Concept | Contrainte principale | Génération | Contexte / Algorithmes |
| :--- | :--- | :--- | :--- |
| **IV** *(Initialization Vector)* | **Imprévisibilité** | Aléatoire strict (CSPRNG). Un compteur ouvre des failles critiques. | Modes anciens : **CBC**, CFB, OFB. |
| **Nonce** *(Number used once)* | **Unicité** (pour une clé donnée) | Compteur ou aléatoire (attention aux collisions en aléatoire). | Modes modernes : **GCM**, **CTR**, **ChaCha20**. *(Note : **ECB** n'utilise ni IV ni Nonce et est interdit).* |
| **Sel** *(Salt)* | **Unicité** (par utilisateur/entrée) | Aléatoire (CSPRNG). | Hachage de mots de passe, **PBKDF**. |

> **⚠️ DANGER CRITIQUE :** Réutiliser un même **Nonce** avec la même **Clé** en mode CTR, AES-GCM ou ChaCha20-Poly1305 compromet gravement la confidentialité et l'authenticité. En revanche, **Ed25519** gère son nonce interne de manière déterministe et sûre (à l'inverse d'ECDSA, où un nonce répété expose la clé privée).

### D. Le Padding (Bourrage)

Le **padding** consiste à ajouter des octets supplémentaires à une donnée pour qu'elle respecte une taille de bloc fixe ou une structure imposée par un algorithme :

* **Chiffrement par blocs (ex. AES-CBC) :** AES opère sur des blocs fixes de **16 octets (128 bits)**. Si un message fait 20 octets, on complète le second bloc jusqu'à 32 octets avec un schéma comme **PKCS#7**, puis le déchiffrement retire ces octets.
  * *Risque (*Padding Oracle*) :* En mode **CBC**, si le système révèle (par une erreur ou un temps de réponse) que le padding est invalide sans vérification d'intégrité préalable, un attaquant peut déchiffrer les données bloc par bloc.
  * *Modes modernes (AEAD / flux) :* **AES-GCM**, **CTR** et **ChaCha20-Poly1305** n'ont **pas besoin de padding** pour ajuster la longueur d'un message de taille arbitraire.
* **Cryptographie asymétrique (RSA) :** Avec **RSA**, le padding est une **condition de sécurité indispensable** (sans lui, le *textbook RSA* est déterministe et vulnérable) :
  * **Chiffrement :** **RSA-OAEP** (remplace l'ancien PKCS#1 v1.5).
  * **Signature :** **RSA-PSS** (remplace l'ancien PKCS#1 v1.5).

---

## 4. Intégrité sans chiffrement : MAC & HMAC

Lorsque la confidentialité n'est pas requise mais qu'il faut vérifier l'intégrité/authenticité via une clé partagée :

* **MAC :** Prend `(Clé secrète + Message)` et produit un *tag*.
* **HMAC :** MAC basé sur une fonction de hachage (ex. **HMAC-SHA256**), servant également de **PRF** dans de nombreux protocoles.
* **Autres familles :** CMAC, GMAC, Poly1305.

---

## 5. Cryptographie Asymétrique (Clé Publique / Clé Privée)

### A. Courbes Elliptiques (ECC) vs RSA

**RSA** est progressivement remplacé par l'**ECC**, qui offre une sécurité équivalente avec des clés plus courtes (ex. **ECC 256 bits** $\approx$ **RSA 3072 bits**), réduisant la bande passante et le coût de calcul.

* **P-256** *(secp256r1)* : Courbe NIST très répandue (TLS, WebCrypto, certificats, HSM). Elle désigne **la courbe** et peut être utilisée avec **ECDSA** (signature) ou **ECDH** (échange de clés).
* **X25519 :** Courbe/mécanisme dédié à l'échange de clés (**ECDH**).
* **Ed25519 :** Courbe/mécanisme dédié aux signatures (**EdDSA**).

### B. Chiffrement vs Signature

| Critère | Chiffrement Asymétrique | Signature Numérique |
| :--- | :--- | :--- |
| **Objectif** | Confidentialité | Authenticité, Intégrité, Non-répudiation |
| **Action de l'émetteur** | Chiffre avec la **clé publique** du destinataire | Signe avec sa **clé privée** |
| **Action du récepteur** | Déchiffre avec sa **clé privée** | Vérifie avec la **clé publique** de l'émetteur |
| **Algorithmes modernes** | Hybride : **X25519 + HKDF + AEAD** (ou **RSA-OAEP**) | **Ed25519**, ECDSA (P-256), **RSA-PSS** |

### C. Échange de clés ECDH & ECDHE

1. Alice et Bob génèrent chacun une paire de clés (privée/publique) et échangent leurs clés publiques.
2. Chaque partie combine `Sa clé privée` + `Clé publique de l'autre` pour obtenir le même secret brut (*IKM*).
3. **HKDF** dérive de ce secret une clé symétrique solide pour **AES-GCM** ou **ChaCha20-Poly1305**.
4. Avec **ECDHE** (*Ephemeral*), de nouvelles clés sont générées par session, offrant la **Forward Secrecy** (les sessions passées restent protégées même si une clé à long terme est compromise plus tard).

---

## 6. Tableau d'association des algorithmes et briques

| Famille / Rôle | Algorithme / Standard | Courbe / Mode / Hash / Padding | Usage typique | Remarque / Vigilance |
| :--- | :--- | :--- | :--- | :--- |
| **Chiffrement symétrique (AEAD)** | **AES-GCM** | Clé 128/256 bits + **Nonce** unique + **AD** $\rightarrow$ Ciphertext + **Tag** (sans padding) | Chiffrement rapide de données/flux | Ne jamais réutiliser `(Clé, Nonce)` |
| **Chiffrement symétrique (AEAD)** | **ChaCha20-Poly1305** | Clé 256 bits + **Nonce** unique + **AD** $\rightarrow$ Ciphertext + **Tag** (sans padding) | Mobile, transport réseau, chiffrement logiciel | Très rapide sans accélération AES |
| **Chiffrement symétrique (AEAD)** | **AES-GCM-SIV** | Clé 128/256 bits + **Nonce** + **AD** $\rightarrow$ Ciphertext + **Tag** (sans padding) | Contextes à risque de réutilisation de nonce | Résistant au *nonce reuse* accidentel |
| **Chiffrement symétrique (legacy)** | **AES-CBC** / CTR / CFB / OFB | **IV** imprévisible + **Padding PKCS#7** (CBC) ou **Nonce** sans padding (CTR) | Compatibilité legacy uniquement | Préférer l'AEAD ; risque *padding oracle* en CBC ; **ECB** banni |
| **Échange de clés** | **ECDH / ECDHE** | **X25519** ou **P-256** $\rightarrow$ **HKDF** $\rightarrow$ AEAD | Établissement de secret partagé (TLS, messagerie) | **ECDHE** apporte la *Forward Secrecy* |
| **Signature numérique** | **Ed25519** (EdDSA) | Courbe Curve25519 (hash interne) | Signatures modernes, SSH, paquets, jetons | Nonce déterministe sûr |
| **Signature numérique** | **ECDSA** | **P-256** (ou P-384, secp256k1) + **SHA-256** | Certificats TLS, WebCrypto, signatures | Exige un aléa unique par signature |
| **Signature / Chiffrement asymétrique** | **RSA** | **RSA-PSS** (padding signature) / **RSA-OAEP** (padding chiffrement) | Compatibilité existante (2048–4096 bits) | Padding obligatoire pour la sécurité ; limité en taille ; plus lent que ECC |
| **Signature historique** | **DSA** | Paramètres DSA + SHA | Héritage / comparaison historique | Obsolète ; à éviter |
| **Intégrité / MAC** | **HMAC** | **HMAC-SHA256** (ou SHA-512) + clé secrète | Authentification de messages/requêtes/jetons | Ne chiffre pas le contenu |
| **Brique / Dérivation** | **PRF** (*Pseudorandom Function*) | **HMAC-SHA256** (utilisé dans **HKDF** / **PBKDF2**) | Dérivation de clés, MAC, protocoles (TLS) | Sortie pseudo-aléatoire sans la clé ; non inversible (contrairement à une **PRP**/AES) |
| **Hachage rapide** | **SHA-2 / SHA-3 / BLAKE2** | SHA-256, SHA-512, BLAKE2b/s | Intégrité de fichiers, empreintes | **MD5** et **SHA-1** cassés ; pas pour mdp |
| **Mots de passe & KDF** | **Argon2id** / scrypt / PBKDF2 | **Sel** aléatoire + paramètres coût CPU/RAM | Stockage mdp (Argon2id) et dérivation **KEK** | **HKDF** sert pour secret brut (IKM) |

---

## 7. Architectures Pratiques (Mise en application)

### Cas 1 : Échange de fichier sécurisé (Chiffrement hybride + Signature)

```text
Échange de fichier :
  ECC (X25519) ──► HKDF (SHA-256) ──► clé AES-GCM + nonce ──► fichier chiffré + tag
  Ed25519 (signature) pour l'authenticité (sur le hash du fichier / paquet)
```

* **Point d'attention :** Le *Sign-then-encrypt* (signer puis chiffrer) permet de protéger la signature par le chiffrement. L'authentification d'origine reste assurée par la signature asymétrique (utile pour la non-répudiation ou la vérification par un tiers).

### Cas 2 : Données en base de données (Envelope Encryption)

```text
[Mot de passe] ──(KDF (Argon2id/PBKDF2 + sel))──► [KEK]
                                       │
                                 (chiffre/wrap)
                                       ▼
[DEK aléatoire] ─────────────────► [DEK chiffrée] (stockée en BDD à côté de la donnée)
       │
  (AES-GCM + Nonce unique + AD)
       ▼
[Donnée en clair] ───────────────► [Donnée chiffrée + Tag]
```

* **Cycle de vie KEK / DEK :** La **DEK** est générée aléatoirement (CSPRNG) pour chiffrer les données ; si elle est perdue ou changée sans re-chiffrement, les données deviennent illisibles. Lors d'un **changement de mot de passe**, on déchiffre la DEK avec l'ancienne **KEK**, on dérive une nouvelle **KEK** (nouveau sel), et on **re-wrappe la même DEK** avec un nouvel IV/nonce — sans avoir à re-chiffrer toutes les données.
* **Point d'attention :** Chaque chiffrement avec une **DEK** utilise un **nonce** unique ; la **DEK wrappée** et le **nonce** sont stockés avec la donnée (et l'ID d'enregistrement ou d'utilisateur peut être passé en **AD** pour empêcher le déplacement d'un champ entre lignes ou comptes).

## 8. Résumé Mémo

* **SHA (SHA-2 / SHA-3)** est toujours utilisé pour le hachage rapide sans clé, **SAUF** pour les mots de passe (préférence à **Argon2id**, **scrypt** ou **bcrypt** ; **SHA-1** est banni).
* **RSA** est toujours utilisé, mais la préférence va aujourd'hui à l'**ECC** (courbes elliptiques).
* **AES** est toujours utilisé (en mode **GCM**), avec pour principal concurrent moderne **ChaCha20-Poly1305**.
* **RSA** ou **ECC** permettent de créer des paires de clés asymétriques (clé publique / clé privée).
* **AES** et **ChaCha20** chiffrent avec une **clé symétrique** (générée via des octets aléatoires CSPRNG ou dérivée par un **KDF**).
* On peut **signer** avec **RSA** et **ECC** (on signe avec la **clé privée**, on valide avec la **clé publique**).
* On peut **chiffrer directement** avec **RSA** (clé publique, petites données uniquement), mais **pas directement avec l'ECC**.
* L'**ECC** sert à la **signature** (EdDSA / ECDSA) et à l'**accord de clé** (**ECDH**), puis on chiffre les données avec **AES-GCM** ou **ChaCha20-Poly1305**.
* **Chiffrement hybride (gros volumes et échanges) :** asymétrique pour établir/protéger la clé, symétrique pour chiffrer les données (**ECDHE** si échange interactif, type TLS).
* **MAC (HMAC, Poly1305) :** vérifie que le contenu n'a pas été altéré (intégrité) et qu'il provient de quelqu'un qui connaît le secret (authenticité), mais **ne chiffre rien**.

### KDF (Key Derivation Function)

* Fonction qui dérive une ou plusieurs clés à partir d'un secret de départ
* Entrées : le secret, un sel (aléatoire, non secret, stocké avec le résultat), des paramètres (coût, mémoire) et éventuellement un contexte (info)
* Sortie : des octets utilisables comme clé (même secret et mêmes paramètres : même clé ; sel différent : clé différente)
* Deux familles selon la qualité du secret :
    * Secret faible (mot de passe, passphrase) : **KDF** lent et gourmand en mémoire pour freiner le brute force hors ligne : **Argon2id** (recommandé), **scrypt**, **bcrypt**, **PBKDF2** (si contrainte FIPS)
    * Secret déjà fort (résultat d'un ECDH, clé maître) : **KDF** rapide, comme **HKDF** (basé sur HMAC), pour dériver plusieurs clés distinctes (une pour chiffrer, une pour authentifier) avec des contextes différents
    * Ne jamais utiliser un mot de passe, un secret **ECDH** brut ou un simple **SHA-256** directement comme clé **AES**

### DEK et KEK

* **DEK** (Data Encryption Key) : clé aléatoire qui chiffre les données (**AES-GCM**), stockée chiffrée avec les données
* **KEK** (Key Encryption Key) : clé qui chiffre la **DEK**. Elle peut être dérivée d'un mot de passe (**KDF** + sel), stockée dans un **KMS**/**HSM**, etc.
* Mot de passe ──KDF──► KEK ──chiffre──► DEK ──chiffre──► données
* Changer de mot de passe : on dérive une nouvelle **KEK** et on rechiffre seulement la **DEK** (re-wrap), pas les données
* Le **KDF** (sel, algo, paramètres) doit être stocké dans l'en-tête, avec la version du format
* Même schéma pour une clé privée protégée par passphrase : la passphrase donne une **KEK** par **KDF**, qui chiffre la clé privée (**PKCS#8** chiffré). Le coût du **KDF** (**scrypt**, itérations élevées) est le vrai levier contre un brute force sur un fichier volé

### Pour les JWT (JSON Web Tokens)

* **`HS256` (HMAC-SHA-256) :** produit et valide le jeton avec le **même secret** symétrique.
* **`RS256` :** signe avec la **clé privée RSA** et valide avec la **clé publique RSA** (**`PS256`** avec RSA-PSS est préférable).
* **`ES256` :** signe avec la **clé privée ECDSA (P-256)** et valide avec la **clé publique**.
* **`EdDSA` :** signe avec la **clé privée Ed25519** et valide avec la **clé publique**.

### Quel algo pour quel besoin ?

| Besoin | À utiliser | À éviter |
|---|---|---|
| Empreinte d'un fichier | SHA-256, SHA-3, BLAKE2 | MD5, SHA-1 |
| Authentifier avec une clé partagée | HMAC-SHA256 | `hash(clé \|\| message)` |
| Hasher un mot de passe | Argon2id, scrypt, PBKDF2 | SHA-256 simple, MD5, `surtout sans sel` |
| Dériver des clés d'un secret | HKDF | secret brut utilisé comme clé |
| Chiffrer des données | AES-GCM, ChaCha20-Poly1305 (AEAD) | ECB, CBC ou CTR sans MAC |
| Échanger une clé | X25519 (ECDH) + HKDF, RSA-OAEP | RSA brut, PKCS#1 v1.5 |
| Chiffrer un gros fichier | Hybride : clé symétrique aléatoire + clé publique | RSA sur le fichier |
| Signer | Ed25519, ECDSA P-256, RSA-PSS | RSA PKCS#1 v1.5 (legacy), MD5/SHA-1 |
