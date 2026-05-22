MolinaCrypto Web3 Shield
Version: 0.4.1
Author: Paolo Molina
Website: https://www.molinacrypto.eu

============================================================
ENGLISH GUIDE - PROGRAM USAGE
============================================================

MolinaCrypto Web3 Shield is an open source desktop program designed to help crypto and Web3 users check wallets, public addresses, suspicious links, smart contracts and signature requests.

The program is designed for normal users, not only technical users.

It helps answer practical questions such as:

- Does this wallet address look formally correct?
- Could this Web3 link be suspicious?
- Is this smart contract/EVM address at least in the correct format?
- Does this Web3 signature contain risky words such as approve, permit or setApprovalForAll?
- Where can I quickly check approvals, explorers and public information?


Latest version: v0.4.1

Version 0.4.1 includes all v0.4 improvements and fixes startup disclaimer focus handling on Windows.
See CHANGELOG.md for full release notes.


============================================================
SECURITY PRINCIPLE
============================================================

The program does NOT ask for seed phrases.
The program does NOT ask for private keys.
The program does NOT ask for passwords.
The program does NOT connect to wallets.
The program does NOT sign transactions.
The program does NOT move funds.
The program does NOT custody cryptocurrency.
The program does NOT create wallets.

The program only works with:

- public addresses;
- links pasted by the user;
- public smart contracts/addresses;
- technical text manually pasted by the user;
- publicly available online data.

NEVER ENTER:

- seed phrases;
- private keys;
- passwords;
- 2FA codes;
- recovery phrases;
- banking data;
- sensitive personal data.

If you accidentally pasted a seed phrase or private key into any program, website, chat or online form, consider that wallet potentially compromised.

============================================================
LINUX REQUIREMENTS
============================================================

This version requires Python 3.

Check whether Python 3 is installed:

python3 --version

If Python 3 is not installed, on Linux Mint / Ubuntu / Debian you can install it with:

sudo apt update
sudo apt install python3

The program uses standard Python libraries.
No additional pip installation is required.

============================================================
HOW TO START THE PROGRAM ON LINUX
============================================================

Open the terminal inside the program folder.

Example:

cd /home/aka/SITO/Programma/molinacrypto-web3-shield

Make the launcher executable:

chmod +x avvia.sh

Start the program:

./avvia.sh

Alternatively, you can run the Python file directly:

python3 MolinaCryptoWeb3Shield.py

On some Linux file managers, you can double click avvia.sh and choose “Run”.

============================================================
WINDOW STRUCTURE
============================================================

When you open MolinaCrypto Web3 Shield you will see:

ON THE LEFT:
1. Wallet / Address Check
2. Link / dApp Check
3. Smart Contract Check
4. Signature / Approval Check

ON THE RIGHT:
- Result panel;
- Quick actions panel;
- buttons to export report, clear, open website and resources.

TOP RIGHT:
- IT/EN language selector.

============================================================
1. WALLET / ADDRESS CHECK
============================================================

This section checks a public Bitcoin or Ethereum/EVM address.

Field to use:

Wallet / Address Check

What you can paste:

- public Bitcoin address;
- public Ethereum address;
- compatible public EVM address.

Ethereum/EVM example:

0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe

Bitcoin example:

bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh

Button to press:

Analyze wallet

------------------------------------------------------------
IF YOU ENTER A BITCOIN ADDRESS
------------------------------------------------------------

The program tries to read public data through mempool.space.

It shows:

- recognized Bitcoin format;
- confirmed balance;
- unconfirmed/mempool balance;
- number of confirmed transactions;
- number of unconfirmed transactions;
- estimated Bitcoin fee;
- risk/caution score;
- quick buttons to explorers.

Available quick actions:

- Mempool.space;
- Blockstream.

What they do:

Mempool.space:
opens the Bitcoin address on the mempool.space explorer.

Blockstream:
opens the Bitcoin address on the Blockstream explorer.

Note:
Bitcoin data is public and comes from public APIs. If the API does not respond or there is no Internet connection, the program may show an API error but still provides explorer links.

------------------------------------------------------------
IF YOU ENTER AN ETHEREUM / EVM ADDRESS
------------------------------------------------------------

The program recognizes the Ethereum/EVM format.

It shows:

- valid Ethereum/EVM format;
- explanation of the main risk;
- recommendation to check approvals and interactions;
- risk/caution score;
- quick buttons to explorers and useful tools.

Available quick actions:

- Etherscan;
- Revoke.cash;
- BaseScan;
- PolygonScan;
- Arbiscan.

What they do:

Etherscan:
opens the address on Ethereum.

Revoke.cash:
opens the page to check possible approvals.

BaseScan:
opens the address on Base.

PolygonScan:
opens the address on Polygon.

Arbiscan:
opens the address on Arbitrum.

Note:
In this version the program does not automatically read EVM balances and tokens, but it opens the correct tools with one click.

============================================================
2. LINK / dAPP CHECK
============================================================

This section checks a suspicious Web3 link.

Field to use:

Link / dApp Check

What you can paste:

- dApp link;
- claim page;
- mint page;
- airdrop page;
- website asking to connect a wallet;
- link received via Telegram, Discord, X, Threads, Facebook, email or private message;
- sponsored link that looks related to crypto/wallets.

Test example:

https://metamask-claim-airdrop-verify-wallet.example.com

Button to press:

Check link

------------------------------------------------------------
WHAT THE PROGRAM CHECKS
------------------------------------------------------------

The program checks static link indicators, for example:

- presence or absence of HTTPS;
- very long domain;
- many hyphens in the domain;
- IP address instead of readable domain;
- suspicious words such as claim, airdrop, verify, wallet, seed, restore, recover;
- known brand names inside domains that do not look official;
- possible deceptive domain patterns.

------------------------------------------------------------
RESULT
------------------------------------------------------------

The program returns:

- check type: WEB3 LINK / DAPP;
- score;
- risk level;
- recommendation;
- detected indicators;
- check limitation.

------------------------------------------------------------
AVAILABLE QUICK ACTIONS
------------------------------------------------------------

Open link:
opens the link in the browser. Use with caution if risk is high.

Google search:
searches the domain on Google.

VirusTotal URL:
opens the link search on VirusTotal.

------------------------------------------------------------
IMPORTANT NOTE
------------------------------------------------------------

The link check is static.

The program does NOT actually visit the website.
The program does NOT analyze JavaScript.
The program does NOT guarantee that a website is safe.
The program does NOT guarantee that a website is dangerous.

It is a first prudential filter.

If the result is medium or high risk, do not connect your main wallet.

============================================================
3. SMART CONTRACT CHECK
============================================================

This section checks the format of a smart contract or EVM address.

Field to use:

Smart Contract Check

What you can paste:

- Ethereum/EVM smart contract address;
- EVM address to verify;
- contract copied from a dApp;
- address found on a Web3 page.

Test example:

0x0000000000000000000000000000000000000000

Button to press:

Check contract

------------------------------------------------------------
WHAT THE PROGRAM DOES
------------------------------------------------------------

The program verifies whether the inserted data has a valid Ethereum/EVM format.

If the format is valid, it shows a prudential recommendation.

Warning:
a formally valid EVM address does NOT mean that the contract is safe.

------------------------------------------------------------
WHAT YOU SHOULD MANUALLY CHECK
------------------------------------------------------------

On explorers you should verify:

- verified or unverified contract;
- proxy presence;
- active owner;
- admin functions;
- pause functions;
- blacklist functions;
- mint functions;
- upgrade functions;
- withdraw functions;
- interaction history;
- consistency with the official project website.

------------------------------------------------------------
AVAILABLE QUICK ACTIONS
------------------------------------------------------------

Etherscan:
opens the address on Ethereum.

Revoke.cash:
opens the approval checker.

BaseScan:
opens the address on Base.

PolygonScan:
opens the address on Polygon.

Arbiscan:
opens the address on Arbitrum.

------------------------------------------------------------
CHECK LIMITATION
------------------------------------------------------------

In this version the program does not decompile bytecode.
It does not automatically analyze source code.
It does not assign full on-chain reputation.

It works as a preliminary check and as a shortcut to the right tools.

============================================================
4. SIGNATURE / APPROVAL CHECK
============================================================

This section prudentially interprets Web3 signature requests.

Field to use:

Signature / Approval Check

What you can paste:

- signature text;
- approve request;
- permit request;
- setApprovalForAll request;
- technical text copied from a wallet;
- payload copied from a dApp;
- message you do not understand before signing.

Test example:

setApprovalForAll true operator 0x0000000000000000000000000000000000000000

Button to press:

Translate signature

------------------------------------------------------------
WHAT THE PROGRAM LOOKS FOR
------------------------------------------------------------

The program looks for potentially sensitive words and functions, including:

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
- possible unlimited approvals;
- EVM addresses inside the text.

------------------------------------------------------------
PRACTICAL MEANING OF SOME ITEMS
------------------------------------------------------------

setApprovalForAll:
may authorize an operator to manage all tokens/NFTs in a collection. This is highly sensitive.

approve:
may authorize a spender to move tokens from the wallet.

increaseAllowance:
may increase the amount of tokens a spender can move.

permit:
may grant permissions through a signature without a classic on-chain approve transaction.

permit2:
powerful authorization mechanism. Check spender, token, limits and expiry.

eth_sign:
blind/legacy signature. It can be risky if the content is not readable.

personal_sign:
often used for login, but it can still be abused on malicious websites.

transferFrom / safeTransferFrom:
may indicate operations related to moving assets or NFTs.

------------------------------------------------------------
PRACTICAL RULE
------------------------------------------------------------

If you do not clearly understand:

- requesting website;
- domain;
- spender;
- token;
- amount;
- expiry;
- reason for signing;

DO NOT sign.

------------------------------------------------------------
AVAILABLE QUICK ACTIONS
------------------------------------------------------------

Revoke.cash:
opens the tool to check/revoke approvals.

Etherscan Token Approval:
opens the token approval checker on Etherscan.

------------------------------------------------------------
CHECK LIMITATION
------------------------------------------------------------

The program interprets text and keywords.
It does not actually simulate the transaction.
It does not replace a wallet simulator.
It cannot guarantee that a signature is safe or dangerous.

It works as a prudential translator to help you understand when to stop.

============================================================
RESULT PANEL
============================================================

The Result panel shows:

- Type;
- Score;
- risk level;
- recommended action;
- detected indicators;
- check limitation.

The score ranges from 0 to 100.

As a general indication:

80 - 100:
low risk in the static check.

55 - 79:
medium risk, caution required.

0 - 54:
high risk, proceed with strong caution or do not proceed.

The score is NOT a safety guarantee.
It is an informational indicator.

============================================================
QUICK ACTIONS
============================================================

The Quick actions section changes depending on the performed check.

Examples:

For Bitcoin:
- Mempool.space;
- Blockstream.

For Ethereum/EVM:
- Etherscan;
- Revoke.cash;
- BaseScan;
- PolygonScan;
- Arbiscan.

For links:
- Open link;
- Google search;
- VirusTotal URL.

For signatures:
- Revoke.cash;
- Etherscan Token Approval.

The buttons open the browser and take you directly to the useful page.

============================================================
GENERAL BUTTONS
============================================================

Export .txt report:
saves the current result into a text file.

Clear:
clears the fields and resets the result.

molinacrypto.eu:
opens the official website.

Resources:
opens the website resources page.

EN / IT:
switches the interface language.

============================================================
RIGHT-CLICK MENU
============================================================

In the program fields you can right-click to:

- Cut;
- Copy;
- Paste;
- Select all.

This is useful for easily pasting addresses, links, contracts and signatures.

============================================================
WHAT YOU SHOULD NOT EXPECT FROM THE PROGRAM
============================================================

MolinaCrypto Web3 Shield is not an antivirus.
It is not a wallet.
It is not a fund custody tool.
It is not an investment service.
It is not a smart contract audit.
It is not professional cybersecurity advice.
It is not financial, tax or legal advice.

It is an informational, educational and prudential tool.

============================================================
DISCLAIMER
============================================================

MolinaCrypto Web3 Shield is provided for informational and educational purposes only.

It does not constitute financial, tax, legal, investment or professional cybersecurity advice.

The user remains responsible for their own decisions, official-source verification and wallet usage.

============================================================
LICENSE
============================================================

MIT License.

Project connected to:
https://www.molinacrypto.eu
