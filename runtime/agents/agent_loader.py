from pathlib import Path


BASE = Path(__file__).resolve().parent.parent.parent
AGENTS_DIR = BASE / "agents"


def load_agent_instructions(agent_name: str) -> str:
    agent_file = AGENTS_DIR / f"{agent_name}.md"

    if not agent_file.exists():
        raise FileNotFoundError(f"Agent definition not found: {agent_file}")

    return agent_file.read_text(encoding="utf-8")