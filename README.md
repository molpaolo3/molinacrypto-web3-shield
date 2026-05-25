# MolinaCrypto Web3 Shield

**MolinaCrypto Web3 Shield** is an open source desktop tool designed to perform preliminary security and awareness checks on public crypto/Web3 data before the user takes operational decisions.

Project connected to: <https://www.molinacrypto.eu>

Current version: **v0.5**

---

## English

### Overview

MolinaCrypto Web3 Shield helps users inspect public Bitcoin, Ethereum/EVM, Web3, URL, e-mail and Lightning-related data without requesting wallet connection, seed phrases, private keys or passwords.

The tool is designed for prevention, awareness and first-level risk evaluation. It does not replace a wallet simulator, a blockchain forensic platform, professional cybersecurity analysis, legal advice, tax advice or investment advice.

### Main features in v0.5

#### New tabbed UX

Version 0.5 introduces a clearer tab-based interface:

- **Wallet & TX**
- **Web Risk**
- **Lightning**

This keeps the interface cleaner and makes future features easier to add without cluttering the first screen.

#### Wallet & TX

- Bitcoin address format recognition.
- Bitcoin public address check via mempool.space API.
- Confirmed BTC balance.
- Unconfirmed/mempool balance.
- Confirmed and unconfirmed transaction count.
- Recommended Bitcoin fee snapshot.
- Ethereum/EVM public address recognition.
- Direct quick actions for Etherscan, Revoke.cash, BaseScan, PolygonScan and Arbiscan.
- New **Bitcoin Transaction Check** for public Bitcoin TXIDs.
- Bitcoin transaction status: confirmed/unconfirmed.
- Bitcoin block height and block time when available.
- Transaction inputs/outputs.
- Total output amount.
- Fee and estimated fee rate in sat/vB.
- Quick links to mempool.space and Blockstream.

#### Web Risk

- URL, e-mail and dApp preliminary risk check.
- URL validation for `https://`, `http://` and `www.` formats.
- E-mail address static risk analysis.
- Suspicious keyword detection.
- Brand/domain impersonation indicators.
- HTTPS/IP/punycode/long-domain warnings.
- Fixed VirusTotal URL quick action.
- Fixed URLScan domain search quick action.
- Smart contract/EVM address format check.
- Signature / Approval Check for common Web3 approval and signing risks.
- Detection of keywords such as `approve`, `setApprovalForAll`, `permit`, `permit2`, `eth_sign`, `transferFrom`, `safeTransferFrom`.
- Direct Revoke.cash and Etherscan links when an EVM address is detected in signature text.
- No generic useless quick-action links when no EVM address is detected.

#### Lightning

- New **Lightning Invoice / LNURL Check**.
- Local decoding of BOLT11 Lightning invoices where supported.
- Invoice network detection: mainnet/testnet/regtest-like.
- Invoice amount detection when present.
- Creation and expiry time.
- Description field when present.
- Payment hash presence indicator.
- Expired invoice warning.
- Amountless invoice warning.
- Missing description warning.
- LNURL decoding.
- LNURL endpoint check.
- Lightning Address check using the standard `/.well-known/lnurlp/` endpoint.
- LNURL type, callback, min/max amount and comment support when available.
- Warning for LNURL-auth/login flows.
- Warning for non-HTTPS endpoints.

### Security model

This tool:

- does **not** ask for seed phrases;
- does **not** ask for private keys;
- does **not** ask for passwords;
- does **not** connect to wallets;
- does **not** sign transactions;
- does **not** move funds;
- works only with public data or text manually pasted by the user.

### External services

Depending on the selected check, the tool may query or open external services, including mempool.space, Blockstream, Etherscan, Revoke.cash, BaseScan, PolygonScan, Arbiscan, VirusTotal, URLScan, Google Search and public Lightning Address / LNURL endpoints.

The user remains responsible for evaluating whether opening or querying an external service is appropriate in their context.

### Limitations

MolinaCrypto Web3 Shield provides an indicative risk score based on static checks, public data and heuristic indicators.

It cannot guarantee that a wallet, URL, contract, signature, invoice, LNURL or transaction is safe. It cannot verify ownership of addresses, real-world identities, intent of a transaction or whether a Lightning payment has already been completed.

Lightning payments are off-chain. The tool can inspect the payment request, invoice, LNURL or Lightning Address endpoint, but it cannot act as a universal Lightning payment explorer.

### Linux/source usage

Install Python 3 and Tkinter if not already available.

On Debian/Ubuntu/Linux Mint:

```bash
sudo apt update
sudo apt install python3 python3-tk
```

Run:

```bash
python3 MolinaCryptoWeb3Shield.py
```

If an `avvia.sh` script is included:

```bash
chmod +x avvia.sh
./avvia.sh
```

### Windows portable usage

The Windows portable release is distributed as a ZIP containing an `.exe` file. Extract the ZIP and run:

```text
MolinaCryptoWeb3Shield.exe
```

Windows may show a SmartScreen or security warning because the executable is not signed with a commercial code-signing certificate. This does not automatically mean the file is malicious. Users should download the program only from the official GitHub release page and verify the SHA256 hash when provided.

### Project links

- Website: <https://www.molinacrypto.eu>
- Resources: <https://www.molinacrypto.eu/risorse.html>

### Disclaimer

This tool is for informational and educational security awareness purposes only. It does not provide financial, investment, tax, legal or professional cybersecurity advice. The responsibility for any operational decision remains with the user.

---

## Italiano

### Panoramica

**MolinaCrypto Web3 Shield** aiuta l’utente a controllare dati pubblici Bitcoin, Ethereum/EVM, Web3, URL, e-mail e Lightning prima di prendere decisioni operative.

Il tool è pensato per prevenzione, consapevolezza e prima valutazione del rischio. Non sostituisce un wallet simulator, una piattaforma di blockchain forensic, un’analisi professionale di cybersecurity, una consulenza legale, fiscale o finanziaria.

### Novità principali della v0.5

La versione 0.5 introduce una nuova interfaccia a schede:

- **Wallet & TX**
- **Web Risk**
- **Lightning**

La sezione **Wallet & TX** include controllo wallet/address Bitcoin ed Ethereum/EVM e nuovo controllo TXID Bitcoin pubblico. La sezione **Web Risk** mantiene e migliora URL/e-mail/dApp, Smart Contract Check e Signature / Approval Check. La sezione **Lightning** introduce controllo preventivo di invoice Lightning, LNURL e Lightning Address.

### Modello di sicurezza

Questo tool non chiede seed phrase, private key o password, non collega il wallet, non firma transazioni e non sposta fondi. Lavora solo con dati pubblici o testo incollato manualmente dall’utente.

### Servizi esterni

A seconda del controllo selezionato, il tool può interrogare o aprire servizi esterni, tra cui mempool.space, Blockstream, Etherscan, Revoke.cash, BaseScan, PolygonScan, Arbiscan, VirusTotal, URLScan, Google Search ed endpoint pubblici Lightning Address / LNURL.

### Limiti

MolinaCrypto Web3 Shield fornisce uno score indicativo basato su controlli statici, dati pubblici e indicatori euristici. Non può garantire che wallet, URL, contratto, firma, invoice, LNURL o transazione siano sicuri. Lightning è off-chain: il tool può ispezionare richiesta di pagamento, invoice, LNURL o endpoint Lightning Address, ma non può funzionare come explorer universale dei pagamenti Lightning.

### Uso Linux/source

```bash
sudo apt update
sudo apt install python3 python3-tk
python3 MolinaCryptoWeb3Shield.py
```

Con `avvia.sh`:

```bash
chmod +x avvia.sh
./avvia.sh
```

### Uso Windows portable

Estrarre lo ZIP ed eseguire:

```text
MolinaCryptoWeb3Shield.exe
```

Windows può mostrare un avviso SmartScreen o di sicurezza perché l’eseguibile non è firmato con certificato commerciale. Scaricare il programma solo dalla release GitHub ufficiale e verificare l’hash SHA256 quando disponibile.

### Disclaimer

Questo tool ha finalità informative, educative e di security awareness. Non costituisce consulenza finanziaria, di investimento, fiscale, legale o professionale in ambito cybersecurity. La responsabilità delle decisioni operative resta dell’utente.
