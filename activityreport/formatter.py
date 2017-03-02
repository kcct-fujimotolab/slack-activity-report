import datetime
import math


def _element_to_string(dateTimeList_element):
    # convert datetime.* to string

    def _aDayOfWeek_en_to_ja(dateTime):
        if dateTime.strftime("%A") == "Monday":
            return "月"
        elif dateTime.strftime("%A") == "Tuesday":
            return "火"
        elif dateTime.strftime("%A") == "Wednesday":
            return "水"
        elif dateTime.strftime("%A") == "Thursday":
            return "木"
        elif dateTime.strftime("%A") == "Friday":
            return "金"
        elif dateTime.strftime("%A") == "Saturday":
            return "土"
        elif dateTime.strftime("%A") == "Sunday":
            return "日"

    for (i, element) in enumerate(dateTimeList_element):

        if isinstance(element, datetime.datetime):
            # format: "2017/01/01(月) 00:00:00"
            dateTimeList_element[i] = element.strftime(
                "%Y/%m/%d(" + _aDayOfWeek_en_to_ja(element) + ") %H:%M:%S")
        elif isinstance(element, datetime.date):
            # format: "2017/01/01(月)"
            dateTimeList_element[i] = element.strftime(
                "%Y/%m/%d(" + _aDayOfWeek_en_to_ja(element) + ")")
        elif isinstance(element, datetime.time):
            # format: "00:00:00"
            dateTimeList_element[i] = element.strftime("%H:%M:%S")

    return dateTimeList_element


def _retGFM(dateTimeList):
    transposedDateTimeList = list(map(list, zip(*dateTimeList)))

    gfm = ""
    for x in dateTimeList:
        gfm += "|"
        for j, y in enumerate(x):
            if isinstance(y, int):
                # get maximum number of digits
                maxNumberOfDigits = int(math.log10(
                    max(transposedDateTimeList[j])) + 1)
                gfm += str(y).rjust(maxNumberOfDigits, ' ')  # align right
                gfm += "|"
            else:
                # get length of maximum length str
                maxStrLength = len(max(transposedDateTimeList[j], key=len))
                gfm += str(y).ljust(maxStrLength, ' ')  # align left
                gfm += "|"

        gfm += "\n"

    return gfm


def to_gfm_table(dateTimeList):
    # convert tuple into list
    for i, element in enumerate(dateTimeList):
        dateTimeList[i] = list(dateTimeList[i])
        dateTimeList[i] = _element_to_string(dateTimeList[i])

    _retGFM(dateTimeList)
