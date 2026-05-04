from __future__ import annotations

import json
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from database import SessionLocal  # noqa: E402
from models.user import User  # noqa: E402
from services.auth import get_password_hash  # noqa: E402

TOTAL_FAKE_USERS = 20000
BATCH_SIZE = 1000
DEFAULT_PASSWORD = "Password123!"
OUTPUT_FILE = Path(__file__).resolve().with_name("generated_user_ids.json")

FIRST_NAMES = [
    "Ana", "Luis", "Marta", "Carlos", "Lucia", "Javier", "Sofia", "Diego",
    "Elena", "Mario", "Paula", "Hugo", "Nora", "Adrian", "Irene", "Pablo",
    "Clara", "Raul", "Diana", "Ruben", "Celia", "Marcos", "Noelia", "Ivan",
]
LAST_NAMES = [
    "Garcia", "Lopez", "Martinez", "Sanchez", "Perez", "Gomez", "Martin",
    "Jimenez", "Ruiz", "Hernandez", "Diaz", "Torres", "Vazquez", "Romero",
    "Alvarez", "Molina", "Navarro", "Ortega", "Delgado", "Castro", "Ramos",
]
CITIES = [
    "Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao", "Malaga", "Zaragoza",
    "Murcia", "Vigo", "Granada", "Alicante", "Gijon", "Cordoba", "Salamanca",
]
COUNTRIES = ["Spain", "Peru", "Chile", "Colombia", "Argentina", "Ecuador", "Uruguay"]


def random_phone(seed_index: int) -> str:
    prefix = random.choice(["+34", "+51", "+56", "+57", "+54", "+593", "+598"])
    middle = f"{seed_index % 1000:03d}"
    tail = f"{random.randint(0, 9999999):07d}"
    return f"{prefix} {middle} {tail[:3]} {tail[3:]}"


def random_created_at() -> datetime:
    start = datetime(2024, 1, 1)
    end = datetime(2026, 4, 30)
    delta = end - start
    seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=seconds)


def build_email(index: int) -> str:
    return f"seed_user_{index:05d}@example.com"


def main() -> None:
    db = SessionLocal()
    generated_ids: list[int] = []
    password_hash = get_password_hash(DEFAULT_PASSWORD)

    try:
        existing_seed_emails = {
            email
            for (email,) in db.query(User.email)
            .filter(User.email.like("seed_user_%@example.com"))
            .all()
        }

        pending_indexes = [
            index
            for index in range(1, TOTAL_FAKE_USERS + 1)
            if build_email(index) not in existing_seed_emails
        ]

        if not pending_indexes:
            print("No hay usuarios fake pendientes para insertar.")
            return

        print(f"Insertando {len(pending_indexes)} usuarios fake...")

        for position, index in enumerate(pending_indexes, start=1):
            full_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)} {random.choice(LAST_NAMES)}"
            user = User(
                nombre=full_name,
                email=build_email(index),
                password=password_hash,
                telefono=random_phone(index),
                role="user",
                activo=True,
                created_at=random_created_at(),
            )
            db.add(user)

            if position % BATCH_SIZE == 0:
                db.commit()
                db.refresh(user)
                generated_ids.append(user.id)
                print(f"Insertados {position} usuarios...")

        db.commit()

        inserted_users = (
            db.query(User)
            .filter(User.email.like("seed_user_%@example.com"))
            .order_by(User.id.asc())
            .all()
        )
        generated_ids = [user.id for user in inserted_users]

        payload = {
            "total_seed_users": len(generated_ids),
            "default_password": DEFAULT_PASSWORD,
            "generated_user_ids": generated_ids,
            "created_at": datetime.utcnow().isoformat(),
        }
        OUTPUT_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

        print(f"Usuarios fake insertados: {len(generated_ids)}")
        print(f"IDs guardados en: {OUTPUT_FILE}")
        print(f"Superadmin preservado: rafael@superadmin.com")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
