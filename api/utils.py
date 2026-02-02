def expand_domain_plan(domains: dict) -> list[str]:
    plan = []
    for domain, count in domains.items():
        plan.extend([domain] * count)
    return plan

def expand_difficulty_plan(total: int, mix: dict) -> list[str]:
    plan = []
    for difficulty, percent in mix.items():
        count = round((percent / 100) * total)
        plan.extend([difficulty] * count)
    return plan[:total]