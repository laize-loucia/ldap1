import socket
import ldap

LDAP_URI = "ldap://localhost"
BASE_DN = "ou=users,dc=miniauth,dc=local"

HOST = "127.0.0.1"
PORT = 5000

def authenticate(username, password):
    dn = f"uid={username},{BASE_DN}"
    try:
        conn = ldap.initialize(LDAP_URI)
        conn.simple_bind_s(dn, password)
        conn.unbind_s()
        return True
    except ldap.INVALID_CREDENTIALS:
        return False
    except ldap.LDAPError as e:
        print(f"LDAP error: {e}")
        return False

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)
    print("Auth daemon listening on port 5000")

    while True:
        conn, addr = s.accept()
        with conn:
            data = conn.recv(1024).decode().strip()
            if ":" not in data:
                conn.sendall(b"KO")
                continue

            user, pwd = data.split(":", 1)
            if authenticate(user, pwd):
                conn.sendall(b"OK")
            else:
                conn.sendall(b"KO")
