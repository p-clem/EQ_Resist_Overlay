SPECIAL_ABILITIES = {
    1: "Summon",
    2: "Enrage",
    3: "Rampage",
    4: "AreaRampage",
    5: "Flurry",
    6: "TripleAttack",
    7: "DualWield",
    8: "DisallowEquip",
    9: "BaneAttack",
    10: "MagicalAttack",
    11: "RangedAttack",
    12: "Unslowable",          # SlowImmunity
    13: "Unmezzable",          # MesmerizeImmunity
    14: "Uncharmable",         # CharmImmunity
    15: "Unstunable",          # StunImmunity
    16: "Unsnarable",          # SnareImmunity
    17: "Unfearable",          # FearImmunity
    18: "DispellImmunity",
    19: "MeleeImmunity",
    20: "MagicImmunity",
    21: "Immune to fleeing",   # FleeingImmunity
    22: "MeleeImmunityExceptBane",
    23: "Immune to melee except magical",  # MeleeImmunityExceptMagical
    24: "AggroImmunity",
    25: "BeingAggroImmunity",
    26: "CastingFromRangeImmunity",
    27: "FeignDeathImmunity",
    28: "TauntImmunity",
    29: "TunnelVision",
    30: "NoBuffHealFriends",
    31: "Immune to lull effects",  # PacifyImmunity
    32: "Leash",
    33: "Tether",
    34: "PermarootFlee",
    35: "HarmFromClientImmunity",
    36: "AlwaysFlee",
    37: "FleePercent",
    38: "AllowBeneficial",
    39: "DisableMelee",
    40: "NPCChaseDistance",
    41: "AllowedToTank",
    42: "ProximityAggro",
    43: "AlwaysCallHelp",
    44: "UseWarriorSkills",
    45: "AlwaysFleeLowCon",
    46: "NoLoitering",
    47: "BadFactionBlockHandin",
    48: "PCDeathblowCorpse",
    49: "CorpseCamper",
    50: "ReverseSlow",
    51: "HasteImmunity",
    52: "DisarmImmunity",
    53: "RiposteImmunity",
    54: "ProximityAggro2",
    # 55: "Max"  # usually not used as an ability
}


def _iter_ability_ids(entry: str):
    """Yield ordered, de-duplicated ability IDs from a DB `special_abilities` string.

    The common format is caret-separated ability entries, where each entry is:
    `id,param1,param2...` (comma-separated params).

    Examples:
    - "10,1^13,1^15,1" -> 10, 13, 15
    - "1,1^2,1^3,1,4^10,1" -> 1, 2, 3, 10
    - "1^10:1,1^14" -> 1, 10, 14 (params after ':' or ',' are ignored)
    """
    if not entry or str(entry).strip() == "":
        return

    seen: set[int] = set()

    # Abilities are separated by '^'. Commas inside a segment are parameters.
    # We intentionally do NOT split on ',' first, because that misreads params as abilities.
    for segment in str(entry).split('^'):
        token = segment.strip()
        if not token:
            continue

        # Some sources store params like "10:1"; keep just the numeric prefix.
        for sep in (':', ','):
            if sep in token:
                token = token.split(sep, 1)[0].strip()
                break

        # Accept leading digits only.
        num = ''
        for ch in token:
            if ch.isdigit():
                num += ch
            else:
                break
        if not num:
            continue

        try:
            aid = int(num)
        except ValueError:
            continue

        if aid in SPECIAL_ABILITIES and aid not in seen:
            seen.add(aid)
            yield aid


def parse_special_abilities_ids(entry: str) -> list[int]:
    """Parse a special_abilities DB string and return ordered ability IDs.

    Handles formats like:
    - "1,1^10,1^14,1"
    - "1^10:1,1^14" (params after ':' are ignored)
    """
    if not entry or entry.strip() == "":
        return []

    return list(_iter_ability_ids(entry))


def parse_special_abilities(entry: str) -> str:
    """Parse a special_abilities DB string and return comma-separated friendly names."""
    if not entry or entry.strip() == "":
        return ""

    ordered_names = [SPECIAL_ABILITIES[aid] for aid in _iter_ability_ids(entry)]
    return ", ".join(ordered_names)
