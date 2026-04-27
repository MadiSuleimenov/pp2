# db.py — работа с PostgreSQL через psycopg2
import psycopg2
from psycopg2.extras import RealDictCursor

# подключение
# Измени параметры под свою БД
DB_PARAMS = {
    "host":     "localhost",
    "port":     5432,
    "dbname":   "snake_db",
    "user":     "postgres",
    "password": "1234",
}


def _connect():
    return psycopg2.connect(**DB_PARAMS)


def init_db():
    """Создаёт таблицы если их нет."""
    sql = """
    CREATE TABLE IF NOT EXISTS players (
        id       SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS game_sessions (
        id            SERIAL PRIMARY KEY,
        player_id     INTEGER REFERENCES players(id),
        score         INTEGER   NOT NULL,
        level_reached INTEGER   NOT NULL,
        played_at     TIMESTAMP DEFAULT NOW()
    );
    """
    try:
        with _connect() as conn, conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()
        return True
    except Exception as e:
        print(f"[DB] init error: {e}")
        return False


def get_or_create_player(username: str) -> int | None:
    """Возвращает player_id (создаёт запись если нет)."""
    try:
        with _connect() as conn, conn.cursor() as cur:
            cur.execute("INSERT INTO players (username) VALUES (%s)"
                        " ON CONFLICT (username) DO NOTHING", (username,))
            conn.commit()
            cur.execute("SELECT id FROM players WHERE username = %s", (username,))
            row = cur.fetchone()
            return row[0] if row else None
    except Exception as e:
        print(f"[DB] get_or_create_player error: {e}")
        return None


def save_session(username: str, score: int, level: int):
    """Сохраняет результат игры."""
    try:
        pid = get_or_create_player(username)
        if pid is None:
            return
        with _connect() as conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO game_sessions (player_id, score, level_reached)"
                " VALUES (%s, %s, %s)",
                (pid, score, level)
            )
            conn.commit()
    except Exception as e:
        print(f"[DB] save_session error: {e}")


def get_leaderboard(limit=10) -> list[dict]:
    """Топ-N по лучшему счёту."""
    try:
        with _connect() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT p.username,
                       gs.score,
                       gs.level_reached,
                       gs.played_at::date AS date
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                ORDER BY gs.score DESC
                LIMIT %s
            """, (limit,))
            return [dict(r) for r in cur.fetchall()]
    except Exception as e:
        print(f"[DB] get_leaderboard error: {e}")
        return []


def get_personal_best(username: str) -> int:
    """Лучший счёт игрока (0 если нет записей)."""
    try:
        with _connect() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT COALESCE(MAX(gs.score), 0)
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                WHERE p.username = %s
            """, (username,))
            row = cur.fetchone()
            return row[0] if row else 0
    except Exception as e:
        print(f"[DB] get_personal_best error: {e}")
        return 0
