MolinaCrypto Web3 Shield
Versione: 0.4.1
Autore: Paolo Molina
Sito: https://www.molinacrypto.eu

============================================================
GUIDA ITALIANA - USO DEL PROGRAMMA
============================================================

MolinaCrypto Web3 Shield è un programma desktop open source pensato per aiutare utenti crypto e Web3 a controllare wallet, indirizzi pubblici, link sospetti, smart contract e richieste di firma.

Il programma è pensato per utenti normali, non solo per tecnici.

Serve a rispondere a domande pratiche come:

- Questo indirizzo wallet sembra formalmente corretto?
- Questo link Web3 può essere sospetto?
- Questo smart contract/address EVM è almeno nel formato corretto?
- Questa firma Web3 contiene parole pericolose come approve, permit o setApprovalForAll?
- Dove posso controllare rapidamente approvals, explorer e informazioni pubbliche?


Ultima versione: v0.4.1

La versione 0.4.1 include tutte le migliorie della v0.4 e corregge la gestione del focus del disclaimer iniziale su Windows.
Per i dettagli completi consultare CHANGELOG.md.


============================================================
PRINCIPIO DI SICUREZZA
============================================================

Il programma NON chiede seed phrase.
Il programma NON chiede private key.
Il programma NON chiede password.
Il programma NON collega il wallet.
Il programma NON firma transazioni.
Il programma NON sposta fondi.
Il programma NON custodisce criptovalute.
Il programma NON crea wallet.

Il programma lavora solo con:

- indirizzi pubblici;
- link incollati dall’utente;
- smart contract/address pubblici;
- testo tecnico incollato manualmente dall’utente;
- dati pubblici disponibili online.

NON INSERIRE MAI:

- seed phrase;
- private key;
- password;
- codici 2FA;
- recovery phrase;
- dati bancari;
- dati personali sensibili.

Se hai incollato per errore una seed phrase o una private key in qualsiasi programma, sito, chat o form online, considera quel wallet potenzialmente compromesso.

============================================================
REQUISITI LINUX
============================================================

Per usare questa versione serve Python 3.

Verifica se Python 3 è installato:

python3 --version

Se Python 3 non è installato, su Linux Mint / Ubuntu / Debian puoi installarlo con:

sudo apt update
sudo apt install python3

Il programma usa librerie standard di Python.
Non servono installazioni aggiuntive con pip.

============================================================
COME AVVIARE IL PROGRAMMA SU LINUX
============================================================

Apri il terminale nella cartella del programma.

Esempio:

cd /home/aka/SITO/Programma/molinacrypto-web3-shield

Rendi eseguibile lo script di avvio:

chmod +x avvia.sh

Avvia il programma:

./avvia.sh

In alternativa puoi avviare direttamente il file Python:

python3 MolinaCryptoWeb3Shield.py

Su alcuni file manager Linux puoi anche fare doppio click su avvia.sh e scegliere “Esegui”.

============================================================
STRUTTURA DELLA FINESTRA
============================================================

Quando apri MolinaCrypto Web3 Shield trovi:

A SINISTRA:
1. Wallet / Address Check
2. Link / dApp Check
3. Smart Contract Check
4. Signature / Approval Check

A DESTRA:
- riquadro Risultato;
- riquadro Azioni rapide;
- pulsanti per esportare report, pulire, aprire sito e risorse.

IN ALTO A DESTRA:
- selezione lingua IT/EN.

============================================================
1. WALLET / ADDRESS CHECK
============================================================

Questa sezione serve per controllare un indirizzo pubblico Bitcoin o Ethereum/EVM.

Campo da usare:

Wallet / Address Check

Cosa puoi incollare:

- indirizzo Bitcoin pubblico;
- indirizzo Ethereum pubblico;
- indirizzo EVM compatibile.

Esempio indirizzo Ethereum/EVM:

0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe

Esempio indirizzo Bitcoin:

bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh

Pulsante da premere:

Analizza wallet

------------------------------------------------------------
SE INSERISCI UN INDIRIZZO BITCOIN
------------------------------------------------------------

Il programma prova a leggere dati pubblici tramite mempool.space.

Mostra:

- formato riconosciuto come Bitcoin;
- saldo confermato;
- saldo non confermato / mempool;
- numero di transazioni confermate;
- numero di transazioni non confermate;
- fee Bitcoin stimata;
- score di rischio/attenzione;
- azioni rapide verso explorer.

Azioni rapide disponibili:

- Mempool.space;
- Blockstream.

A cosa servono:

Mempool.space:
apre l’indirizzo Bitcoin nell’explorer mempool.space.

Blockstream:
apre l’indirizzo Bitcoin nell’explorer Blockstream.

Nota:
i dati Bitcoin sono pubblici e provengono da API pubbliche. Se l’API non risponde o manca Internet, il programma può mostrare un errore ma fornisce comunque i link agli explorer.

------------------------------------------------------------
SE INSERISCI UN INDIRIZZO ETHEREUM / EVM
------------------------------------------------------------

Il programma riconosce il formato Ethereum/EVM.

Mostra:

- formato Ethereum/EVM valido;
- spiegazione del rischio principale;
- raccomandazione di controllare approvals e interazioni;
- score di rischio/attenzione;
- pulsanti rapidi verso explorer e strumenti utili.

Azioni rapide disponibili:

- Etherscan;
- Revoke.cash;
- BaseScan;
- PolygonScan;
- Arbiscan.

A cosa servono:

Etherscan:
apre l’indirizzo su Ethereum.

Revoke.cash:
apre la pagina per controllare eventuali autorizzazioni/approvals.

BaseScan:
apre l’indirizzo sulla rete Base.

PolygonScan:
apre l’indirizzo sulla rete Polygon.

Arbiscan:
apre l’indirizzo sulla rete Arbitrum.

Nota:
in questa versione il programma non legge automaticamente saldo e token EVM, ma apre con un click gli strumenti corretti per controllare manualmente.

============================================================
2. LINK / dAPP CHECK
============================================================

Questa sezione serve per controllare un link Web3 sospetto.

Campo da usare:

Link / dApp Check

Cosa puoi incollare:

- link di una dApp;
- pagina di claim;
- pagina di mint;
- pagina di airdrop;
- sito che chiede di collegare il wallet;
- link ricevuto via Telegram, Discord, X, Threads, Facebook, email o messaggio privato;
- link sponsorizzato che sembra legato a crypto/wallet.

Esempio di test:

https://metamask-claim-airdrop-verify-wallet.example.com

Pulsante da premere:

Controlla link

------------------------------------------------------------
COSA CONTROLLA IL PROGRAMMA
------------------------------------------------------------

Il programma verifica indicatori statici del link, per esempio:

- presenza o assenza di HTTPS;
- dominio molto lungo;
- dominio con molti trattini;
- uso di indirizzo IP al posto di dominio leggibile;
- parole sospette come claim, airdrop, verify, wallet, seed, restore, recover;
- presenza di nomi di brand noti dentro domini che non sembrano ufficiali;
- possibile dominio creato per campagne phishing o truffe Web3.

------------------------------------------------------------
RISULTATO
------------------------------------------------------------

Il programma restituisce:

- tipo di controllo: WEB3 LINK / DAPP;
- score;
- livello di rischio;
- raccomandazione;
- indicatori rilevati;
- limite del controllo.

------------------------------------------------------------
AZIONI RAPIDE DISPONIBILI
------------------------------------------------------------

Apri link:
apre il link nel browser. Usare con cautela se il rischio è alto.

Google search:
cerca il dominio su Google.

VirusTotal URL:
apre la ricerca del link su VirusTotal.

------------------------------------------------------------
NOTA IMPORTANTE
------------------------------------------------------------

Il controllo link è statico.

Il programma NON visita realmente il sito.
Il programma NON analizza JavaScript.
Il programma NON garantisce che un sito sia sicuro.
Il programma NON garantisce che un sito sia pericoloso.

Serve come primo filtro prudenziale.

Se il risultato è rischio medio o alto, non collegare il wallet principale.

============================================================
3. SMART CONTRACT CHECK
============================================================

Questa sezione serve per controllare il formato di uno smart contract o address EVM.

Campo da usare:

Smart Contract Check

Cosa puoi incollare:

- indirizzo smart contract Ethereum/EVM;
- address EVM da verificare;
- contratto copiato da una dApp;
- indirizzo trovato in una pagina Web3.

Esempio di test:

0x0000000000000000000000000000000000000000

Pulsante da premere:

Controlla contratto

------------------------------------------------------------
COSA FA IL PROGRAMMA
------------------------------------------------------------

Il programma verifica se il dato inserito ha formato Ethereum/EVM valido.

Se il formato è valido, mostra una raccomandazione prudenziale.

Attenzione:
un indirizzo EVM formalmente valido NON significa che il contratto sia sicuro.

------------------------------------------------------------
COSA DEVI CONTROLLARE MANUALMENTE
------------------------------------------------------------

Sugli explorer dovresti verificare:

- contratto verificato o non verificato;
- presenza di proxy;
- owner ancora attivo;
- funzioni admin;
- funzioni pause;
- funzioni blacklist;
- funzioni mint;
- funzioni upgrade;
- funzioni withdraw;
- cronologia delle interazioni;
- coerenza con il sito ufficiale del progetto.

------------------------------------------------------------
AZIONI RAPIDE DISPONIBILI
------------------------------------------------------------

Etherscan:
apre l’indirizzo su Ethereum.

Revoke.cash:
apre il controllo approvals.

BaseScan:
apre l’indirizzo su Base.

PolygonScan:
apre l’indirizzo su Polygon.

Arbiscan:
apre l’indirizzo su Arbitrum.

------------------------------------------------------------
LIMITE DEL CONTROLLO
------------------------------------------------------------

In questa versione il programma non decompila il bytecode.
Non analizza automaticamente il codice sorgente.
Non assegna una reputazione on-chain completa.

Serve come controllo preliminare e come scorciatoia verso gli strumenti corretti.

============================================================
4. SIGNATURE / APPROVAL CHECK
============================================================

Questa sezione serve per interpretare in modo prudenziale richieste di firma Web3.

Campo da usare:

Signature / Approval Check

Cosa puoi incollare:

- testo di una firma;
- richiesta approve;
- richiesta permit;
- richiesta setApprovalForAll;
- testo tecnico copiato dal wallet;
- payload copiato da una dApp;
- messaggio che non capisci prima di firmare.

Esempio di test:

setApprovalForAll true operator 0x0000000000000000000000000000000000000000

Pulsante da premere:

Traduci firma

------------------------------------------------------------
COSA CERCA IL PROGRAMMA
------------------------------------------------------------

Il programma cerca parole e funzioni potenzialmente sensibili, tra cui:

- setApprovalForAll;
- approve;
- increaseAllowance;
- permit;
- permit2;
- eth_sign;
- personal_sign;
- eth_signTypedData;
- transferFrom;
- safeTransferFrom;
- possibili approval illimitate;
- indirizzi EVM presenti nel testo.

------------------------------------------------------------
SIGNIFICATO PRATICO DI ALCUNE VOCI
------------------------------------------------------------

setApprovalForAll:
può autorizzare un operatore a gestire tutti i token/NFT di una collezione. È una funzione molto delicata.

approve:
può autorizzare uno spender a muovere token dal wallet.

increaseAllowance:
può aumentare la quantità di token che uno spender può muovere.

permit:
può concedere autorizzazioni tramite firma senza una classica transazione approve on-chain.

permit2:
meccanismo potente di autorizzazione. Controllare spender, token, limiti e scadenza.

eth_sign:
firma cieca/legacy. Può essere rischiosa se il contenuto non è leggibile.

personal_sign:
spesso usata per login, ma può comunque essere abusata su siti malevoli.

transferFrom / safeTransferFrom:
può indicare operazioni collegate allo spostamento di asset o NFT.

------------------------------------------------------------
REGOLA PRATICA
------------------------------------------------------------

Se non capisci chiaramente:

- sito richiedente;
- dominio;
- spender;
- token;
- importo;
- scadenza;
- motivo della firma;

NON firmare.

------------------------------------------------------------
AZIONI RAPIDE DISPONIBILI
------------------------------------------------------------

Revoke.cash:
apre lo strumento per controllare/revocare approvals.

Etherscan Token Approval:
apre il controllo autorizzazioni token su Etherscan.

------------------------------------------------------------
LIMITE DEL CONTROLLO
------------------------------------------------------------

Il programma interpreta testo e parole chiave.
Non simula realmente la transazione.
Non sostituisce un wallet simulator.
Non può garantire che una firma sia sicura o pericolosa.

Serve come traduttore prudenziale per aiutarti a capire quando serve fermarsi.

============================================================
RIQUADRO RISULTATO
============================================================

Il riquadro Risultato mostra:

- Tipo;
- Score;
- livello di rischio;
- azione consigliata;
- indicatori rilevati;
- limite del controllo.

Lo score va da 0 a 100.

Indicativamente:

80 - 100:
rischio basso nel controllo statico.

55 - 79:
rischio medio, serve attenzione.

0 - 54:
rischio alto, procedere con molta prudenza o non procedere.

Lo score NON è una garanzia di sicurezza.
È un indicatore informativo.

============================================================
AZIONI RAPIDE
============================================================

La sezione Azioni rapide cambia in base al controllo effettuato.

Esempi:

Per Bitcoin:
- Mempool.space;
- Blockstream.

Per Ethereum/EVM:
- Etherscan;
- Revoke.cash;
- BaseScan;
- PolygonScan;
- Arbiscan.

Per link:
- Apri link;
- Google search;
- VirusTotal URL.

Per firme:
- Revoke.cash;
- Etherscan Token Approval.

I pulsanti aprono il browser e portano direttamente alla pagina utile.

============================================================
PULSANTI GENERALI
============================================================

Esporta report .txt:
salva il risultato corrente in un file di testo.

Pulisci:
svuota i campi e resetta il risultato.

molinacrypto.eu:
apre il sito ufficiale.

Risorse:
apre la pagina risorse del sito.

EN / IT:
cambia lingua dell’interfaccia.

============================================================
MENU TASTO DESTRO
============================================================

Nei campi del programma puoi usare il tasto destro per:

- Taglia;
- Copia;
- Incolla;
- Seleziona tutto.

Serve per incollare facilmente indirizzi, link, contratti e firme.

============================================================
COSA NON DEVI ASPETTARTI DAL PROGRAMMA
============================================================

MolinaCrypto Web3 Shield non è un antivirus.
Non è un wallet.
Non è un custode di fondi.
Non è un servizio di investimento.
Non è un audit smart contract.
Non è una consulenza professionale di cybersecurity.
Non è una consulenza finanziaria, fiscale o legale.

È uno strumento informativo, educativo e prudenziale.

============================================================
DISCLAIMER
============================================================

MolinaCrypto Web3 Shield è fornito a scopo informativo ed educativo.

Non costituisce consulenza finanziaria, fiscale, legale, di investimento o cybersecurity professionale.

L’utente resta responsabile delle proprie decisioni, delle verifiche su fonti ufficiali e dell’uso dei propri wallet.

============================================================
LICENZA
============================================================

MIT License.

Progetto collegato a:
https://www.molinacrypto.eu
