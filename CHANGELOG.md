# Changelog

All notable changes to MolinaCrypto Web3 Shield are documented in this file.

---

## v0.5 - 2026-05-25

### English

Feature release focused on a cleaner tabbed UX, Bitcoin transaction analysis and Lightning preventive checks.

#### Added

- New tab-based interface with three macro sections:
  - Wallet & TX
  - Web Risk
  - Lightning
- New **Bitcoin TX Check** for public Bitcoin transaction IDs.
- Bitcoin transaction status detection: confirmed/unconfirmed.
- Bitcoin block height and block time when available.
- Bitcoin transaction input/output count.
- Bitcoin transaction total output amount.
- Bitcoin transaction fee and estimated fee rate in sat/vB.
- Bitcoin TX quick actions for mempool.space and Blockstream.
- New **Lightning Invoice / LNURL Check**.
- Local BOLT11 Lightning invoice decoding where supported.
- Lightning invoice amount, network, creation time, expiry time, description and payment hash indicators.
- Expired invoice warning.
- Amountless invoice warning.
- Missing invoice description warning.
- LNURL Bech32 decoding.
- LNURL endpoint check.
- Lightning Address check through the standard `/.well-known/lnurlp/` endpoint.
- LNURL type, callback, min/max amount and comment support indicators when available.
- LNURL-auth/login warning.
- Non-HTTPS endpoint warning.
- Better separation between Bitcoin/EVM wallet checks, Web3 risk checks and Lightning checks.

#### Changed

- Increased main window size to better support the new tabbed workflow.
- Updated result placeholder text to refer to tabs instead of a flat list of checks.
- Improved left-side panel organization to reduce visual clutter.
- Kept the result panel and quick-action workflow consistent with v0.4.1.
- Updated app subtitle to include transactions and Lightning.

#### Preserved from v0.4.1

- Windows startup disclaimer focus handling fix.
- Correct release of the disclaimer modal grab after accept/reject.
- Ability to type in input fields after closing the disclaimer on Windows.
- Correct VirusTotal URL identifier generation.
- Correct URLScan domain search generation.
- URL validation for `https://`, `http://` and `www.` formats.
- E-mail address static risk check.
- Improved Signature / Approval Check scoring for incomplete or non-interpretable input.
- Direct Revoke.cash and Etherscan links when an EVM address is detected in signature text.
- Removal of generic quick-action links when no EVM address is detected.

#### Security note

The tool still does not ask for seed phrases, private keys or passwords.  
It does not connect to wallets.  
It does not sign transactions.  
It does not move funds.  
It only works with public data or text manually pasted by the user.

---

### Italiano

Release funzionale dedicata a una UX più pulita a schede, all’analisi delle transazioni Bitcoin e ai controlli preventivi Lightning.

#### Aggiunto

- Nuova interfaccia a schede con tre macro sezioni:
  - Wallet & TX
  - Web Risk
  - Lightning
- Nuovo **Bitcoin TX Check** per TXID Bitcoin pubblici.
- Rilevamento stato transazione Bitcoin: confermata/non confermata.
- Altezza blocco e orario blocco quando disponibili.
- Numero input/output della transazione Bitcoin.
- Totale output della transazione Bitcoin.
- Fee e fee rate stimato in sat/vB.
- Azioni rapide Bitcoin TX verso mempool.space e Blockstream.
- Nuovo **Lightning Invoice / LNURL Check**.
- Decodifica locale invoice Lightning BOLT11 dove supportato.
- Indicatori su importo, rete, creazione, scadenza, descrizione e payment hash dell’invoice.
- Avviso invoice scaduta.
- Avviso invoice senza importo.
- Avviso descrizione invoice mancante.
- Decodifica LNURL Bech32.
- Controllo endpoint LNURL.
- Controllo Lightning Address tramite endpoint standard `/.well-known/lnurlp/`.
- Indicatori su tipo LNURL, callback, importo min/max e supporto commenti quando disponibili.
- Avviso LNURL-auth/login.
- Avviso endpoint non HTTPS.
- Migliore separazione tra controlli wallet Bitcoin/EVM, rischi Web3 e controlli Lightning.

#### Modificato

- Aumentata la dimensione della finestra principale per supportare meglio il nuovo workflow a schede.
- Aggiornato il testo iniziale del pannello risultati per fare riferimento alle schede.
- Migliorata l’organizzazione del pannello sinistro per ridurre l’affollamento visivo.
- Mantenuto coerente il pannello risultato e il workflow delle azioni rapide della v0.4.1.
- Aggiornato il sottotitolo dell’app includendo transazioni e Lightning.

#### Mantenuto dalla v0.4.1

- Fix della gestione focus del disclaimer iniziale su Windows.
- Rilascio corretto del blocco modale del disclaimer dopo Accetta/Rifiuta.
- Possibilità di scrivere nei campi dopo la chiusura del disclaimer su Windows.
- Generazione corretta identificativo VirusTotal URL.
- Generazione corretta ricerca URLScan per dominio.
- Validazione URL nei formati `https://`, `http://` e `www.`.
- Controllo statico degli indirizzi e-mail.
- Miglioramento scoring Signature / Approval Check per input incompleti o non interpretabili.
- Link diretti Revoke.cash ed Etherscan quando viene rilevato un address EVM nel testo firma.
- Rimozione link rapidi generici quando non viene rilevato un address EVM.

#### Nota di sicurezza

Il tool continua a non chiedere seed phrase, private key o password.  
Non collega il wallet.  
Non firma transazioni.  
Non sposta fondi.  
Lavora solo con dati pubblici o testo incollato manualmente dall’utente.

---

## v0.4.1 - 2026-05-21

### English

Desktop bugfix and packaging release based on v0.4.

#### Fixed

- Fixed startup disclaimer focus handling on Windows.
- The app now correctly releases the disclaimer modal grab after accept/reject.
- Fixed an issue where input fields could become unavailable after closing the disclaimer on Windows.
- Updated release packages to include the correct v0.4.1 documentation files.

### Italiano

Release bugfix e di packaging desktop basata sulla v0.4.

#### Corretto

- Corretta la gestione del focus del disclaimer iniziale su Windows.
- L’app ora rilascia correttamente il blocco modale del disclaimer dopo Accetta/Rifiuta.
- Corretto un problema per cui i campi di input potevano non essere compilabili dopo la chiusura del disclaimer su Windows.
- Aggiornati i pacchetti di release includendo la documentazione corretta della v0.4.1.

---

## v0.4 - 2026-05-21

### English

Security and usability release focused on URL/e-mail/dApp checks, quick actions and startup disclaimer.

#### Added

- Renamed **Link/dApp Check** to **Check URL / e-mail / dApp**.
- Preliminary e-mail address risk check.
- URL input validation for `https://`, `http://` and `www.` formats.
- URLScan quick action for checked domains.
- Bilingual startup disclaimer with accept/reject flow.
- Custom MolinaCrypto-style desktop logo.

#### Fixed and improved

- Fixed VirusTotal URL quick action by using the correct URL identifier.
- Fixed URLScan search query generation.
- Improved Signature / Approval Check scoring for incomplete, random or non-interpretable input.
- Removed generic quick-action links when no EVM address is detected in signature text.
- Added direct Revoke.cash and Etherscan links when an EVM address is detected.
- Improved clarity of warning and limitation messages.

### Italiano

Release di sicurezza e usabilità dedicata ai controlli URL, e-mail, dApp, azioni rapide e disclaimer iniziale.

#### Aggiunto

- Rinominata la sezione **Link/dApp Check** in **Check URL / e-mail / dApp**.
- Controllo preliminare degli indirizzi e-mail.
- Validazione degli URL nei formati `https://`, `http://` e `www.`.
- Azione rapida URLScan per i domini controllati.
- Disclaimer bilingue all’avvio con scelta Accetta/Rifiuta.
- Logo desktop in stile MolinaCrypto.

#### Corretto e migliorato

- Corretto il link rapido VirusTotal usando l’identificativo URL corretto.
- Corretta la generazione della ricerca URLScan.
- Migliorato lo scoring del Signature / Approval Check per input incompleti, casuali o non interpretabili.
- Rimossi i link rapidi generici quando nel testo firma non viene rilevato un address EVM.
- Aggiunti link diretti Revoke.cash ed Etherscan quando viene rilevato un address EVM.
- Migliorata la chiarezza dei messaggi di avviso e dei limiti del controllo.

---

## v0.3 - 2026-05-18

### English

Maintenance release focused on cross-platform layout stability, especially for Windows display scaling.

#### Fixed

- Added scrollable left control panel.
- Fixed layout issues on Windows where the Signature / Approval Check area could be cut off.
- Fixed footer visibility with Resources and molinacrypto.eu buttons.
- Fixed Quick actions panel visibility on smaller windows or scaled displays.
- Improved usability on screens with different DPI/scaling settings.

### Italiano

Release di manutenzione dedicata alla stabilità grafica multipiattaforma, soprattutto su Windows con scaling/display diversi.

#### Corretto

- Aggiunta colonna sinistra scrollabile.
- Corretti problemi di layout su Windows dove la sezione Signature / Approval Check poteva risultare tagliata.
- Corretta la visibilità del footer con i pulsanti Risorse e molinacrypto.eu.
- Corretta la visibilità del pannello Azioni rapide su finestre più piccole o display scalati.
- Migliorata l’usabilità su schermi con impostazioni DPI/scaling differenti.
