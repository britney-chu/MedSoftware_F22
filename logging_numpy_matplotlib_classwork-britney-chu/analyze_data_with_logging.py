import logging


def analyze_signal(filename):
    in_file = open(filename, 'r')
    number_of_positives = 0
    total_number = 0
    while True:
        new_data = in_file.read(1)
        total_number += 1
        if new_data == "+":
            number_of_positives += 1
        elif new_data == "0":
            logging.warning("The data point {} was a 0".format(total_number))
        elif new_data == "\n":
            break
        elif new_data == "-":
            logging.info("The data point {} was a "-"".format(total_number))
        else:
            logging.error("The data point {} was not '+', '-', or '-'".format(total_number))
    percent_positive = round(number_of_positives / total_number * 100, 1)
    return percent_positive


if __name__ == '__main__':
    logging.basicConfig(filename = "signal_analysis_log.log", filemode = 'w', level = logging.INFO)
    answer = analyze_signal("signal.txt")
    print("Percent positive = {}".format(answer))
