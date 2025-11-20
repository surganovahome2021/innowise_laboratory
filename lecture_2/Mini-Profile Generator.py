current_year = 2025
count = 0
person = str
loop_stop = "stop"
life_stage = ["Child", "Teenager", "Adult"]
user_name = input(f"Enter your full name:")
birth_year_str = input(f"Enter your birth year in range '1900 - 2024':")
birth_year = int(birth_year_str)
age = current_year - birth_year
hobbies = []


def generate_profile(age):
    if age in range(0, 12):
        return life_stage[0]
    if age in range(13, 19):
        return life_stage[1]
    if age >= 20:
        return life_stage[2]
    return age


while hobbies != loop_stop:
    hobbies_list = input(f"Enter a favorite hobby or type 'stop' to finish  ")
    hobbies.append(hobbies_list)
    count = count + 1

    if hobbies_list == loop_stop and len(hobbies) == 1:
        count = 0
        hobbies.clear()
        print(f"Profile Summary:\nName: {user_name}\nAge: {age}\nLife Stage: {generate_profile(age)}\nYou didn't "
              f"mention any hobbies ")
        break
    else:
        if hobbies_list == loop_stop and len(hobbies) > 2:
            hobbies.remove(loop_stop)
            nl = '\n -'
            print(f"Profile Summary:\nName: {user_name}\nAge: {age}\nLife Stage: {generate_profile(age)}\nFavorite "
                  f"hobbies ({count-1})\n -{nl.join(hobbies) }")
            break
    continue



