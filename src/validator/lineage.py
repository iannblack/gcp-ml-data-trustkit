import json, os
def write_lineage(out_dir, dataset, features):
    os.makedirs(out_dir, exist_ok=True)
    graph={"nodes":[{"id":dataset,"type":"dataset"},{"id":features,"type":"feature_table"}],
           "edges":[{"from":dataset,"to":features,"type":"derives"}]}
    path=os.path.join(out_dir,"lineage.json")
    with open(path,"w") as f: json.dump(graph,f,indent=2)
    return path
