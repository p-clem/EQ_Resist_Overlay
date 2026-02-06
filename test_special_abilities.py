#!/usr/bin/env python3

from special_abilities import parse_special_abilities, parse_special_abilities_ids


def test_pair_encoded_entries_do_not_treat_params_as_abilities():
    raw = "10,1^13,1^15,1"
    assert parse_special_abilities_ids(raw) == [10, 13, 15]
    assert parse_special_abilities(raw) == "MagicalAttack, Unmezzable, Unstunable"


def test_single_pair_entry():
    raw = "10,1"
    assert parse_special_abilities_ids(raw) == [10]
    assert parse_special_abilities(raw) == "MagicalAttack"


def test_colon_params_are_ignored():
    raw = "1^10:1,1^14"
    assert parse_special_abilities_ids(raw) == [1, 10, 14]


if __name__ == "__main__":
    test_pair_encoded_entries_do_not_treat_params_as_abilities()
    test_single_pair_entry()
    test_colon_params_are_ignored()
    print("OK")
