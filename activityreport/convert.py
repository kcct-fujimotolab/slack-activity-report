from ArrayImage.ArrayImage import TextImage
import datetime
from PIL import Image


class Converter():

    def __init__(self, imgpath='report.png', font):
        self.font = font
        self.baseimage = Image.open(imgpath)
        self.nameXY = (1200, 400, 1500, 474)
        self.monthXY = (270, 400, 330, 474)
        self.intimeXY = (650, 550, 800, 2859)
        self.outtimeXY = (850, 550, 1100, 2859)
        self.weekdayXY = (500, 550, 594, 2859)
        self.hoursXY = (1100, 550, 1250, 2859)
        self.descriptionXY = (1270, 550, 2200, 2859)
        self.sumhoursXY = (1080, 2869, 1250, 2943)
        self.img = None

    def to_png(self, name, intime, outtime, descriptions):
        months = list(filter(lambda m: type(m) is not None, intime))
        month = ["{0:2d}".format(months[0].month)]
        intimeint = [self._period30min(d.hour, d.minute) if d is not None else (
            None, None) for d in intime]
        outtimeint = [self._period30min(d.hour, d.minute) if d is not None else (
            None, None) for d in outtime]
        weekday = [self._num_to_day(d.weekday())
                   if d is not None else '' for d in intime]
        fhours = [self._hours(tin[0], tin[1], tout[0], tout[1])
                  if tin[0] is not None else 0 for tin, tout in zip(intimeint, outtimeint)]

        intimestr = ["{0:2d}:{1:02d}".format(
            inhour, inmin) if inhour is not None else "" for inhour, inmin in intimeint]
        outtimestr = ["{0:2d}:{1:02d}".format(
            outhour, outmin) if outhour is not None else "" for outhour, outmin in outtimeint]
        hoursstr = ["{0:3.1f}".format(
            hour) if hour != 0 else "" for hour in fhours]
        sumhours = ["{0:3.1f}".format(sum(fhours))]
        descriptions = [
            description if description is not None else "" for description in descriptions]

        textimage = TextImage(
            font=self.font, occupancy=0.6)
        # test output
        self.img = textimage(self.baseimage, month, *self.monthXY)
        self.img = textimage(self.img, [name], *self.nameXY)
        self.img = textimage(self.img, intimestr, *self.intimeXY)
        self.img = textimage(self.img, outtimestr, *self.outtimeXY)
        self.img = textimage(self.img, weekday, *self.weekdayXY)
        self.img = textimage(self.img, hoursstr, *self.hoursXY)
        self.img = textimage(self.img, descriptions, *self.descriptionXY)
        self.img = textimage(self.img, sumhours, *self.sumhoursXY)

    def save(self, filename):
        self.img.save(filename)

    def _period30min(self, hour, minute):
        if minute < 15:
            return hour, 0
        elif minute < 45:
            return hour, 30
        else:
            return hour + 1, 0

    def _num_to_day(self, daynum):
        weekday = ['月', '火', '水', '木', '金', '土', '日']
        return weekday[daynum]

    def _hours(self, inhour, inminute, outhour, outminute):
        if inminute > outminute:
            return (outhour - inhour - 1) + 0.5
        else:
            return (outhour - inhour) + (outminute - inminute) / 60.0
