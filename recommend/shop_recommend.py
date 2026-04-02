from domain.place import Place
from domain.category import Category


class ShopRecommend:
    """
    상점 추천 클래스
    - 반경 필터, 프렌차이즈 제외, 카테고리 필터, 별점순 정렬
    """

    def __init__(self, places: list[Place]):
        self._places = places

    def recommend(
        self,
        user_lat: float,
        user_lng: float,
        radius_km: float = 2.0,
        category: Category = None,
        local_only: bool = True,
    ) -> list[Place]:
        """
        상점 추천 메인 메서드

        :param user_lat:   사용자 위도
        :param user_lng:   사용자 경도
        :param radius_km:  추천 반경 (기본 2km)
        :param category:   카테고리 필터 (None이면 전체)
        :param local_only: True면 프렌차이즈 제외
        :return:           별점 내림차순 장소 리스트
        """
        result = self._places

        # 반경 필터
        result = [p for p in result if p.distance_to(user_lat, user_lng) <= radius_km]

        # 프렌차이즈 제외
        if local_only:
            result = [p for p in result if not getattr(p, "is_franchise", False)]

        # 카테고리 필터
        if category is not None:
            result = [p for p in result if p.category == category]

        # 별점 내림차순
        result.sort(key=lambda p: p.rating, reverse=True)

        return result
