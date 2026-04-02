from datetime import time, datetime
from domain.place import Place
from domain.category import Category


class ShopPlace(Place):
    """
    가게/음식점/카페 장소 구현체
    Java의 ShopPlace extends Place 와 동일한 구조
    예) 세종전통시장, Cafe Gaga, 모시울 카페
    """

    def __init__(self, place_id: str, name: str,
                 lat: float, lng: float, address: str,
                 category: Category,
                 open_time: time, close_time: time,
                 phone: str = "",
                 is_franchise: bool = False):
        super().__init__(place_id, name, lat, lng, category, address)
        self._open_time   = open_time
        self._close_time  = close_time
        self._phone       = phone
        self._is_franchise = is_franchise

    # ── 추상 메서드 구현 ────────────────────────────────────────────────────
    def get_description(self) -> str:
        status = "영업중 ✅" if self.is_open() else "영업종료 ❌"
        return (
            f"{self._name}\n"
            f"  위치  : {self._address}\n"
            f"  영업  : {self._open_time.strftime('%H:%M')} ~ "
            f"{self._close_time.strftime('%H:%M')}\n"
            f"  현재  : {status}\n"
            f"  별점  : ★{self._rating:.1f}\n"
            f"  전화  : {self._phone or '정보 없음'}"
        )

    def get_place_type(self) -> str:
        return str(self._category)

    # ── 영업 여부 ───────────────────────────────────────────────────────────
    def is_open(self) -> bool:
        """현재 시각 기준 영업 중인지 판단"""
        now = datetime.now().time()
        return self._open_time <= now <= self._close_time

    # ── Getters ─────────────────────────────────────────────────────────────
    @property
    def open_time(self):   return self._open_time

    @property
    def close_time(self):  return self._close_time

    @property
    def phone(self):         return self._phone

    @property
    def is_franchise(self):  return self._is_franchise
