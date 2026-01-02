MATCH ()..p-[:isLocatedIn]->(:City {name: "London"})
WHERE KEY(p) = "name"
RETURN VALUE(p) AS Name;
