"""Try to break out of the agent's sandbox, and report what worked.

    uv run python tests/test_sandbox.py

Each case is a small Python script run exactly the way the agent runs its own
scripts (Workspace.run_python). The script prints "SUCCEEDED" if its action
worked; otherwise the sandbox raised an error. Every case says whether we
EXPECT it to be allowed or blocked. The run folder is kept afterwards
(runs/sandbox-test-*/) so you can inspect the scripts and outputs.
"""

import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import agent  # noqa: E402

ENV_FILE = ROOT / ".env"
HOME = Path.home()
# Two tiny made-up datasets: the test run uses study_a; study_b stands in for another dataset.
FIXTURES = ROOT / "tests" / "fixtures"

# (description, expected, code). Each code snippet tries one thing.
CASES = [
    # --- things the agent's scripts SHOULD be able to do
    ("read a data file", "allowed",
     "open('data/raw_timing.csv').read()"),
    ("write a file in the run folder", "allowed",
     "open('results.csv', 'w').write('a,b\\n1,2\\n')"),
    ("import pandas", "allowed",
     "import pandas"),
    ("pandas: load a CSV from data/", "allowed",
     "import pandas as pd; pd.read_csv('data/raw_timing.csv')"),
    ("scipy: run a t-test", "allowed",
     "import numpy as np, scipy.stats as st; st.ttest_ind(np.arange(10), np.arange(10) + 1)"),
    ("multiprocessing: run a 2-worker pool", "allowed",
     "import multiprocessing as mp\nif __name__ == '__main__':\n    with mp.Pool(2) as p: p.map(abs, [-1, -2])"),
    ("look up the current user name", "allowed",
     "import getpass; getpass.getuser()"),

    # --- reading things outside the sandbox
    ("read the project's .env (API key)", "blocked",
     f"open({str(ENV_FILE)!r}).read()"),
    ("read agent.py in the project folder", "blocked",
     f"open({str(ROOT / 'agent.py')!r}).read()"),
    ("read ~/.zshrc", "blocked",
     f"open({str(HOME / '.zshrc')!r}).read()"),
    ("list files in your home folder", "blocked",
     f"import os; os.listdir({str(HOME)!r})"),
    ("list files in the project folder", "blocked",
     f"import os; os.listdir({str(ROOT)!r})"),
    ("list files in the folder above the project", "blocked",
     f"import os; os.listdir({str(ROOT.parent)!r})"),
    ("list files in ~/.local (on the way to Python)", "blocked",
     f"import os; os.listdir({str(HOME / '.local')!r})"),

    # --- writing outside the run folder
    ("read a file in another dataset", "blocked",
     f"open({str(FIXTURES / 'study_b' / 'other.csv')!r}).read()"),
    ("list the other datasets", "blocked",
     f"import os; os.listdir({str(FIXTURES)!r})"),
    ("write into data/", "blocked",
     "open('data/new.txt', 'w').write('x')"),
    ("write into the project folder", "blocked",
     f"open({str(ROOT / 'new.txt')!r}, 'w').write('x')"),
    ("write to /tmp", "blocked",
     "open('/tmp/agent-test.txt', 'w').write('x')"),

    # --- sneakier routes to the .env file
    ("symlink to .env, then read the link", "blocked",
     f"import os; os.symlink({str(ENV_FILE)!r}, 'link.env'); open('link.env').read()"),
    ("hard link to .env, then read the link", "blocked",
     f"import os; os.link({str(ENV_FILE)!r}, 'hard.env'); open('hard.env').read()"),
    ("run a shell command: cat .env", "blocked",
     f"import subprocess; subprocess.run(['cat', {str(ENV_FILE)!r}], check=True, capture_output=True)"),
    ("find the API key in environment variables", "blocked",
     "import os; assert 'OPENROUTER_API_KEY' in os.environ"),

    # --- app-to-app requests and launching other programs
    ("start Python in a subprocess", "allowed",
     "import subprocess, sys; subprocess.run([sys.executable, '-c', 'pass'], check=True)"),
    ("run a harmless program (/usr/bin/true)", "blocked",
     "import subprocess; subprocess.run(['/usr/bin/true'], check=True)"),
    ("run AppleScript (osascript)", "blocked",
     "import subprocess; subprocess.run(['osascript', '-e', 'return 1'], check=True, capture_output=True)"),
    ("open an app with the `open` command", "blocked",
     "import subprocess; subprocess.run(['/usr/bin/open', '-g', '-a', 'Calculator'], check=True, capture_output=True)"),
    # Calls macOS's app launcher directly from Python, with no subprocess. If this
    # isn't blocked, Calculator opens.
    ("open an app from Python via LaunchServices", "blocked", """
import ctypes
cf = ctypes.CDLL('/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation')
ls = ctypes.CDLL('/System/Library/Frameworks/CoreServices.framework/CoreServices')
cf.CFStringCreateWithCString.restype = ctypes.c_void_p
cf.CFStringCreateWithCString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint32]
cf.CFURLCreateWithFileSystemPath.restype = ctypes.c_void_p
cf.CFURLCreateWithFileSystemPath.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_bool]
ls.LSOpenCFURLRef.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
path = cf.CFStringCreateWithCString(None, b'/System/Applications/Calculator.app', 0x08000100)
url = cf.CFURLCreateWithFileSystemPath(None, path, 0, True)
status = ls.LSOpenCFURLRef(url, None)
assert status == 0, 'LaunchServices refused: %d' % status
"""),

    # --- network
    ("download a web page", "blocked",
     "import urllib.request; urllib.request.urlopen('https://example.com', timeout=5)"),
    ("open a raw network socket", "blocked",
     "import socket; socket.create_connection(('1.1.1.1', 443), timeout=5)"),
]


def main():
    run_dir = ROOT / "runs" / ("sandbox-test-" + dt.datetime.now().strftime("%Y%m%d-%H%M%S"))
    ws = agent.Workspace(run_dir, FIXTURES / "study_a")
    failures = 0
    for i, (desc, expected, code) in enumerate(CASES, 1):
        script = code + "\nprint('SUCCEEDED')"
        output = ws.run_python("case{:02d}".format(i), script)
        actual = "allowed" if "SUCCEEDED" in output else "blocked"
        ok = actual == expected
        failures += not ok
        print("{}  {:<45} expected {:<8} got {}".format("PASS" if ok else "FAIL", desc, expected, actual))
    print("\n{} of {} cases behaved as expected.".format(len(CASES) - failures, len(CASES)))
    print("Scripts and outputs kept in", run_dir.relative_to(ROOT))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
