import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent.orchestrator import run_agent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", type=str, help="User support question")
    args = parser.parse_args()

    state = run_agent(args.query)
    print(state.final_response)


if __name__ == "__main__":
    main()
