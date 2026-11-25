## Exercice 5 : chiffrer un gros fichier (clé symétrique)

### 5a. Reconstituer un AEAD à la main (encrypt-then-MAC)

```bash
head -c 10M /dev/urandom > gros.bin
K_ENC=$(openssl rand -hex 32); K_MAC=$(openssl rand -hex 32); IV=$(openssl rand -hex 16)

# Chiffrement : IV || chiffré, puis HMAC(IV || chiffré)
openssl enc -aes-256-ctr -K $K_ENC -iv $IV -in gros.bin -out gros.ct
{ echo -n $IV | xxd -r -p; cat gros.ct; } > gros.blob
openssl dgst -sha256 -mac HMAC -macopt hexkey:$K_MAC -binary gros.blob > gros.tag

# Déchiffrement : vérifier le tag AVANT de déchiffrer
openssl dgst -sha256 -mac HMAC -macopt hexkey:$K_MAC -binary gros.blob | cmp - gros.tag && echo "tag OK"
tail -c +17 gros.blob | openssl enc -d -aes-256-ctr -K $K_ENC -iv $(head -c 16 gros.blob | xxd -p) > gros.dec
cmp gros.bin gros.dec && echo "identique"
```

- Modifiez un octet de `gros.blob` : le tag le détecte-t-il ?
- Pourquoi vérifier avant de déchiffrer ? Pourquoi deux clés distinctes ?
- Défauts par rapport à un vrai AEAD : comparaison non constante (`cmp`), pas d'AAD, assemblage manuel fragile, tout en un bloc (pas de chunks, pas de protection contre la troncature d'un flux).
