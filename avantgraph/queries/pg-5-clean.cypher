MATCH (:Message)-[:hasCreator]->(p:Person)-[:workAt]..prop->(:Company)
WHERE KEY(prop) = "workFrom"
RETURN VALUE(prop), p.firstName, p.lastName;
