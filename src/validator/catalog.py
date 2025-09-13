def suggest_tags(pii_summary):
    return [{'policy':'pii','level':'detected' if any(v['hits'] for v in pii_summary.values()) else 'none'}]
