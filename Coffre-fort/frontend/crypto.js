import sodium from "./vendor/libsodium-wrappers.mjs";


export async function init() {
    await sodium.ready;
}


export function randomBytes(n) {
    return sodium.randombytes_buf(n);
}


export function deriveMasterKey(password, salt) {
    return sodium.crypto_pwhash(
        32,
        password,
        salt,
        3,
        64*1024*1024,
        sodium.crypto_pwhash_ALG_ARGON2ID13
    );
}


export async function deriveKeys(masterKey) {
    const base = await crypto.subtle.importKey("raw", masterKey, "HKDF", false, ["deriveBits"]);
    const kek = new Uint8Array(await crypto.subtle.deriveBits(
        { name: "HKDF", hash: "SHA-256", salt: new Uint8Array(), info: new TextEncoder().encode("enc") },
        base,
        256
    ));
    const authKey = new Uint8Array(await crypto.subtle.deriveBits(
        { name: "HKDF", hash: "SHA-256", salt: new Uint8Array(), info: new TextEncoder().encode("auth") },
        base,
        256
    ));

    return { kek: kek, authKey: authKey };
}


export function encrypt(key, data) {
    const nonce = randomBytes(24);
    const ct = sodium.crypto_aead_xchacha20poly1305_ietf_encrypt(data, null, null, nonce, key)
    return { nonce: nonce, ct: ct };
}


export function decrypt(key, nonce, ct) {
    return sodium.crypto_aead_xchacha20poly1305_ietf_decrypt( null, ct, null, nonce, key );
}