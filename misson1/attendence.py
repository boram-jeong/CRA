# dat[사용자ID][요일]
grade = [0] * 100
names = [''] * 100


def get_day_of_the_week_index(day_name):
    if day_name == "monday":
        return 0
    elif day_name == "tuesday":
        return 1
    elif day_name == "wednesday":
        return 2
    elif day_name == "thursday":
        return 3
    elif day_name == "friday":
        return 4
    elif day_name == "saturday":
        return 5
    elif day_name == "sunday":
        return 6
    else: return -1

def get_point_of_target_day(day_name):
    if day_name == "wednesday":
        return 3
    elif day_name == "saturday" or day_name == "sunday":
        return 2
    else: return 1





def update_player_dict(player_name, id_dict):
    number_of_ids = len(id_dict)
    if player_name not in id_dict:
        number_of_ids += 1
        id_dict[player_name] = number_of_ids
        names[number_of_ids] = player_name
    return id_dict

def read_attendance_file(file_name):
    try:
        lines = []

        with open("attendance_weekday_500.txt", encoding='utf-8') as f:
            for _ in range(500):
                line = f.readline()
                if not line:
                    break
                player_information = line.strip().split()
                if len(player_information) == 2:
                    lines.append(player_information)
                else:
                    print("file read error, check input file")

        return lines

    except Exception as e:
        raise Exception(f"read error: {e}")


def update_current_player_point(current_player_id, day, points):
    points.append(0)
    add_point = get_point_of_target_day(day)
    points[current_player_id] += add_point

    return points


def update_attendence_list(current_player_id, day, attendence_list):
    attendence_list.append([0 for _ in range(7)])
    index = get_day_of_the_week_index(day)
    attendence_list[current_player_id][index] += 1

    return attendence_list


def get_attendence_list(player_attendence_information, updated_player_dict):
    attendence_list = [[0 for _ in range(7)]]
    for each_player_information in player_attendence_information:
        name, day = each_player_information[0], each_player_information[1]
        attendence_list = update_attendence_list(updated_player_dict[name], day, attendence_list)

    return attendence_list


def get_attendence_list(player_attendence_information, updated_player_dict):
    attendence_list = [[0 for _ in range(7)]]
    for each_player_information in player_attendence_information:
        name, day = each_player_information[0], each_player_information[1]
        attendence_list = update_attendence_list(updated_player_dict[name], day, attendence_list)

    return attendence_list

def input_file():
    player_dict = {}
    try:
        player_attendence_information = read_attendance_file("attendance_weekday_500.txt")
        attendence_list = [[0 for _ in range(7)]]
        points = [0]
        for each_player_information in player_attendence_information:
            name, day = each_player_information[0], each_player_information[1]
            updated_player_dict = update_player_dict(name, player_dict)
            attendence_list = update_attendence_list(updated_player_dict[name], day, attendence_list)
            points = update_current_player_point(updated_player_dict[name], day, points)




        number_of_ids = len(updated_player_dict)

        updated_points = update_bonus_point(number_of_ids, attendence_list, points)
        updated_grade = calculated_grade(number_of_ids, updated_points)
        print_player_point_and_grade(updated_player_dict, updated_grade, points)

        print("\nRemoved player")
        print("==============")
        for player_id in range(1, number_of_ids + 1):

            wednesday_index = get_day_of_the_week_index('wednesday')
            saturday_index = get_day_of_the_week_index('saturday')
            sunday_index = get_day_of_the_week_index('sunday')

            number_of_attendence_for_wednesday = attendence_list[player_id][wednesday_index]
            number_of_attendence_for_weekend = attendence_list[player_id][saturday_index] + attendence_list[player_id][sunday_index]
            if grade[player_id] not in (1, 2) and number_of_attendence_for_wednesday == 0 and number_of_attendence_for_weekend == 0:
                print(names[player_id])

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")


def print_player_point_and_grade(player_dict, grade, points):
    for player_name, player_id in player_dict.items():
        print(f"NAME : {player_name}, POINT : {points[player_id]}, GRADE : ", end="")
        if grade[player_id] == 1:
            print("GOLD")
        elif grade[player_id] == 2:
            print("SILVER")
        else:
            print("NORMAL")


def calculated_grade(number_of_ids, points):
    grade = [0]
    for player_id in range(1, number_of_ids + 1):
        grade.append(0)
        if points[player_id] >= 50:
            grade[player_id] = 1
        elif points[player_id] >= 30:
            grade[player_id] = 2
        else:
            grade[player_id] = 0
    return grade


def update_bonus_point(number_of_ids, dat, points):
    for player_id in range(1, number_of_ids + 1):
        if dat[player_id][2] > 9:
            points[player_id] += 10
        if dat[player_id][5] + dat[player_id][6] > 9:
            points[player_id] += 10

    return points


if __name__ == "__main__":
    input_file()