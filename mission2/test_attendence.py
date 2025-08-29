import pytest
from attendence import (
    get_day_of_the_week_index, get_point_of_target_day,
    read_attendance_file, get_grade_from_player_points,
    Gold, Silver, Normal, PlayerStats, attendence_manager, main
)

@pytest.mark.parametrize("day, expected", [
    ("monday", 0), ("tuesday", 1), ("wednesday", 2),
    ("thursday", 3), ("friday", 4), ("saturday", 5), ("sunday", 6),
    ("wrong", -1)
])
def test_get_day_of_the_week_index_Should_return_correct_index_When_day_is_given(day, expected):
    assert get_day_of_the_week_index(day) == expected

@pytest.mark.parametrize("day, expected", [
    ("monday", 1), ("tuesday", 1), ("wednesday", 3),
    ("thursday", 1), ("friday", 1), ("saturday", 2), ("sunday", 2)
])
def test_get_point_of_target_day_Should_return_correct_point_When_day_is_given(day, expected):
    assert get_point_of_target_day(day) == expected


def test_read_attendance_file_Should_raise_exception_When_file_does_not_exist():
    with pytest.raises(Exception):
        read_attendance_file("not_exist.txt")

def test_read_attendance_file_Should_raise_exception_When_file_with_bad_line(tmp_path):
    f = tmp_path / "bad.txt"
    f.write_text("amy\n")
    with pytest.raises(Exception):
        read_attendance_file(str(f))

def test_playerstats_add_attendance_and_apply_bonus_Should_calculate_points_corretly_When_input_is_given():
    p = PlayerStats("amy")
    p.add_attendance("monday")
    p.add_attendance("wednesday")
    assert p.points == 4
    for _ in range(10):
        p.add_attendance("saturday")
    for _ in range(10):
        p.add_attendance("wednesday")
    p.apply_bonus()
    assert p.points >= 24

def test_playerstats_add_attendance_Should_raise_ValueError_When_invalid_input_is_given():
    p = PlayerStats("cat")
    with pytest.raises(ValueError):
        p.add_attendance("noday")

@pytest.mark.parametrize("pts, cls", [
    (70, Gold), (40, Silver), (10, Normal)
])
def test_get_grade_from_player_points_Should_return_correct_grade_When_points_are_given(pts, cls):
    g = get_grade_from_player_points(pts)
    assert isinstance(g, cls)

def test_attendence_manager_Should_print_correctly_When_input_file_is_given(tmp_path, capsys):
    f = tmp_path / "ok.txt"
    f.write_text("amy monday\nbori wednesday\ncat sunday\n")
    player_dict, points = attendence_manager(str(f))
    assert "amy" in player_dict
    assert len(points) == len(player_dict) + 1
    out = capsys.readouterr().out
    assert "NAME : amy" in out
    assert "Removed player" in out

def  test_attendence_manager_Should_raise_exception_When_bad_input_file_is_given(tmp_path):
    f = tmp_path / "bad2.txt"
    f.write_text("amy wrong wrong\n")
    with pytest.raises(Exception):
        attendence_manager(str(f))

def test_main_runs(monkeypatch):
    monkeypatch.setattr("attendence.attendence_manager", lambda f=None: ({}, []))
    main()
