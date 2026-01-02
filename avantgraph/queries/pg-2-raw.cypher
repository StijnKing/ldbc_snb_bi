MATCH (n)
RETURN n.name
UNION
MATCH ()-[r]->()
RETURN r.name;
