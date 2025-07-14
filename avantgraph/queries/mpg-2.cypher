// 2. Find all authors and comments that mention the startyear of someone working at a company
// That is the same year as when they started working at a company.
MATCH (c:Comment::{prop})-[:hasCreator]->(p:Person)-[:workAt]..prop->(co:Company)
WHERE KEY(prop) = "workFrom"
RETURN VALUE(prop), p.firstName, p.lastName;
