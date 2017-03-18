"""Get tables from the database and apply heuristic to get list of photos."""


def getTopN(conn, N):
    """Get top N images according to our heuristic."""
    result = conn.execute("SELECT * FROM Images WHERE Active == TRUE")

    # Generate score for each of the rows.
    for row in result:
