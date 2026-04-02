from enum import Enum

class Category(Enum):
    CAFE     = "카페"
    MARKET   = "시장"
    CULTURE  = "문화/예술"
    LEISURE  = "여가"
    FOOD     = "음식점"
    HISTORY  = "역사/관광"

    def __str__(self):
        return self.value
