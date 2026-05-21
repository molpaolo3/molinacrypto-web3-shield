# Changelog

All notable changes to MolinaCrypto Web3 Shield will be documented in this file.

---

## [v0.4] - 2026-05-21

### English
Security and usability release focused on URL/e-mail/dApp checks, quick actions and startup disclaimer.

#### Added
- Bilingual startup disclaimer with accept/reject flow.
- Custom MolinaCrypto-style logo drawn in the desktop interface.
- E-mail address check inside the URL/e-mail/dApp section.
- URLScan quick action for checked domains.

#### Fixed
- Renamed Link/dApp Check to Check URL / e-mail / dApp.
- Added URL input validation for `https://`, `http://` and `www.` formats.
- Fixed VirusTotal URL quick action by using the correct URL identifier.
- Fixed URLScan search query generation.
- Improved Signature / Approval Check scoring for incomplete or non-interpretable input.
- Removed generic quick-action links when no EVM address is detected in signature text.
- Added direct Revoke.cash and Etherscan links when an EVM address is detected.

### Italiano
Release di sicurezza e usabilità dedicata ai controlli URL/e-mail/dApp, alle azioni rapide e al disclaimer iniziale.

#### Aggiunto
- Disclaimer bilingue all’avvio con scelta Accetta/Rifiuta.
- Logo in stile MolinaCrypto disegnato direttamente nell’interfaccia desktop.
- Controllo indirizzi e-mail nella sezione URL/e-mail/dApp.
- Azione rapida URLScan per i domini controllati.

#### Corretto
- Rinominata la sezione Link/dApp Check in Check URL / e-mail / dApp.
- Aggiunta validazione input URL per i formati `https://`, `http://` e `www.`.
- Corretto il link rapido VirusTotal usando l’identificativo URL corretto.
- Corretta la generazione della ricerca URLScan.
- Migliorato lo scoring del Signature / Approval Check per input incompleti o non interpretabili.
- Rimossi link rapidi generici quando nel testo firma non viene rilevato un address EVM.
- Aggiunti link diretti Revoke.cash ed Etherscan quando viene rilevato un address EVM.

---

## [v0.3] - 2026-05-18

### Fixed
- Added scrollable left control panel for better Windows/Linux display compatibility.
- Fixed layout issues on Windows where the Signature / Approval Check area could be cut off.
- Fixed footer visibility with Resources and molinacrypto.eu buttons.
- Fixed Quick actions panel visibility on smaller windows or scaled displays.

### Improved
- More robust desktop layout for Windows display scaling.

---

## [0.2] - 2026-05-18

### Added
- Added language label next to the IT/EN selector.
- Added clearer bilingual interface handling.
- Added Linux launcher script: `avvia.sh`.
- Added Italian and English user guides:
  - `README_IT.txt`
  - `README_EN.txt`
- Added GitHub project structure:
  - `README.md`
  - `LICENSE`
  - `.gitignore`
  - `requirements.txt`
  - `CHANGELOG.md`

### Improved
- Improved startup window layout.
- Improved visibility of all four main control cards.
- Improved usability of the Signature / Approval Check area.

---

## [0.1] - 2026-05-18

### Added
- First working prototype of MolinaCrypto Web3 Shield.
- Wallet / Address Check for Bitcoin and Ethereum/EVM public addresses.
- Bitcoin public data reading through mempool.space API.
- Ethereum/EVM address format recognition.
- Link / dApp static risk check.
- Smart Contract / EVM address format check.
- Signature / Approval keyword-based risk check.
- Web3 risk scoring system.
- Quick action buttons for:
  - Mempool.space
  - Blockstream
  - Etherscan
  - Revoke.cash
  - BaseScan
  - PolygonScan
  - Arbiscan
  - Google Search
  - VirusTotal
- TXT report export.
- Right-click menu for cut/copy/paste/select all.
- Italian / English interface.
