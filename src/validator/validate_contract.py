import argparse, json, os, pandas as pd
from contracts import load_contract
from dlp_classifier import classify_series
from lineage import write_lineage
from catalog import suggest_tags

def check_schema(df, contract):
    expected=[f.name for f in contract.schema]; cols=list(df.columns)
    missing=[c for c in expected if c not in cols]; extra=[c for c in cols if c not in expected]
    errs=[]; 
    if missing: errs.append(f"Missing columns: {missing}")
    if extra: errs.append(f"Extra columns: {extra}")
    for f in contract.schema:
        if f.name in df.columns:
            try:
                if f.type=='int': pd.to_numeric(df[f.name], errors='raise', downcast='integer')
                elif f.type=='float': pd.to_numeric(df[f.name], errors='raise')
            except Exception as e: errs.append(f'Type mismatch on {f.name}: expected {f.type}: {e}')
            if (not f.nullable) and df[f.name].isna().any(): errs.append(f'Nulls not allowed in {f.name}')
            if f.constraints.allowed_values is not None and (~df[f.name].isin(f.constraints.allowed_values)).any():
                errs.append(f'{f.name} has values outside allowed set')
            if f.constraints.min is not None and (df[f.name] < f.constraints.min).any(): errs.append(f'{f.name} below min')
            if f.constraints.max is not None and (df[f.name] > f.constraints.max).any(): errs.append(f'{f.name} above max')
    return errs

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--contract', required=True); ap.add_argument('--data', required=True); ap.add_argument('--out', default='artifacts')
    args=ap.parse_args(); os.makedirs(args.out, exist_ok=True)
    C=load_contract(args.contract); df=pd.read_csv(args.data)
    errors=check_schema(df, C)
    pii={f.name: classify_series(f.name, df[f.name]) for f in C.schema if f.name in df.columns}
    lineage_path=write_lineage(args.out, C.name, 'features_customer_events')
    tags=suggest_tags(pii)
    res={'contract':C.name,'valid':len(errors)==0,'errors':errors,'pii_summary':pii,'lineage':lineage_path,'suggested_tags':tags}
    with open(os.path.join(args.out,'validation_result.json'),'w') as f: json.dump(res,f,indent=2)
    if errors: raise SystemExit(1)
    print(json.dumps(res, indent=2))
