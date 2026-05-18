# MolinaCrypto Web3 Shield

**EN:** Open source desktop tool for preliminary Web3 safety checks on public wallet addresses, suspicious links, EVM smart contracts and signature/approval requests.

**IT:** Tool desktop open source per controlli preliminari di sicurezza Web3 su indirizzi wallet pubblici, link sospetti, smart contract EVM e richieste di firma/approval.

Project connected to / Progetto collegato a:  
https://www.molinacrypto.eu

---

# English

## What it is

MolinaCrypto Web3 Shield is an open source desktop program designed to help crypto and Web3 users perform simple preliminary safety checks before interacting with wallets, dApps, smart contracts, airdrops, claims, mints or signature requests.

It is designed for normal users, not only technical users.

The tool helps answer practical questions such as:

- Does this wallet address look formally correct?
- Could this Web3 link be suspicious?
- Is this smart contract/EVM address at least in the correct format?
- Does this Web3 signature contain risky words such as `approve`, `permit` or `setApprovalForAll`?
- Where can I quickly check approvals, explorers and public information?

---

## Security principles

MolinaCrypto Web3 Shield:

- does **not** ask for seed phrases;
- does **not** ask for private keys;
- does **not** ask for passwords;
- does **not** connect to wallets;
- does **not** sign transactions;
- does **not** move funds;
- does **not** custody crypto assets;
- does **not** create wallets;
- works only with public data or text manually pasted by the user.

Never enter:

- seed phrases;
- private keys;
- passwords;
- 2FA codes;
- recovery phrases;
- banking data;
- sensitive personal data.

If you accidentally pasted a seed phrase or private key into any program, website, chat or online form, consider that wallet potentially compromised.

---

## Main features

### Wallet / Address Check

Checks public Bitcoin and Ethereum/EVM addresses.

For Bitcoin addresses, the tool can read public data through mempool.space:

- confirmed balance;
- unconfirmed/mempool balance;
- confirmed transactions;
- unconfirmed transactions;
- estimated Bitcoin fee;
- quick links to Mempool.space and Blockstream.

For Ethereum/EVM addresses, the tool:

- validates the EVM address format;
- reminds users that the main Web3 risks are approvals, signatures and dApp interactions;
- provides quick links to Etherscan, Revoke.cash, BaseScan, PolygonScan and Arbiscan.

---

### Link / dApp Check

Performs a static check of suspicious Web3 links.

It looks for indicators such as:

- missing HTTPS;
- very long domains;
- many hyphens;
- IP-based hosts;
- suspicious Web3 words such as `claim`, `airdrop`, `verify`, `wallet`, `seed`, `restore`, `recover`;
- known brand names inside domains that do not look official.

Quick actions include:

- Open link;
- Google Search;
- VirusTotal URL search.

Important: the tool does not visit the website and does not analyze JavaScript. It only performs a static preliminary check.

---

### Smart Contract Check

Checks whether a pasted smart contract/address has a valid Ethereum/EVM format.

The tool reminds users to manually verify:

- verified or unverified source code;
- proxy contract;
- active owner;
- admin functions;
- pause / blacklist / mint / upgrade / withdraw functions;
- interaction history;
- consistency with the official project website.

Quick actions include:

- Etherscan;
- Revoke.cash;
- BaseScan;
- PolygonScan;
- Arbiscan.

---

### Signature / Approval Check

Interprets pasted Web3 signature or approval text using keyword-based risk indicators.

The tool looks for:

- `setApprovalForAll`;
- `approve`;
- `increaseAllowance`;
- `permit`;
- `permit2`;
- `eth_sign`;
- `personal_sign`;
- `eth_signTypedData`;
- `transferFrom`;
- `safeTransferFrom`;
- possible unlimited approvals;
- EVM addresses inside pasted text.

This is not a transaction simulator.  
It is a prudential text-based warning tool.

---

## Linux usage

Requirements:

- Python 3

Check Python version:

    python3 --version

Run the program:

    chmod +x avvia.sh
    ./avvia.sh

Alternatively:

    python3 MolinaCryptoWeb3Shield.py

No external Python packages are required.

---

## Project files

    MolinaCryptoWeb3Shield.py   Main Python application
    avvia.sh                    Linux launcher
    README.md                   GitHub README
    README_IT.txt               Detailed Italian guide
    README_EN.txt               Detailed English guide
    CHANGELOG.md                Version history
    LICENSE                     MIT License
    requirements.txt            Python dependency note

---

## Detailed English guide

For a full step-by-step English guide, read:

    README_EN.txt

---

## Disclaimer

MolinaCrypto Web3 Shield is provided for informational and educational purposes only.

It does not constitute financial, tax, legal, investment or professional cybersecurity advice.

The user remains responsible for their own decisions, official-source verification and wallet usage.

The tool does not guarantee that a website, wallet, smart contract or signature request is safe or dangerous.

---

# Italiano

## Cos’è

MolinaCrypto Web3 Shield è un programma desktop open source pensato per aiutare utenti crypto e Web3 a fare semplici controlli preliminari di sicurezza prima di interagire con wallet, dApp, smart contract, airdrop, claim, mint o richieste di firma.

È pensato per utenti normali, non solo per tecnici.

Il tool aiuta a rispondere a domande pratiche come:

- Questo indirizzo wallet sembra formalmente corretto?
- Questo link Web3 può essere sospetto?
- Questo smart contract/address EVM è almeno nel formato corretto?
- Questa firma Web3 contiene parole rischiose come `approve`, `permit` o `setApprovalForAll`?
- Dove posso controllare rapidamente approvals, explorer e informazioni pubbliche?

---

## Principi di sicurezza

MolinaCrypto Web3 Shield:

- non chiede **seed phrase**;
- non chiede **private key**;
- non chiede **password**;
- non collega il wallet;
- non firma transazioni;
- non sposta fondi;
- non custodisce criptovalute;
- non crea wallet;
- lavora solo con dati pubblici o testo incollato manualmente dall’utente.

Non inserire mai:

- seed phrase;
- private key;
- password;
- codici 2FA;
- recovery phrase;
- dati bancari;
- dati personali sensibili.

Se hai incollato per errore una seed phrase o una private key in qualsiasi programma, sito, chat o form online, considera quel wallet potenzialmente compromesso.

---

## Funzioni principali

### Wallet / Address Check

Controlla indirizzi pubblici Bitcoin ed Ethereum/EVM.

Per indirizzi Bitcoin, il tool può leggere dati pubblici tramite mempool.space:

- saldo confermato;
- saldo non confermato/mempool;
- transazioni confermate;
- transazioni non confermate;
- fee Bitcoin stimata;
- link rapidi verso Mempool.space e Blockstream.

Per indirizzi Ethereum/EVM, il tool:

- valida il formato dell’indirizzo EVM;
- ricorda che i principali rischi Web3 derivano da approvals, firme e interazioni con dApp;
- fornisce link rapidi verso Etherscan, Revoke.cash, BaseScan, PolygonScan e Arbiscan.

---

### Link / dApp Check

Effettua un controllo statico di link Web3 sospetti.

Cerca indicatori come:

- assenza di HTTPS;
- domini molto lunghi;
- molti trattini nel dominio;
- host basati su indirizzo IP;
- parole sospette Web3 come `claim`, `airdrop`, `verify`, `wallet`, `seed`, `restore`, `recover`;
- nomi di brand noti dentro domini che non sembrano ufficiali.

Azioni rapide disponibili:

- Apri link;
- Google Search;
- VirusTotal URL.

Importante: il tool non visita realmente il sito e non analizza JavaScript. Effettua solo un controllo preliminare statico.

---

### Smart Contract Check

Controlla se uno smart contract/address incollato ha un formato Ethereum/EVM valido.

Il tool ricorda all’utente di verificare manualmente:

- codice sorgente verificato o non verificato;
- proxy contract;
- owner attivo;
- funzioni admin;
- funzioni pause / blacklist / mint / upgrade / withdraw;
- cronologia delle interazioni;
- coerenza con il sito ufficiale del progetto.

Azioni rapide disponibili:

- Etherscan;
- Revoke.cash;
- BaseScan;
- PolygonScan;
- Arbiscan.

---

### Signature / Approval Check

Interpreta testo incollato relativo a firme Web3 o approval usando indicatori basati su parole chiave.

Il tool cerca:

- `setApprovalForAll`;
- `approve`;
- `increaseAllowance`;
- `permit`;
- `permit2`;
- `eth_sign`;
- `personal_sign`;
- `eth_signTypedData`;
- `transferFrom`;
- `safeTransferFrom`;
- possibili approval illimitate;
- indirizzi EVM presenti nel testo incollato.

Non è un simulatore di transazioni.  
È uno strumento prudenziale testuale per aiutare l’utente a capire quando fermarsi.

---

## Uso su Linux

Requisiti:

- Python 3

Verifica la versione Python:

    python3 --version

Avvia il programma:

    chmod +x avvia.sh
    ./avvia.sh

In alternativa:

    python3 MolinaCryptoWeb3Shield.py

Non sono richiesti pacchetti Python esterni.

---

## File del progetto

    MolinaCryptoWeb3Shield.py   Applicazione Python principale
    avvia.sh                    Launcher Linux
    README.md                   README GitHub
    README_IT.txt               Guida dettagliata in italiano
    README_EN.txt               Guida dettagliata in inglese
    CHANGELOG.md                Storico versioni
    LICENSE                     Licenza MIT
    requirements.txt            Nota sulle dipendenze Python

---

## Guida italiana dettagliata

Per una guida italiana completa passo-passo, leggere:

    README_IT.txt

---

## Disclaimer

MolinaCrypto Web3 Shield è fornito solo a scopo informativo ed educativo.

Non costituisce consulenza finanziaria, fiscale, legale, di investimento o cybersecurity professionale.

L’utente resta responsabile delle proprie decisioni, delle verifiche su fonti ufficiali e dell’uso dei propri wallet.

Il tool non garantisce che un sito, wallet, smart contract o richiesta di firma sia sicuro o pericoloso.

---

# License / Licenza

MIT License.

Copyright © 2026 Paolo Molina.
