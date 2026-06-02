import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent.orchestrator import run_agent


def main():
    with open(ROOT / "data" / "eval" / "agent_scenarios.json", "r", encoding="utf-8") as f:
        scenarios = json.load(f)

    passed = 0
    total = len(scenarios)

    for scenario in scenarios:
        state = run_agent(scenario["query"])
        ok = state.intent.value == scenario["expected_intent"]
        status = "PASS" if ok else "FAIL"
        print(
            f"{status} | {scenario['name']} | expected={scenario['expected_intent']} | got={state.intent.value}"
        )
        if ok:
            passed += 1

    print(f"\nPassed {passed}/{total}")


if __name__ == "__main__":
    main()
