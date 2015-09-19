import os, fnmatch
import subprocess
import getpass
import pexpect


def get_cert_dirs():
    certs_dbs = []
    moz_dir = os.path.join(os.path.expanduser("~"), ".mozilla")
    for root, dirname, filenames in os.walk(moz_dir):
        for filename in fnmatch.filter(filenames, 'cert8.db'):
	    certs_dbs.append(root)
    return certs_dbs

def parse_certs(certs):
    parsed = []
    for cert in certs:
        if cert[0] != "-":
            continue
        parsed.append(cert)
    return parsed

if __name__ == "__main__":
    certs = []
    for cert_db_folder in get_cert_dirs():
        escaped = cert_db_folder.replace(" ", "\\ ")
        c = pexpect.spawn("certutil -L -a -n" + "\"" + getpass.getuser() + "@mit.edu\" -d" + escaped)
        certs.append(c.read())
    #    with open("".join(["/tmp/","tmpcert",str(i),".cer"]), "w") as fout:
    #        fout.write(cert)
 
    parsed = parse_certs(certs)
    if len(parsed) == 0:
        print "Couldn't find your certs. Please open firefox and set up your MIT certificates"
        exit(0)

    with open("/tmp/tmp_client_cert.cer", "w") as fout:
        fout.write(parse_certs(certs)[0])

    pexpect.spawn("openssl genrsa -out /tmp/hackmitkey.key 768")

    print open("/tmp/hackmitkey.key").read()

    c = pexpect.spawn("openssl x509 -in /tmp/tmp_client_cert.cer -signkey /tmp/hackmitkey.key")

    print c.read()
  
