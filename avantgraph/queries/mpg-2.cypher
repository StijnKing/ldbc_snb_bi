// 2. Find all authors and their messages that mention the startyear of someone working at a company
MATCH (c:Message::()-[:workAt]..prop->())-[:hasCreator]->(p:Person)-[:workAt]..prop->(co:Company)
WHERE KEY(prop) = "workFrom"
RETURN VALUE(prop), p.firstName, p.lastName;
