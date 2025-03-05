# Packet-Parsing-Software
### Software for Parsing and Analyzing Packets from Ethernet
###
## Install Software
### - Anaconda3 or Miniconda3
### - Anaconda Prompt
###
## Anaconda Prompt
### 1. Create Virtual Environment
```
conda create -n "yourEnvName" pyinstaller pip
```
### 2. Activate Environment
```
conda activate "yourEnvName"
```
### 3. Install scapy, six 
```
(yourEnvName) pip install scapy, six
```
### 4. Build Pyinstaller
```
(yourEnvName) cd "yourDirectory"
(yourEnvName) pyinstaller PPS.spec
```
### 5. Find your output on dist folder
###