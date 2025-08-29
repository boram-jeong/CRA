from attendence import *
import pytest

def test_read_attendance_file_Should_raise_exception_When_file_does_not_exist():
    wrong_file_name = 'wrong_file_name.txt'
    with pytest.raises(Exception):
        read_attendance_file(wrong_file_name)

player_info_for_test = [
    ('cat', {'amy':1, 'bori':2}, {'amy':1, 'bori':2, 'cat':3}),
    ('amy', {'amy':1}, {'amy':1})
]
@pytest.mark.parametrize("player_name, current_dict, expected_player_dict", player_info_for_test)
def test_update_player_dict(player_name, current_dict, expected_player_dict):
    assert update_player_dict(player_name, current_dict) == expected_player_dict

day_name_and_index_test_data = [
    ("monday", 0),
    ("tuesday", 1),
    ("wednesday", 2),
    ("thursday", 3),
    ("friday", 4),
    ("saturday", 5),
    ("sunday", 6),
    ("wrong", -1)
]
@pytest.mark.parametrize("day_name, expected", day_name_and_index_test_data)
def test_get_day_of_the_week_index_Should_return_correct_index_When_day_is_given(day_name, expected):
    assert get_day_of_the_week_index(day_name) == expected

def test_get_player_dict_Should_return_player_dict_When_player_attendence_information_is_given():
    player_attendence_information = read_attendance_file("attendance_weekday_500.txt")
    assert get_player_dict(player_attendence_information).get('Oscar', None) is not None

def test_get_attendence_list_Should_return_attendence_list_When_player_attendence_information_is_given():
    player_attendence_information = read_attendance_file("attendence_test_simple_case.txt")
    player_dict = {'amy': 1, 'bori': 2, 'cat': 3}
    expected_attendence_list = [[0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0]]
    assert get_attendence_list(player_attendence_information, player_dict) ==  expected_attendence_list

def test_attendence_manager_Should_execute_properly_When_correct_file_is_given():
    player_dict, updated_points= attendence_manager('attendence_test_simple_case.txt')
    expected_player_dict = {'amy': 1, 'bori': 2, 'cat': 3}
    expected_points = [0, 1, 1, 1]
    assert player_dict == expected_player_dict
    assert updated_points == expected_points

def test_attendence_manager_Should_raise_exception_When_incorrect_file_is_given():
    with pytest.raises(Exception):
        attendence_manager("attendence_test_wrong_case.txt")

day_name_and_points_test_data = [
    ("monday", 1),
    ("tuesday", 1),
    ("wednesday", 3),
    ("thursday", 1),
    ("friday", 1),
    ("saturday", 2),
    ("sunday", 2)
]
@pytest.mark.parametrize("day_name, expected", day_name_and_points_test_data)
def test_get_point_of_target_day_Should_return_correct_point_When_day_is_given(day_name, expected):
    assert get_point_of_target_day(day_name) == expected


def test_update_bonus_point_Should_return_updated_points_When_attendence_list_and_points_are_given():
    number_of_id = 3
    attendence_list = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 15, 0, 0, 0, 0], [1, 0, 0, 0, 0, 6, 7], [0, 1, 0, 0, 0, 0, 0]]
    points = [0, 45, 27, 1]
    expected_points = [0, 55, 37, 1]

    assert update_bonus_point(number_of_id, attendence_list, points) == expected_points


grade_and_points_for_test = [
    ({'amy':1}, [0, 70], 'NAME : amy, POINT : 70, GRADE : GOLD\n'),
    ({'bb':1}, [0, 40], 'NAME : bb, POINT : 40, GRADE : SILVER\n')
]
@pytest.mark.parametrize("player_dict, points, expected_output", grade_and_points_for_test)
def test_print_player_point_and_grade_Should_print_correctly_When_grade_and_points_are_given(capsys, player_dict, points, expected_output):
    print_player_point_and_grade(player_dict, points)
    captured = capsys.readouterr()
    assert captured.out == expected_output