import re
EMAIL_RE=re.compile(r"[\w.\-+]+@[\w\-]+\.[A-Za-z]{2,}")
PHONE_RE=re.compile(r"\b\+?\d[\d\s\-()]{7,}\b")
def classify_series(name, series):
    sample=series.dropna().astype(str).head(200).tolist()
    text=" ".join(sample); hits=[]
    if EMAIL_RE.search(text): hits.append("EMAIL")
    if PHONE_RE.search(text): hits.append("PHONE")
    return {"field":name,"hits":hits,"count":len(sample)}
