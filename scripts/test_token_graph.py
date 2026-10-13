import copy
import unittest
from validate_token_graph import validate


def sample():
    def token(id, name, tier, value, **extra):
        return dict(id=id, name=name, tier=tier, type="COLOR", values={"light": value}, purpose="Fixture", permittedUses=["Fixture"], status="observed", source="fixture", **extra)
    return {"policy": {"numberedColorPrimitives": True}, "tokens": [
        token("p", "color/purple/700", "primitive", dict(r=.2, g=.1, b=.8)),
        token("s", "color/text/primary", "semantic", dict(type="VARIABLE_ALIAS", id="p")),
        token("c", "button/foreground", "component", dict(type="VARIABLE_ALIAS", id="s"), owner="button")], "bindings": []}


class TokenGraphTests(unittest.TestCase):
    def test_valid_graph(self):
        self.assertEqual(validate(sample()), [])

    def test_bad_cases(self):
        cases = [
            (0, "name", "color/heading", "usage role"),
            (0, "name", "color/purple", "numbered colour"),
            (0, "name", "color/merge-purple/700", "merge marker"),
            (1, "values", {"light": "#FFFFFF"}, "raw value outside"),
            (1, "values", {"light": {"type": "VARIABLE_ALIAS", "id": "absent"}}, "missing alias"),
            (1, "type", "FLOAT", "type mismatch"),
            (1, "values", {"light": {"type": "VARIABLE_ALIAS", "id": "c"}}, "semantic depends"),
            (1, "values", {"light": {"type": "VARIABLE_ALIAS", "id": "s"}}, "alias cycle"),
            (2, "values", {"light": {"type": "VARIABLE_ALIAS", "id": "p"}}, "bypasses semantic"),
            (2, "owner", "avatar", "owner/name mismatch"),
            (0, "status", "", "unknown status"),
            (0, "id", "s", "duplicate or missing id"),
        ]
        for i, key, value, expected in cases:
            with self.subTest(expected=expected):
                data = sample()
                data["tokens"][i][key] = value
                self.assertTrue(any(expected in e for e in validate(data)))

    def test_scale_and_legitimate_exceptions(self):
        data = sample()
        data["tokens"][0].update(type="FLOAT", name="radius/6", values={"light": 6})
        data["tokens"][1]["type"] = data["tokens"][2]["type"] = "FLOAT"
        self.assertEqual(validate(data), [])
        data["tokens"][0].update(name="space/33", values={"light": 32})
        self.assertTrue(any("differs from value" in e for e in validate(data)))

    def test_equal_values_do_not_merge_semantics(self):
        data = sample()
        other = copy.deepcopy(data["tokens"][1])
        other.update(id="s2", name="color/icon/primary")
        data["tokens"].append(other)
        self.assertEqual(validate(data), [])

    def test_binding_scope(self):
        data = sample()
        data["bindings"] = [dict(nodeId="n", field="fill", tokenId="p", context="component", owner="button")]
        self.assertTrue(any("direct primitive" in e for e in validate(data)))
        data["bindings"][0]["context"] = "foundation"
        self.assertEqual(validate(data), [])
        data["bindings"][0].update(tokenId="c", context="component", owner="avatar")
        self.assertTrue(any("wrong component" in e for e in validate(data)))

    def test_component_geometry_direct_alias_is_valid(self):
        data = sample()
        data["tokens"][0].update(type="FLOAT", name="dimension/53", values={"light": 53})
        data["tokens"][1]["type"] = data["tokens"][2]["type"] = "FLOAT"
        data["tokens"][2]["values"]["light"]["id"] = "p"
        self.assertEqual(validate(data), [])


if __name__ == "__main__":
    unittest.main()
