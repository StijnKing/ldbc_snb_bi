// Q1. Posting summary
/*
:params { datetime: datetime('2011-12-01T00:00:00.000') }
*/
MATCH (c:Comment)
RETURN c.browserUsed
