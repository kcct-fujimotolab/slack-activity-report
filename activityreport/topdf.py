from ArrayImage import TextImage
import datetime

def topdf(intime, outtime, description):
    intimeint = [period30min(d.hour, d.minute) for d in intime]
    outtimeint = [period30min(d.hour, d.minute) for d in outtime]
    weekday = [num_to_day(d.weekday()) for d in intime]
    fhours = [hours(tin[0], tin[1], tout[0], tout[1]) for tin, tout in zip(intimeint, outtimeint)]
    #test output
    print(intimeint)
    print(outtimeint)
    print(weekday)
    print(fhours)

def period30min(hour, minute):
    if minute < 15:
        return hour, 0
    elif minute < 45:
        return hour, 30
    else:
        return hour+1, 0

def num_to_day(daynum):
    weekday = ["月", "火", "水", "木", "金", "土", "日"]
    return weekday[daynum]

def hours(inhour, inminute, outhour, outminute):
    if inminute > outminute:
        return (outhour - inhour - 1) + 0.5
    else:
        return (outhour - inhour) + (outminute - inminute)/60.0

if __name__ == '__main__':
    testtime = '2016-11-7 15:18:00'
    tdatetime = datetime.datetime.strptime(testtime, '%Y-%m-%d %H:%M:%S')
    tdatetime2 = datetime.datetime.now()
    topdf([tdatetime], [tdatetime2], "hello")
    print(tdatetime.weekday())
