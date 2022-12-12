class Vessel:
    def __init__(self, uid):
        # The unique identifier for a vessel
        # Set by Generator
        self.uid: int = uid

        # The destination of the vessel
        # Set at AnchorPoint and used at confluences
        self.destination_dock: str = None

        # self.creation_time = creation_time


class CrudeOilTanker(Vessel):
    vessel_type = "Crude Oil Tanker"
    surface_area = 11007
    avg_velocity = 10.7
    max_velocity = 15.4
    prob = 0.28


class BulkCarrier(Vessel):
    vessel_type = "Bulk Carrier"
    surface_area = 5399
    avg_velocity = 12
    max_velocity = 15.6
    prob = 0.22


class TugBoat(Vessel):
    vessel_type = "Tug Boat"
    surface_area = 348
    avg_velocity = 7.8
    max_velocity = 10.6
    prob = 0.33


class SmallCargoFreighter(Vessel):
    vessel_type = "Small Cargo Freighter"
    surface_area = 1265
    avg_velocity = 6.4
    max_velocity = 9.8
    prob = 0.17


ALL_VESSELS = [
    CrudeOilTanker,
    BulkCarrier,
    TugBoat,
    SmallCargoFreighter
]
