def mudae_time_to_seconds(string: str):
    clean_str = string.replace("%", "")

    split_string = clean_str.split("h")
    if len(split_string) > 1:
        return ((int(split_string[0]) * 60) + int(split_string[1])) * 60

    return int(split_string[0]) * 60
