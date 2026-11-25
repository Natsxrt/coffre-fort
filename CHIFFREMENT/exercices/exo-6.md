
## Exercice 6 : chiffrement avec une clé asymétrique

### 6a. RSA-OAEP sur une petite donnée

```bash
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:3072 -out rsa.key
openssl pkey -in rsa.key -pubout -out rsa.pub

echo -n "Secret court" > petit.txt

openssl pkeyutl -encrypt -pubin -inkey rsa.pub \
  -pkeyopt rsa_padding_mode:oaep -pkeyopt rsa_oaep_md:sha256 -pkeyopt rsa_mgf1_md:sha256 \
  -in petit.txt -out petit.enc

openssl pkeyutl -decrypt -inkey rsa.key \
  -pkeyopt rsa_padding_mode:oaep -pkeyopt rsa_oaep_md:sha256 -pkeyopt rsa_mgf1_md:sha256 \
  -in petit.enc
```

- Chiffrez deux fois la même donnée : les sorties diffèrent-elles ? Pourquoi ?
- Quelle est la taille du chiffré ? Indépendante du clair ?
- Déchiffrez avec une autre clé privée : que se passe-t-il ?
- Chiffrez avec `-pkeyopt rsa_padding_mode:none` (RSA "brut") : deux fois la même donnée, mêmes sorties ? Pourquoi est-ce dangereux ?

### 6b. La limite de taille

```bash
head -c 400 /dev/urandom > moyen.bin
openssl pkeyutl -encrypt -pubin -inkey rsa.pub \
  -pkeyopt rsa_padding_mode:oaep -pkeyopt rsa_oaep_md:sha256 -pkeyopt rsa_mgf1_md:sha256 \
  -in moyen.bin -out moyen.enc
```

- Que se passe-t-il ? Le maximum est `taille_clé - 2×taille_hash - 2` = 318 octets ici. Pourquoi RSA ne sert-il pas à chiffrer des fichiers ?

### 6c. Chiffrement hybride "à la main" (clé symétrique protégée par RSA)

```bash
head -c 10M /dev/urandom > gros.bin

# Alice tire une clé symétrique aléatoire pour ce fichier
openssl rand -out cle_fichier.bin 64
K_ENC=$(head -c 32 cle_fichier.bin | xxd -p -c 64)
K_MAC=$(tail -c 32 cle_fichier.bin | xxd -p -c 64)
IV=$(openssl rand -hex 16)

# Alice chiffre le fichier (encrypt-then-MAC)
openssl enc -aes-256-ctr -K $K_ENC -iv $IV -in gros.bin -out gros.ct
{ echo -n $IV | xxd -r -p; cat gros.ct; } > gros.blob
openssl dgst -sha256 -mac HMAC -macopt hexkey:$K_MAC -binary gros.blob > gros.tag

# Alice chiffre la clé symétrique avec la clé publique de Bob (RSA-OAEP)
openssl pkeyutl -encrypt -pubin -inkey rsa.pub \
  -pkeyopt rsa_padding_mode:oaep -pkeyopt rsa_oaep_md:sha256 -pkeyopt rsa_mgf1_md:sha256 \
  -in cle_fichier.bin -out cle_fichier.enc

# Alice envoie à Bob : cle_fichier.enc, gros.blob, gros.tag
```

Ecrire le **déchiffrement côté Bob** : déchiffrer `cle_fichier.enc` avec `rsa.key`, séparer les deux clés, vérifier le tag, puis déchiffrer.

- Pourquoi une clé symétrique **différente pour chaque fichier** ?
- Que voit un attaquant qui capture les trois fichiers ? Que peut-il modifier sans être détecté ?
- Alice a-t-elle prouvé son identité à Bob ? (n'importe qui connaît `rsa.pub`)

### 6d. Le même schéma avec un standard : CMS

```bash
openssl req -x509 -new -key rsa.key -subj "/CN=bob" -days 30 -out bob.crt

openssl cms -encrypt -binary -in gros.bin -recip bob.crt \
  -aes-256-cbc -keyopt rsa_padding_mode:oaep -outform DER -out gros.cms

openssl cms -decrypt -binary -in gros.cms -inform DER \
  -recip bob.crt -inkey rsa.key -out gros.dec
cmp gros.bin gros.dec && echo "identique"
```

- Inspectez la structure : `openssl cms -cmsout -print -inform DER -in gros.cms`. Où se trouve la clé symétrique chiffrée ? Quels algos sont indiqués ?
- Retirez `-keyopt rsa_padding_mode:oaep` : quel padding RSA est utilisé par défaut ? Pourquoi PKCS#1 v1.5 est-il déconseillé ?
