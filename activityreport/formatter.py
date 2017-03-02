import datetime


def _element_to_string(date_time_list_element):
    # convert datetime.* to string

    def _a_day_of_week_en_to_ja(date_time):
        return ['月', '火', '水', '木', '金', '土', '日'][date_time.weekday()]

    for i, element in enumerate(date_time_list_element):

        if isinstance(element, datetime.datetime):
            # format: '2017/01/01(月) 00:00:00'
            date_time_list_element[i] = element.strftime(
                '%Y/%m/%d(' + _a_day_of_week_en_to_ja(element) + ') %H:%M:%S')
        elif isinstance(element, datetime.date):
            # format: '2017/01/01(月)'
            date_time_list_element[i] = element.strftime(
                '%Y/%m/%d(' + _a_day_of_week_en_to_ja(element) + ')')
        elif isinstance(element, datetime.time):
            # format: '00:00:00'
            date_time_list_element[i] = element.strftime('%H:%M:%S')

    return date_time_list_element


def _ret_gfm(date_time_list):
    transposed_date_time_list = list(map(list, zip(*date_time_list)))

    gfm = ''
    for x in date_time_list:
        gfm += '|'
        for j, y in enumerate(x):
            if isinstance(y, int):
                # get maximum number of digits
                max_number_of_digits = len(
                    str(max(transposed_date_time_list[j])))
                gfm += str(y).rjust(max_number_of_digits, ' ')  # align right
                gfm += '|'
            else:
                # get length of maximum length str
                max_str_length = len(
                    max(transposed_date_time_list[j], key=len))
                gfm += str(y).ljust(max_str_length, ' ')  # align left
                gfm += '|'

        gfm += '\n'

    return gfm


def to_gfm_table(date_time_list):
    # convert tuple into list
    for i, element in enumerate(date_time_list):
        date_time_list[i] = list(date_time_list[i])
        date_time_list[i] = _element_to_string(date_time_list[i])

    return _ret_gfm(date_time_list)
