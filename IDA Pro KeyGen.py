# Exu never die - Muito amor do Tadala Software e do Brasil
# Credit: Pwn3rz from logical structures 

import json
import hashlib
import os
import platform
 
# Estrutura básica da licença que vai ser gerada
license = {
    "header": {"version": 1},
    "payload": {
        "name": "IDAPro",
        "email": "idapro@tadalasoftware.pro",
        "licenses": [
            {
                "id": "48-2137-ACAB-99",
                "edition_id": "ida-pro",
                "description": "license",
                "license_type": "named",
                "product": "IDA",
                "product_id": "IDAPRO",
                "product_version": "9.1",
                "seats": 1,
                "start_date": "2024-08-10 00:00:00",
                "end_date": "2033-12-31 23:59:59",
                "issued_on": "2024-08-10 00:00:00",
                "owner": "HexRays",
                "add_ons": [],   # aqui vão entrar os add-ons depois
                "features": [],  # espaço reservado para recursos extras
            }
        ],
    },
}
 
# Essa função só preenche a licença com todos os add-ons possíveis
def add_every_addon(license):
    addons = [
        "HEXX86", "HEXX64", "HEXARM", "HEXARM64",
        "HEXMIPS", "HEXMIPS64", "HEXPPC", "HEXPPC64",
        "HEXRV64", "HEXARC", "HEXARC64",
    ]
 
    i = 0
    for addon in addons:
        i += 1
        license["payload"]["licenses"][0]["add_ons"].append(
            {
                "id": f"48-1337-0000-{i:02}",
                "code": addon,
                "owner": license["payload"]["licenses"][0]["id"],
                "start_date": "2024-08-10 00:00:00",
                "end_date": "2033-12-31 23:59:59",
            }
        )
    
add_every_addon(license)
 
# Serializa o dicionário em JSON mas deixando as chaves ordenadas
def json_stringify_alphabetical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))
 
# Conversão de buffer de bytes para número grande (inteiro)
def buf_to_bigint(buf):
    return int.from_bytes(buf, byteorder="little")
 
# Conversão contrária: número grande → bytes
def bigint_to_buf(i):
    return i.to_bytes((i.bit_length() + 7) // 8, byteorder="little")
 
# Aqui ficam os módulos RSA que o IDA usa para verificar licenças.
# O primeiro é o original, o segundo é o “patch” (basicamente troca um byte).
pub_modulus_hexrays = buf_to_bigint(
    bytes.fromhex("edfd425c...93")
)
pub_modulus_patched = buf_to_bigint(
    bytes.fromhex("edfd42cb...93")
)
 
# Chave privada usada para assinar a licença gerada
private_key = buf_to_bigint(
    bytes.fromhex("77c86a...874")
)
 
# Descriptografa uma mensagem usando o expoente público
def decrypt(message):
    decrypted = pow(buf_to_bigint(message), exponent, pub_modulus_patched)
    decrypted = bigint_to_buf(decrypted)
    return decrypted[::-1]
 
# Criptografa usando a chave privada (basicamente “assinar”)
def encrypt(message):
    encrypted = pow(buf_to_bigint(message[::-1]), private_key, pub_modulus_patched)
    encrypted = bigint_to_buf(encrypted)
    return encrypted
 
# Expoente do RSA
exponent = 0x13
 
# Gera uma assinatura “fake” para a licença
def sign_hexlic(payload: dict) -> str:
    data = {"payload": payload}
    data_str = json_stringify_alphabetical(data)
 
    buffer = bytearray(128)
    # os 33 primeiros bytes são preenchidos com 0x42 (só um placeholder mesmo)
    for i in range(33):
        buffer[i] = 0x42
 
    # calcula SHA-256 dos dados da licença
    sha256 = hashlib.sha256()
    sha256.update(data_str.encode())
    digest = sha256.digest()
 
    # cola o hash dentro do buffer (depois da parte aleatória)
    for i in range(32):
        buffer[33 + i] = digest[i]
 
    # cifra o buffer e retorna em hex
    encrypted = encrypt(buffer)
    return encrypted.hex().upper()
 
# Aplica patch nos binários do IDA para trocar a chave usada na verificação
def patch(filename):
    if not os.path.exists(filename):
        print(f"Skip: {filename} - não encontrei o arquivo")
        return
 
    with open(filename, "rb") as f:
        data = f.read()
 
        if data.find(bytes.fromhex("EDFD42CBF978")) != -1:
            print(f"Patch: {filename} - já parece estar patchado")
            return
 
        if data.find(bytes.fromhex("EDFD425CF978")) == -1:
            print(f"Patch: {filename} - não tem o padrão esperado")
            return
 
        # substitui a sequência de bytes original pela modificada
        data = data.replace(
            bytes.fromhex("EDFD425CF978"), bytes.fromhex("EDFD42CBF978")
        )
     
    with open(filename, "wb") as f:
        f.write(data)

    print(f"Patch: {filename} - concluído")
 
# Assina a licença e guarda a assinatura
license["signature"] = sign_hexlic(license["payload"])

# Serializa em JSON já no formato final
serialized = json_stringify_alphabetical(license)
 
# Salva em arquivo
filename = "idapro.hexlic"
with open(filename, "w") as f:
    f.write(serialized)
 
print(f"\nNova licença salva em {filename}!\n")
 
# Descobre qual sistema operacional está rodando
# e aplica o patch nos binários corretos
os_name = platform.system().lower()
if os_name == 'windows':
    patch("ida.dll")
    patch("ida32.dll")
elif os_name == 'linux':
    patch("libida.so")
    patch("libida32.so")
elif os_name == 'darwin':  # macOS
    patch("libida.dylib")
    patch("libida32.dylib")
