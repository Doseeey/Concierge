from datetime import datetime, timedelta


def makeHoursList():
    result = []
    for number in range(24):
        result.append((f"{number:02d}:00", f"{number:02d}:00"))
        result.append((f"{number:02d}:15", f"{number:02d}:15"))
        result.append((f"{number:02d}:30", f"{number:02d}:30"))
        result.append((f"{number:02d}:45", f"{number:02d}:45"))
        
    return result

def makeNumberOfGuestsList():
    result = []
    for number in range(1, 7):
        if number == 1:
            result.append((number, f"{number} osoba"))
        elif number > 1 and number < 5:
            result.append((number, f"{number} osoby"))
        else:
            result.append((number, f"{number} osób"))
            
    return result

def findClosestReservationHour():
    quarters = [15, 30, 45, 60]
    now = datetime.now()
    minutes = now.minute
    closest = next(filter(lambda x: x > minutes, quarters))
    closestQuarterTimedelta = abs(closest - minutes)
    delta = timedelta(minutes=closestQuarterTimedelta)
    result = now + delta
    return f"{result.hour}:{result.minute}"
