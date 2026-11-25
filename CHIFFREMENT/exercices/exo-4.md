## Exercice 4 : chiffrement symétrique avec une clé brute

Ici pas de mot de passe : une **clé aléatoire** de la bonne taille, que l'on gère soi-même.

### 4a. AES-256-CBC avec clé et IV explicites

```bash
KEY=$(openssl rand -hex 32)    # 256 bits
IV=$(openssl rand -hex 16)     # 128 bits

echo -n "Donnée secrète" | openssl enc -aes-256-cbc -K $KEY -iv $IV -out donnee.enc
openssl enc -d -aes-256-cbc -K $KEY -iv $IV -in donnee.enc
```

- Quelle est la taille du chiffré pour 14 octets de clair ? (padding PKCS#7 : relisez avec `xxd`)
- Chiffrez deux fois avec le **même IV** puis avec un **IV différent** : comparez les sorties.
- Déchiffrez avec un mauvais IV : seuls les premiers blocs sont corrompus. Pourquoi ?
- Que se passe-t-il avec une clé de mauvaise longueur (`-K` trop court) ?

### 4b. AES-256-CTR et ChaCha20 (chiffrements de flux)

```bash
KEY=$(openssl rand -hex 32)
IV=$(openssl rand -hex 16)

echo -n "Message" | openssl enc -aes-256-ctr -K $KEY -iv $IV | xxd
echo -n "Message" | openssl enc -chacha20 -K $KEY -iv $IV | xxd
```

- Pas de padding : taille du chiffré = taille du clair. Quel risque ?
- Pourquoi ces modes ne protègent-ils pas contre une modification ? Modifiez un octet du chiffré et déchiffrez : que change-t-il dans le clair ?

### 4c. ECB : voir les motifs

```bash
KEY=$(openssl rand -hex 16)
yes "AAAAAAAAAAAAAAAA" | head -n 4 | tr -d '\n' | openssl enc -aes-128-ecb -K $KEY | xxd
yes "AAAAAAAAAAAAAAAA" | head -n 4 | tr -d '\n' | openssl enc -aes-128-cbc -K $KEY -iv $(openssl rand -hex 16) | xxd
```

- Repérez les blocs répétés en ECB. Pourquoi sont-ils absents en CBC ?

### 4d. Réutilisation de nonce (many-time pad)

```bash
K=$(openssl rand -hex 32); N=$(openssl rand -hex 16)
echo -n "ATTAQUE A L AUBE" | openssl enc -aes-256-ctr -K $K -iv $N > c1.bin
echo -n "RETRAITE A MIDI.." | openssl enc -aes-256-ctr -K $K -iv $N > c2.bin
python3 -c "
a=open('c1.bin','rb').read(); b=open('c2.bin','rb').read()
print(bytes(x^y for x,y in zip(a,b)))"
```

- Le résultat est `clair1 XOR clair2`, sans connaître la clé. Que déduire avec un mot probable ("crib dragging") ?

### 4e. Un vrai AEAD (AES-GCM, ChaCha20-Poly1305) avec AAD

`openssl enc` ne le fait pas : passer par Python et la lib **cryptography** (`pip install cryptography`).

```python
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from cryptography.exceptions import InvalidTag

key = AESGCM.generate_key(bit_length=256)
nonce = os.urandom(12)
aad = b"users|email|42"

ct = AESGCM(key).encrypt(nonce, b"alice@example.org", aad)
print(AESGCM(key).decrypt(nonce, ct, aad))

# AAD différente (copie de la donnée sur une autre ligne)
try:
    AESGCM(key).decrypt(nonce, ct, b"users|email|43")
except InvalidTag:
    print("AAD différente : rejeté")

# Chiffré modifié
bad = bytes([ct[0] ^ 1]) + ct[1:]
try:
    AESGCM(key).decrypt(nonce, bad, aad)
except InvalidTag:
    print("Chiffré modifié : rejeté")

# Même chose avec ChaCha20-Poly1305
c2 = ChaCha20Poly1305(key).encrypt(nonce, b"alice@example.org", aad)
```

- Quelle est la taille du chiffré par rapport au clair ? Où est le tag ?
- Mauvaise clé et chiffré corrompu donnent-ils la même erreur ? Pourquoi est-ce voulu ?
- Rechiffrez avec le **même nonce** deux messages différents et XORez les chiffrés : retrouvez-vous le many-time pad de l'exercice 4d ?
