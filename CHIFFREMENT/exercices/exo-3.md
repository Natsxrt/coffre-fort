## Exercice 3 : chiffrement symétrique avec un mot de passe

### 3a. Chiffrer et déchiffrer une donnée

```bash
export MDP="phrase de passe longue"

echo -n "Donnée secrète" | openssl enc -aes-256-cbc -pbkdf2 -iter 600000 -salt -a -pass env:MDP > secret.b64
cat secret.b64
openssl enc -d -aes-256-cbc -pbkdf2 -iter 600000 -a -pass env:MDP -in secret.b64
```

- Chiffrez deux fois la même donnée : pourquoi les sorties diffèrent ? Regardez l'en-tête : `base64 -d secret.b64 | xxd | head` (préfixe `Salted__` + sel de 8 octets).
- Retirez `-iter` au déchiffrement : que se passe-t-il ? Qu'en conclure sur le stockage des paramètres du KDF ?
- Utilisez un mauvais mot de passe. Parfois `bad decrypt`, parfois du bruit : pourquoi ?
- Pourquoi `-pass env:MDP` plutôt que `-pass pass:...` ?

### 3b. Constater l'absence d'authentification

```bash
openssl enc -aes-256-cbc -pbkdf2 -pass env:MDP -in fichier.txt -out f.enc
printf '\xff' | dd of=f.enc bs=1 seek=20 conv=notrunc
openssl enc -d -aes-256-cbc -pbkdf2 -pass env:MDP -in f.enc
```

- La modification est-elle détectée ? Qu'obtient-on en sortie ?
