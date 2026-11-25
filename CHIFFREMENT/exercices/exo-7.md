## Exercice 7 : signature

### 7a. Ed25519

```bash
openssl genpkey -algorithm ED25519 -out alice.key
openssl pkey -in alice.key -pubout -out alice.pub

echo "Virement de 100 EUR a Bob" > message.txt
openssl pkeyutl -sign -rawin -inkey alice.key -in message.txt -out message.sig
openssl pkeyutl -verify -rawin -pubin -inkey alice.pub -in message.txt -sigfile message.sig
```

- Modifiez `message.txt` d'un caractère et revérifiez.
- Vérifiez avec la clé publique d'une autre paire : que se passe-t-il ?
- Signez deux fois : les signatures sont-elles identiques ?

### 7b. ECDSA P-256 (certificats, WebCrypto)

```bash
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out ec.key
openssl pkey -in ec.key -pubout -out ec.pub
openssl dgst -sha256 -sign ec.key -out ec.sig message.txt
openssl dgst -sha256 -verify ec.pub -signature ec.sig message.txt
```

- Signez deux fois : les signatures diffèrent-elles ? Pourquoi ? Quel risque si le nonce est mal généré ou réutilisé ?

### 7c. RSA-PSS

```bash
openssl dgst -sha256 -sign rsa.key \
  -sigopt rsa_padding_mode:pss -sigopt rsa_pss_saltlen:32 -out rsa.sig message.txt
openssl dgst -sha256 -verify rsa.pub \
  -sigopt rsa_padding_mode:pss -sigopt rsa_pss_saltlen:32 -signature rsa.sig message.txt
```

- Signez deux fois : les signatures diffèrent-elles ? Comparez la taille de la signature avec Ed25519.

### 7d. Signature et chiffrement : ce que chacun apporte

- La signature de `message.txt` cache-t-elle son contenu ?
- Chiffrer avec `rsa.pub` prouve-t-il l'identité de l'expéditeur ?
- Dans quel ordre combiner signature et chiffrement, et quels pièges (re-chiffrement d'un message signé par un tiers) ?