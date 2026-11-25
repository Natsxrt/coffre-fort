
## Exercice 2 : hachage de mot de passe (KDF)

```bash
SEL=$(openssl rand -hex 16)

# scrypt
openssl kdf -keylen 32 \
  -kdfopt pass:azerty123 -kdfopt hexsalt:$SEL \
  -kdfopt n:32768 -kdfopt r:8 -kdfopt p:1 -kdfopt maxmem_bytes:67108864 \
  SCRYPT

# Argon2id (OpenSSL 3.2+)
openssl kdf -keylen 32 \
  -kdfopt pass:azerty123 -kdfopt hexsalt:$SEL \
  -kdfopt iter:3 -kdfopt memcost:65536 -kdfopt lanes:4 -kdfopt threads:4 \
  ARGON2ID

# PBKDF2 (pour comparer)
openssl kdf -keylen 32 -kdfopt digest:SHA256 \
  -kdfopt pass:azerty123 -kdfopt hexsalt:$SEL -kdfopt iter:600000 \
  PBKDF2
```

- Relancez avec un **autre sel** : que se passe-t-il ? Pourquoi stocker le sel avec le hash ? Est-il secret ?
- Mesurez avec `time` en faisant varier `n` (scrypt) ou `memcost` (Argon2). Combien d'essais par seconde pour un attaquant ?
- Comparez avec un SHA-256 simple : combien de fois plus lent est le KDF ?
