#!/usr/bin/python2
# -*- coding: utf-8 -*-

from sqlalchemy import MetaData, create_engine, text

engine = create_engine("postgresql:///retailexpert")

metadata = MetaData(engine)

SELECT_GOOD = """
SELECT id, colorlist
  FROM visitors
 WHERE colorlist IS NOT NULL
   AND LENGTH(colorlist) > 0
"""[1:-1]


def colors():
    with engine.connect() as conn:
        stmt = text(SELECT_GOOD).bindparams()
        return conn.execute(stmt).fetchall()

if __name__ == "__main__":
    pass
