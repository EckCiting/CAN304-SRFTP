## Install requirements:

```python
pip3 install -r requirements.txt
```



## Help: 

python SR-FTP.py -h



## Example:

Server start (in server folder): 

```bash
python Server.py
```

Client usage (in client folder): 

```bash
python SR-FTP.py -u ftpuser -p nopassword -f hello.txt -s 127.0.0.1
```



## Config:

**PRE_DEFINED_KEY**:  32 char (256 bit) key

​	for encrypting and decrypting the username, password, and filename. 

​	The two sides should define the same pre-defined key.



**PORT:**  define a port for TCP communication.

​	The two sides should use the same TCP port.



**USERS:** define FTP users for the FTP server 

```python
USERS: [
	['username', 'password'] 
]
```

