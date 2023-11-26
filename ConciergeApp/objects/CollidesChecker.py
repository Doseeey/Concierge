import datetime
from ConciergeApp.models.ReservationModel import ReservationModel


class CollidesChecker:
    def __init__(self, listOfModelsBooked: list[ReservationModel], modelToBook: ReservationModel) -> None:
        self.timelines = []
        self.modelToBookTimeline = None
        modelToBook.date_from = modelToBook.date_from - datetime.timedelta(hours=1)
        modelToBook.date_to = modelToBook.date_to - datetime.timedelta(hours=1)
        self.createTimelineArrays(listOfModelsBooked, modelToBook)
        self.canBeBooked = self.checkCollisions()
        modelToBook.date_from = modelToBook.date_from + datetime.timedelta(hours=1)
        modelToBook.date_to = modelToBook.date_to + datetime.timedelta(hours=1)
        
    def createTimelineArrays(self, listOfModels, modelToBook: ReservationModel):
        for model in listOfModels:
            model: ReservationModel
            timeline = self._createTimeline(model)
            self.timelines.append(timeline)
            
        self.modelToBookTimeline = self._createTimeline(modelToBook)
            
    def _createTimeline(self, model):
        timeline = [0 for x in range(4*24)]
        startIndex = model.date_from.hour * 4 + model.date_from.minute // 15
        endIndex = model.date_to.hour * 4 + model.date_to.minute // 15
        for index in range(startIndex, endIndex):
            timeline[index] = 1
        return timeline
    
    def checkCollisions(self):
        for timelineTuple, modelToBookTimeline in zip(zip(*self.timelines), self.modelToBookTimeline):
            if len(list(filter(None, timelineTuple))) >= 2 and modelToBookTimeline:
                return False
        return True
