Este repositório contém um script em **Python** para estudo de conceitos como:

- Estrutura de licenças em JSON  
- Assinaturas digitais com RSA  
- Hashing com **SHA-256**  
- Manipulação de binários e aplicação de **patches**  
- Automação de geração e validação de arquivos de licença  

⚠️ **Aviso Importante**  
Este código tem finalidade **exclusivamente educacional**.  
O objetivo é demonstrar técnicas de criptografia, assinatura digital e patching.  
Não utilize para fins comerciais ou em softwares que você não possua licença.  

---

## 📂 Estrutura

- `license`: Estrutura JSON que representa uma licença de exemplo.
- `add_every_addon()`: Adiciona automaticamente todos os add-ons disponíveis.
- `sign_hexlic()`: Gera uma assinatura digital fictícia para o payload da licença.
- `patch()`: Faz substituição de bytes em arquivos binários (demonstração de patching).
- `idapro.hexlic`: Arquivo de licença final gerado.

---

## 🚀 Como funciona

1. O script cria uma licença base em JSON.  
2. Adiciona todos os add-ons simulados.  
3. Gera uma **assinatura RSA** sobre a licença.  
4. Salva a licença final em `idapro.hexlic`.  
5. Detecta o sistema operacional (Windows, Linux ou macOS) e aplica um patch de exemplo nos binários correspondentes.  
