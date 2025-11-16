from datetime import date, timedelta

import pytest

from tests.factories import HabitFactory, HabitLogFactory
from tests.helpers import auth_headers


def test_stats_no_logs(client, db, user_token):
    habit = HabitFactory()
    db.session.commit()

    resp = client.get(
        f"/habits/{habit.id}/stats",
        headers=auth_headers(user_token),
    )

    data = resp.get_json()
    assert resp.status_code == 200
    assert data["streak"] == 0
    assert data["completion_rate"] == 0.0


def test_stats_with_logs(client, db, user_token):
    habit = HabitFactory()
    db.session.commit()

    # День 1 — выполнено
    HabitLogFactory(
        habit_id=habit.id,
        date=date.today(),
        completed=True,
    )

    # День 2 — выполнено (вчера)
    HabitLogFactory(
        habit_id=habit.id,
        date=date.today() - timedelta(days=1),
        completed=True,
    )

    # День 3 — не выполнено (2 дня назад)
    HabitLogFactory(
        habit_id=habit.id,
        date=date.today() - timedelta(days=2),
        completed=False,
    )

    db.session.commit()

    resp = client.get(
        f"/habits/{habit.id}/stats",
        headers=auth_headers(user_token),
    )

    data = resp.get_json()

    assert resp.status_code == 200
    assert data["streak"] == 2  # последние 2 дня completed=True
    assert data["completion_rate"] == pytest.approx(66.67, 0.1)
