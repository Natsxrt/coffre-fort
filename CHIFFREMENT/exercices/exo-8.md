## Exercice 8 : échange de clés X25519 + HKDF

```bash
# Bob : clé long terme
openssl genpkey -algorithm X25519 -out bob.key
openssl pkey -in bob.key -pubout -out bob.pub

# Alice : clé éphémère, secret partagé
openssl genpkey -algorithm X25519 -out eph.key
openssl pkey -in eph.key -pubout -out eph.pub
openssl pkeyutl -derive -inkey eph.key -peerkey bob.pub -out secret.bin

# Dérivation des clés (HKDF-SHA256) : ne jamais utiliser le secret brut
openssl kdf -keylen 64 -binary \
  -kdfopt digest:SHA256 -kdfopt hexkey:$(xxd -p -c 256 secret.bin) \
  -kdfopt info:"exercice-v1" HKDF > keys.bin
# 32 premiers octets = clé de chiffrement, 32 suivants = clé MAC
```

- Refaites le calcul côté Bob (`-inkey bob.key -peerkey eph.pub`) : les clés dérivées sont-elles identiques ?
- Changez `info` : que se passe-t-il ? À quoi sert ce paramètre ?
- Reprenez l'exercice 5a avec ces deux clés pour chiffrer un fichier, puis signez le tout avec Ed25519.
- Alice envoie `eph.pub`, le chiffré et le tag. Qui peut retrouver la clé ? La clé éphémère d'Alice est-elle conservée ? Quelle propriété cela donne-t-il ?
- Que manque-t-il pour que Bob sache que c'est bien Alice ? Et comment Alice sait-elle que `bob.pub` est réellement celui de Bob ?