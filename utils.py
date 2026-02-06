import re


def normalize_npc_name(name: str) -> str:
    """Normalize an NPC name to match DB key conventions."""
    if not name:
        return ''
    name = name.strip().lstrip('#')
    return re.sub(r'\s+', '_', name)


def npc_lookup_keys(name: str) -> list[str]:
    """Generate candidate lookup keys to handle EQ/DB punctuation quirks."""
    base = normalize_npc_name(name)
    if not base:
        return []
    candidates = [base]

    # Some logs/sources may omit the EQ backtick used in certain NPC names.
    if '`' in base:
        candidates.append(base.replace('`', ''))
    else:
        # If the DB includes a backtick but the log omitted it, a strict match will fail.
        # We can't reliably re-insert it, but removing punctuation on both sides often works.
        candidates.append(base)

    # Treat apostrophe/backtick as interchangeable in edge cases.
    if "'" in base:
        candidates.append(base.replace("'", '`'))
    if '`' in base:
        candidates.append(base.replace('`', "'"))

    # Also try a punctuation-stripped variant for stubborn cases.
    candidates.append(re.sub(r"[\'`]+", '', base))

    # De-dupe preserving order
    seen = set()
    out: list[str] = []
    for c in candidates:
        if c and c not in seen:
            seen.add(c)
            out.append(c)
    return out


def format_level_text(level, maxlevel) -> str:
    """Format level display, showing a range when maxlevel differs.

    Examples:
      level=10, maxlevel=10 -> "10"
      level=10, maxlevel=11 -> "10-11"
      level="--" -> "--"
    """
    try:
        level_s = str(level).strip() if level is not None else ""
        level_i = int(level_s) if level_s.isdigit() else None

        try:
            maxlevel_i = int(maxlevel) if maxlevel not in (None, "", "--") else 0
        except Exception:
            maxlevel_i = 0

        if level_i is None:
            return level_s if level_s else "--"

        if maxlevel_i and maxlevel_i != level_i:
            lo = min(level_i, maxlevel_i)
            hi = max(level_i, maxlevel_i)
            return f"{lo}-{hi}"

        return str(level_i)
    except Exception:
        return str(level if level is not None else "--")
