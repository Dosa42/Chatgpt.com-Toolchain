"""Execute test through the shared runner-only infrastructure."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

def execute(context):
    from shared.cargo import execute as operation
    operation(context)

if __name__ == "__main__":
    from shared.run import main
    raise SystemExit(main(forced_task="test"))
