# BitcoinScripting

Team Members:
Nandan K Prasad - 230051012

Srikanth Ravi Jois - 230002071

Sai Abhilash Dash - 230005041

## Objective

This project aims to explore Bitcoin scripting by creating and validating transactions using Legacy (P2PKH) and SegWit (P2SH-P2WPKH) address formats. We will write scripts in Python (or C) to interact with bitcoind, create transactions, and analyze Bitcoin scripts.

## Tools & Dependencies
### Requirements
- Bitcoin Core (bitcoind) – A full node implementation of Bitcoin

- Bitcoin CLI (bitcoin-cli) – Command-line tool to interact with Bi- tcoin Core

- Bitcoin Debugger – To validate and decode scripts

- Python – For scripting and RPC interaction

### Python Dependencies 

Install dependencies via pip: 

``` pip install python-bitcoinlib ```

```pip install requests```

## Setup and Execution

- Edit the ```newb.conf``` file
- Start bitcoind.exe in regtest mode

  ``` bitcoind -conf="path/to/conf/file" -regtest ```
- Verify connection using bitcoin cli

  ``` bitcoin-cli -regtest getblockchaininfo ```
- Run the ```Intro to Blockchain A2 (Legacy).py``` and ```Intro to Blockchain A2 (SegWit).py``` files

