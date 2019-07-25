import shlex
from subprocess import Popen
from typing import List


def shell(cmd) -> Popen:
    print(cmd)
    # return subprocess.check_output(cmd, shell=True)
    return Popen(shlex.split(cmd), shell=True)


def wait_all(processes: List[Popen]):
    for _ in processes:
        _.wait()
