import mongoengine


class SimulationModel(mongoengine.Document):

    simulation_time = mongoengine.DateTimeField(required=True)
