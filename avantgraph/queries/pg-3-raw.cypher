MATCH (n)-[:isLocatedIn]->(:City {name: "London"})
RETURN n.name AS Name;
