# AirDrop-For-Windows
This Program Helps You To Transfer Files From Windows To Mac And Vice-Versa

## Requirements:
```
Python3
Tkinter
Socket
```

## Usage:
```
Both the PC's should be connected to the same network.
If both the PCs are running on Windows then download the Windows version of AirDrop for both the PCs and run it using python.
If one is running on Mac and the other on Windows then download the Mac version for Mac and Windows version for Windows respectively.
```

## Screenshots:

### macOS
![](https://raw.github.com/rohit25-1/AirDrop-For-Windows/master/Screenshots/ss_mac.png)

### Windows
![](https://raw.github.com/rohit25-1/AirDrop-For-Windows/master/Screenshots/ss_windows.jpeg)

## Setting Up The Program:
```
1. On line number 29 replace the '<Enter The IP Adddress of Your sending machine>' with the IPv4 address of your current PC.
2. On line number 48 replace the '<Enter the IP address of receiving machine>' with the IPv4 address of the other PC.
3. On line number 52 replace the '<NAME OF THE USER ON YOUR PC>' with the username of your PC.
3. Do these steps on both the PC's to set-up your python script.
```

##Usage:
```
1. Open the script on both the PC's using the command - $python3 airdrop_for_mac.py or $python airdrop_windows.py 
2. Click on the open button on the 'SENDERS PC' to open the file which you want to send.
3. Click on the send button.
4. Click on the receive button on the 'RECEIVING PC'.
5. Wait till the file gets transferred.
6. A pop-up will appear on the 'SENDERS PC' when the file is transferred. Click on the OK button.
7. A pop-up will appear on the 'RECEIVING PC' when the file is transferred. Click on the OK button.
8. The file will be stored in the Downloads Folder of your PC.

```
## PLEASE REPORT IF YOU ENCOUNTER ANY BUGS
