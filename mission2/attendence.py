from abc import ABC, abstractmethod

DAY_INDEX = {
    "monday": 0, "tuesday": 1, "wednesday": 2,
    "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6
}

def get_day_of_the_week_index(day_name: str) -> int:
    return DAY_INDEX.get(day_name, -1)

def get_point_of_target_day(day_name: str) -> int:
    if day_name == "wednesday":
        return 3
    elif day_name in ("saturday", "sunday"):
        return 2
    return 1

def read_attendance_file(file_name: str):
    try:
        lines = []
        with open(file_name, encoding='utf-8') as f:
            for _ in range(500):
                line = f.readline()
                if not line:
                    break
                parts = line.strip().split()
                if len(parts) == 2:
                    lines.append(parts)
                else:
                    raise Exception("file read error, check input file")
        return lines
    except Exception as e:
        raise Exception(f"read error: {e}")

class Grade(ABC):
    @abstractmethod
    def print(self): ...

class Gold(Grade):
    def print(self): print("GOLD")

class Silver(Grade):
    def print(self): print("SILVER")

class Normal(Grade):
    def print(self): print("NORMAL")

def get_grade_from_player_points(points: int) -> Grade:
    if points >= 50:
        return Gold()
    elif points >= 30:
        return Silver()
    else:
        return Normal()

class PlayerStats:
    def __init__(self, name: str):
        self.name = name
        self.attendance = [0] * 7
        self.points = 0

    def add_attendance(self, day_name: str):
        idx = get_day_of_the_week_index(day_name)
        if idx == -1:
            raise ValueError(f"unknown day: {day_name}")
        self.attendance[idx] += 1
        self.points += get_point_of_target_day(day_name)

    def apply_bonus(self):
        if self.attendance[get_day_of_the_week_index("wednesday")] > 9:
            self.points += 10
        if (self.attendance[get_day_of_the_week_index("saturday")] +
            self.attendance[get_day_of_the_week_index("sunday")]) > 9:
            self.points += 10

def attendence_manager(file_name):
    try:
        player_info = read_attendance_file(file_name)
        players = {}
        for name, day in player_info:
            if name not in players:
                players[name] = PlayerStats(name)
            players[name].add_attendance(day)

        for p in players.values():
            p.apply_bonus()

        for p in players.values():
            print(f"NAME : {p.name}, POINT : {p.points}, GRADE : ", end="")
            get_grade_from_player_points(p.points).print()

        print("\nRemoved player")
        print("==============")
        for p in players.values():
            if (p.points < 30 and
                p.attendance[get_day_of_the_week_index("wednesday")] == 0 and
                (p.attendance[get_day_of_the_week_index("saturday")] +
                 p.attendance[get_day_of_the_week_index("sunday")]) == 0):
                print(p.name)

        player_dict = {name: i+1 for i, name in enumerate(players.keys())}
        points = [0] + [p.points for p in players.values()]
        return player_dict, points

    except Exception as e:
        raise Exception(f"attendence_manager_has_error: {e}")

def main():
    attendence_manager("attendance_weekday_500.txt")

if __name__ == "__main__":
    main()
