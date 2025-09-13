from dataclasses import dataclass, field
from typing import Any, List, Optional, Dict
@dataclass
class FieldConstraint:
    min: Optional[float]=None; max: Optional[float]=None; allowed_values: Optional[List[Any]]=None
@dataclass
class FieldSpec:
    name: str; type: str; nullable: bool=True; constraints: FieldConstraint=field(default_factory=FieldConstraint)
@dataclass
class Contract:
    name: str; description: str; owner: str; schema: List[FieldSpec]; pii: Dict[str,Any]|None=None
def load_contract(yaml_path: str) -> Contract:
    import yaml
    with open(yaml_path) as f: raw=yaml.safe_load(f)
    fields=[]
    for s in raw["schema"]:
        c=s.get("constraints",{})
        fields.append(FieldSpec(s["name"], s["type"], bool(s.get("nullable",True)),
            FieldConstraint(c.get("min"), c.get("max"), c.get("allowed_values"))))
    return Contract(raw["name"], raw.get("description",""), raw.get("owner",""), fields, raw.get("pii",{}))
