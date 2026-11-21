from pathlib import Path

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb


def connect():
    return psycopg.connect('', row_factory=dict_row, connect_timeout=4)


def migrate():
    migration = Path(__file__).resolve().parents[1] / 'migrations' / '001_transfer_review.sql'
    with connect() as db:
        db.execute('SELECT pg_advisory_xact_lock(1051001)')
        db.execute(migration.read_text())


def record(db, plan_id, actor, event, **details):
    db.execute('INSERT INTO transfer_audit (plan_id, actor, event, details) VALUES (%s,%s,%s,%s)',
               (plan_id, actor, event, Jsonb(details)))
