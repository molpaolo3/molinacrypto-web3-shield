MolinaCrypto Web3 Shield v0.5
Linux/source package

MolinaCrypto Web3 Shield is an open source desktop tool for preliminary security and awareness checks on wallets, Bitcoin transactions, URLs, e-mails, dApps, smart contracts, Web3 signatures/approvals and Lightning-related data.

The program does not ask for seed phrases, private keys, passwords or wallet connection. It does not sign transactions and does not move funds. It only works with public data or text manually pasted by the user.

Project website:
https://www.molinacrypto.eu


LINUX REQUIREMENTS

Python 3 and Tkinter are required.

On Linux Mint / Ubuntu / Debian:

sudo apt update
sudo apt install python3 python3-tk


QUICK START

From the program folder:

python3 MolinaCryptoWeb3Shield.py

If the avvia.sh script is included:

chmod +x avvia.sh
./avvia.sh


WHAT IS NEW IN VERSION 0.5

Version 0.5 introduces a cleaner and more scalable tab-based interface:

- Wallet & TX
- Web Risk
- Lightning

This avoids cluttering the first screen and prepares the program for future feature expansion.


WALLET & TX SECTION

Wallet / Address Check:
- Bitcoin address recognition;
- public Bitcoin address check via mempool.space;
- confirmed balance;
- unconfirmed/mempool balance;
- confirmed and unconfirmed transaction count;
- recommended fee snapshot;
- Ethereum/EVM address recognition;
- quick actions for Etherscan, Revoke.cash, BaseScan, PolygonScan and Arbiscan.

Bitcoin TX Check:
- public Bitcoin TXID check;
- confirmed/unconfirmed transaction status;
- block height and block time when available;
- inputs and outputs;
- total output amount;
- fee and estimated fee rate in sat/vB;
- quick links to mempool.space and Blockstream.


WEB RISK SECTION

Check URL / e-mail / dApp:
- URL validation for https://, http:// and www. formats;
- preliminary suspicious e-mail check;
- detection of common phishing/Web3 scam words;
- possible brand/domain impersonation indicators;
- warnings for missing HTTPS, IP-based hosts, punycode and long domains;
- fixed quick actions for VirusTotal, URLScan, Google Search and link opening.

Smart Contract Check:
- EVM address recognition;
- warning that a valid address format does not guarantee contract safety;
- quick links to major explorers and Revoke.cash.

Signature / Approval Check:
- detection of risky keywords such as approve, setApprovalForAll, permit, permit2, eth_sign, transferFrom, safeTransferFrom;
- improved scoring for random, incomplete or non-interpretable text;
- direct Revoke.cash and Etherscan links when an EVM address is detected in the pasted text;
- no useless generic quick links when no EVM address is detected.


LIGHTNING SECTION

Lightning Invoice / LNURL Check:
- local BOLT11 Lightning invoice decoding where supported;
- invoice network detection;
- amount, creation time, expiry time, description and payment hash when available;
- expired invoice warning;
- amountless invoice warning;
- missing description warning;
- LNURL decoding;
- LNURL endpoint check;
- Lightning Address check through the standard /.well-known/lnurlp/ endpoint;
- warning for LNURL-auth/login flows;
- warning for non-HTTPS endpoints.


EXTERNAL SERVICES

Depending on the selected check, the program may query or open external services, including:

- mempool.space;
- Blockstream explorer;
- Etherscan;
- Revoke.cash;
- BaseScan;
- PolygonScan;
- Arbiscan;
- VirusTotal;
- URLScan;
- Google Search;
- public Lightning Address / LNURL endpoints.

The user remains responsible for deciding whether querying or opening such services is appropriate in their context.


LIMITATIONS

The program provides an indicative score based on static checks, public data and heuristic indicators.

It does not guarantee that a wallet, URL, contract, signature, transaction, invoice or LNURL is safe. It does not identify the real owner of an address and does not verify identity, economic intent or completed Lightning payments.

Lightning is off-chain: the tool can inspect invoices, LNURLs and Lightning Address endpoints before the user acts, but it cannot universally confirm whether a Lightning payment has been completed.


DISCLAIMER

This tool is intended for informational, educational and security awareness purposes only. It does not provide financial, tax, legal, investment or professional cybersecurity advice. The user remains responsible for any operational decision.


FILES INCLUDED IN THE LINUX/SOURCE PACKAGE

- MolinaCryptoWeb3Shield.py
- README.md
- README_IT.txt
- README_EN.txt
- CHANGELOG.md
- LICENSE
- requirements.txt
- avvia.sh


WEBSITE AND RESOURCES

Website:
https://www.molinacrypto.eu

Resources:
https://www.molinacrypto.eu/risorse.html
