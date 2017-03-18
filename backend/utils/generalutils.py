"""Utilities that don't fit in anywhere else."""


def urlify(app, list):
    """Urlify list by adding rules for each list and giving a view."""
    for i in list:
        app.add_url_rule(i[0], view_func=i[1], methods=["POST"])
