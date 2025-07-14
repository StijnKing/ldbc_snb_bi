// 6. List all people that mention a new employee that work at the same company.
MATCH (m:Message::(e:Person))-[:hasCreator]->(p:Person)-[:workAt]->(c:Company),
      (e:Person)-[:workAt]->(c:Company)
RETURN p.firstName, p.lastName, e.firstName, e.lastName, c.name;
