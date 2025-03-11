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
conda create -n 'yourEnvName' pyinstaller pip psutil pyqt
```
### 2. Activate Environment
```
conda activate 'yourEnvName'
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

'''

data [0:4] = "RTPS"
16바이트 = submsg ID : 0x03 일때
flag last bit=0 (big endian)/b=1 (little endian)
data 길이는 
while문 쓸수밖에...

''''