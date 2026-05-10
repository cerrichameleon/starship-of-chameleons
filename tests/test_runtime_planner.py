from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory

from starship_protocol.runtime import build_runtime
from starship_protocol.runtime_planner import RuntimePlanner


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


@contextmanager
def temporary_provider_env() -> None:
    names = ["OPENAI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY"]
    previous = {name: os.environ.get(name) for name in names}
    os.environ["OPENAI_API_KEY"] = "sk-test-openai"
    os.environ.pop("GEMINI_API_KEY", None)
    os.environ.pop("GOOGLE_API_KEY", None)
    try:
        yield
    finally:
        for name, value in previous.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


def test_runtime_planner_instantiates_brained_crew_from_proposal() -> None:
    with temporary_provider_env(), TemporaryDirectory() as temporary_directory:
        runtime = build_runtime(base_path=Path(temporary_directory))
        planner = RuntimePlanner(runtime)
        proposal = runtime.captain_console.draft_crew_proposal(
            "Create a small software game studio with a software project manager, a scrum master, a ui coder, and a backend coder."
        )

        result = planner.instantiate_from_proposal(proposal)

        assert_true(len(result.instantiated_roles) >= 1, "planner should instantiate at least one role")
        assert_true(all(role["has_brain"] for role in result.instantiated_roles), "all instantiated crew should have brains")
        assert_true(proposal.approval_status == "instantiated", "proposal should move to instantiated state")


def main() -> None:
    tests = [test_runtime_planner_instantiates_brained_crew_from_proposal]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS all {len(tests)} runtime planner tests")


if __name__ == "__main__":
    main()
