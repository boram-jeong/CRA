from attendence import *
import pytest

def test_read_attendance_file_Should_raise_exception_When_file_does_not_exist():
    wrong_file_name = 'wrong_file_name.txt'
    with pytest.raises(Exception):
        read_attendance_file(wrong_file_name)

points_for_test = [
    (5, [0, 70, 76, 30, 2, 10], [0, 1, 1, 2, 0, 0]),
    (5, [0, 1, 0, 0, 2, 30], [0, 0, 0, 0, 0, 2])
]
@pytest.mark.parametrize("number_of_id, points, expected_grade", points_for_test)
def test_calculated_grade_Should_return_correct_grade_When_number_of_ids_and_points_are_given(number_of_id, points, expected_grade):
    assert calculated_grade(number_of_id, points) == expected_grade

player_info_for_test = [
    ('cat', {'amy':1, 'bori':2}, {'amy':1, 'bori':2, 'cat':3}),
    ('amy', {'amy':1}, {'amy':1})
]
@pytest.mark.parametrize("player_name, current_dict, expected_player_dict", player_info_for_test)
def test_update_player_dict(player_name, current_dict, expected_player_dict):
    assert update_player_dict(player_name, current_dict) == expected_player_dict

def test_get_player_dict_Should_return_player_dict_When_player_attendence_information_is_given():
    player_attendence_information = read_attendance_file("attendance_weekday_500.txt")
    assert get_player_dict(player_attendence_information).get('Oscar', None) is not None

def test_get_attendence_list_Should_return_attendence_list_When_player_attendence_information_is_given():
    player_attendence_information = read_attendance_file("attendence_test_simple_case.txt")
    player_dict = {'amy': 1, 'bori': 2, 'cat': 3}
    expected_attendence_list = [[0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0]]
    assert get_attendence_list(player_attendence_information, player_dict) ==  expected_attendence_list

def test_attendence_manager_Should_execute_properly_When_correct_file_is_given():
    player_dict, updated_points, updated_grade = attendence_manager('attendence_test_simple_case.txt')
    expected_player_dict = {'amy': 1, 'bori': 2, 'cat': 3}
    expected_grade = [0, 0, 0, 0]
    expected_points = [0, 1, 1, 1]
    assert player_dict == expected_player_dict
    assert updated_grade == expected_grade
    assert updated_points == expected_points

def test_attendence_manager_Should_raise_exception_When_incorrect_file_is_given():
    with pytest.raises(Exception):
        attendence_manager("attendence_test_wrong_case.txt")
