"""API educacional para demonstrar comunicação HTTP + PostgreSQL via Docker Compose."""
import logging
import os

from flask import Flask, jsonify, request
import psycopg
from psycopg.rows import dict_row

app = Flask(__name__)
logger = logging.getLogger(__name__)


def db_connect():
    return psycopg.connect(
        os.environ["DATABASE_URL"], connect_timeout=3, row_factory=dict_row
    )


@app.get("/api/health")
def health():
    try:
        with db_connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return jsonify(status="ok", database="ok"), 200
    except psycopg.Error:
        logger.exception("Database healthcheck failed")
        return jsonify(status="degraded", database="unavailable"), 503


@app.get("/api/tasks")
def list_tasks():
    try:
        with db_connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, titulo, criada_em FROM tarefas "
                    "ORDER BY id DESC LIMIT 100"
                )
                rows = cur.fetchall()
        return jsonify([
            {"id": row["id"], "titulo": row["titulo"],
             "criada_em": row["criada_em"].isoformat()}
            for row in rows
        ]), 200
    except psycopg.Error:
        logger.exception("Could not list tasks")
        return jsonify(erro="Banco indisponível; tente novamente"), 503


@app.post("/api/tasks")
def create_task():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(erro="Envie um objeto JSON"), 400
    title = data.get("titulo", "")
    if not isinstance(title, str):
        return jsonify(erro="O campo 'titulo' deve ser texto"), 400
    title = title.strip()
    if not 1 <= len(title) <= 120:
        return jsonify(erro="Título obrigatório: entre 1 e 120 caracteres"), 400
    try:
        with db_connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO tarefas (titulo) VALUES (%s) RETURNING id",
                    (title,),
                )
                task_id = cur.fetchone()["id"]
        return jsonify(id=task_id, titulo=title), 201
    except psycopg.Error:
        logger.exception("Could not create task")
        return jsonify(erro="Banco indisponível; tente novamente"), 503
