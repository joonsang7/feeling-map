from abc import ABC, abstractmethod
import math
from domain.category import Category


class Place(ABC):
    """
    장소 추상 클래스
    Java의 abstract class Place 와 동일한 구조
    모든 장소(카페, 시장, 문화공간 등)의 공통 뼈대
    """

    def __init__(self, place_id: str, name: str,
                 lat: float, lng: float,
                 category: Category, address: str):
        self._place_id  = place_id
        self._name      = name
        self._lat       = lat
        self._lng       = lng
        self._category  = category
        self._address   = address
        self._rating    = 0.0

    # ── 추상 메서드: 서브클래스가 반드시 구현 ──────────────────────────────
    @abstractmethod
    def get_description(self) -> str:
        """장소 상세 설명 반환 — 서브클래스마다 다르게 구현"""
        pass

    @abstractmethod
    def get_place_type(self) -> str:
        """장소 타입 이름 반환 (예: '카페', '문화공간')"""
        pass

    # ── 공통 메서드 ────────────────────────────────────────────────────────
    def distance_to(self, user_lat: float, user_lng: float) -> float:
        """
        현재 위치에서 이 장소까지 거리(km) 계산
        Haversine 공식 사용
        ShopRecommend 거리순 정렬에서 호출됨
        """
        R = 6371.0
        d_lat = math.radians(self._lat - user_lat)
        d_lng = math.radians(self._lng - user_lng)
        a = (math.sin(d_lat / 2) ** 2
             + math.cos(math.radians(user_lat))
             * math.cos(math.radians(self._lat))
             * math.sin(d_lng / 2) ** 2)
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    def get_summary(self) -> str:
        """리스트 출력용 한 줄 요약"""
        return f"[{self.get_place_type()}] {self._name} (★{self._rating:.1f}) {self._address}"

    def __repr__(self):
        return f"Place(id={self._place_id}, name={self._name}, category={self._category})"

    # ── Getters / Setters ──────────────────────────────────────────────────
    @property
    def place_id(self):  return self._place_id

    @property
    def name(self):      return self._name

    @property
    def lat(self):       return self._lat

    @property
    def lng(self):       return self._lng

    @property
    def category(self):  return self._category

    @property
    def address(self):   return self._address

    @property
    def rating(self):    return self._rating

    @rating.setter
    def rating(self, value: float):
        if not 0.0 <= value <= 5.0:
            raise ValueError("별점은 0.0 ~ 5.0 사이여야 합니다.")
        self._rating = value
