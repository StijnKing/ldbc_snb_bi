MATCH (:Message)-[:hasCreator]->(p:Person)-[w:workAt]->(:Company)
RETURN w.workFrom AS startyear, p.firstName, p.lastName;