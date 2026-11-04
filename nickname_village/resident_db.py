"""SQLite 주민 등록부. 연결은 작업마다 열고 반드시 닫는다."""
import sqlite3
from contextlib import closing
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).with_name("village.db")


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with closing(connect()) as conn, conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS residents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT NOT NULL,
            seed TEXT NOT NULL,
            style TEXT NOT NULL,
            avatar_svg TEXT NOT NULL,
            house_no INTEGER NOT NULL UNIQUE CHECK(house_no BETWEEN 1 AND 6),
            job TEXT NOT NULL,
            personality TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(nickname, style)
        )""")


def get_residents():
    with closing(connect()) as conn:
        return [dict(row) for row in conn.execute("SELECT * FROM residents ORDER BY house_no")]


def validate_profile(job, personality):
    if not job.strip() or len(job.strip()) > 30:
        raise ValueError("직업은 1~30자로 입력해 주세요.")
    if not personality.strip() or len(personality.strip()) > 200:
        raise ValueError("성격은 1~200자로 입력해 주세요.")


def add_resident(nickname, style, avatar_svg, house_no, job, personality):
    nickname = nickname.strip()
    validate_profile(job, personality)
    if not nickname or len(nickname) > 20 or style not in ("pixel-art", "bottts"):
        raise ValueError("닉네임과 스타일을 확인해 주세요.")
    if house_no not in range(1, 7) or not avatar_svg:
        raise ValueError("빈집과 생성한 주민 사진을 확인해 주세요.")
    try:
        with closing(connect()) as conn, conn:
            conn.execute("""INSERT INTO residents
                (nickname,seed,style,avatar_svg,house_no,job,personality,created_at)
                VALUES (?,?,?,?,?,?,?,?)""",
                (nickname, nickname, style, avatar_svg, house_no, job.strip(),
                 personality.strip(), datetime.now().isoformat(timespec="seconds")))
    except sqlite3.IntegrityError as error:
        raise ValueError("이미 입주한 닉네임·스타일이거나, 다른 주민이 사는 집이에요.") from error


def update_resident(resident_id, job, personality):
    validate_profile(job, personality)
    with closing(connect()) as conn, conn:
        conn.execute("UPDATE residents SET job=?, personality=? WHERE id=?",
                     (job.strip(), personality.strip(), resident_id))


def delete_resident(resident_id):
    with closing(connect()) as conn, conn:
        conn.execute("DELETE FROM residents WHERE id=?", (resident_id,))
