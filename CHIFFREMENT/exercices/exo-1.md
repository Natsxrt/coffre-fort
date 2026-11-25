## Exercice 1 : fonctions de hachage

### 1a. Hash d'un fichier

```bash
echo "Bonjour" > fichier.txt
openssl dgst -sha256 fichier.txt
openssl dgst -sha3-256 fichier.txt
openssl dgst -blake2b512 fichier.txt
```


- Modifiez un seul caractère de `fichier.txt` et comparez les empreintes.
- Générez un fichier de 1 Go (`head -c 1G /dev/urandom > gros.bin`) et chronométrez SHA-256, SHA3-256 et BLAKE2 (`time openssl dgst ...`).
- Calculez `openssl dgst -md5` et `-sha1`. Cherchez « MD5 collision » et « SHAttered » : pourquoi sont-ils interdits pour l'intégrité ?

### 1b. HMAC (hash avec clé)

```bash
openssl dgst -sha256 -hmac "cle-secrete" fichier.txt
```

- Quelle différence avec `sha256(cle || fichier)` ? Pourquoi HMAC existe-t-il ?
- Que se passe-t-il si on modifie le fichier ? Si on change la clé ?

### 1c. Ce qu'il ne faut PAS faire pour un mot de passe

```bash
echo -n "azerty123" | openssl dgst -sha256
```

- Cherchez cette empreinte dans une rainbow table en ligne. Conclusion ?
- Combien de SHA-256 par seconde un attaquant peut-il calculer sur un GPU ?
