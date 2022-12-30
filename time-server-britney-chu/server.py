from datetime import datetime, time, date, timedelta
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/time", methods=["GET"])
def get_time():
    current = datetime.now().time()
    str_now = current.strftime( "%H:%M:%S")
    return str_now


@app.route("/date", methods=["GET"])
def get_date():
    date = datetime.now().date()
    str_date = date.strftime("%m-%d-%y")
    return str_date


@app.route("/age", methods=["POST"])
def find_age():
    in_data = request.get_json()
    time, status_code = find_diff(in_data)
    return jsonify(time), status_code


def find_diff(in_data):
    result = validate_new_date(in_data)
    if result is not True:
        return result, 400
    in_date = datetime(int(in_data['date'].split("/")[2]),
                       int(in_data['date'].split("/")[0]),
                       int(in_data['date'].split("/")[1]))
    current = datetime.now()
    diff = current - in_date
    years_diff = diff.days / 365
    return years_diff, 200


def validate_new_date(in_data):
    if type(in_data) is not dict:
        return "POST data was not a dictionary"
    expected_keys = ["date", "units"]
    for key in expected_keys:
        if key not in in_data:
            return "Key {} is missing from POST data".format(key)
    expected_types = [str, str]
    for key, ex_type in zip(expected_keys, expected_types):
        if type(in_data[key]) is not ex_type:
            return "Key {}'s value has the wrong data type".format(key)
    in_len = len(in_data['date'].split("/"))
    if in_len != 3:
        return "The date is not written in the correct format"
    return True


@app.route("/until_next_meal/<meal>", methods=["GET"])
def time_until_meal(meal):
    current_time = datetime.now().time()
    current_delta = timedelta(hours=int(current_time.hour),
                              minutes=int(current_time.minute),
                              seconds=int(current_time.second))
    breakfast_delta = timedelta(hours=9,
                                minutes=0,
                                seconds=0)
    lunch_delta = timedelta(hours=13,
                            minutes=0,
                            seconds=0)
    dinner_delta = timedelta(hours=20,
                             minutes=0,
                             seconds=0)
    if meal == "breakfast":
        if (current_delta - breakfast_delta).seconds > 0:
            # after breakfast
            return jsonify(24 - (current_delta - breakfast_delta).seconds/3600)
        else:
            # before breakfast
            return jsonify((current_delta - breakfast_delta).seconds / 3600)
    if meal == "lunch":
        if (current_delta - lunch_delta).seconds > 0:
            # after lunch
            return jsonify(24 - (current_delta - lunch_delta).seconds / 3600)
        else:
            # before lunch
            return jsonify((current_delta - lunch_delta).seconds / 3600)
    if meal == "dinner":
        if (current_delta - dinner_delta).seconds > 0:
            # after lunch
            return jsonify(24 - (current_delta - dinner_delta).seconds / 3600)
        else:
            # before lunch
            return jsonify((current_delta - dinner_delta).seconds / 3600)


if __name__ == "__main__":
    app.run()
