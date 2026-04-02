from domain.place import Place
from domain.category import Category
from recommend.shop_recommend import ShopRecommend
from recommend.route_recommend import RouteRecommend


class MapFacade:
    """
    feeling-map 단일 진입점
    외부(app.py, 테스트 등)에서는 이 클래스만 사용
    """

    def __init__(self, places: list[Place]):
        self._places = places
        self._shop_recommend = ShopRecommend(places)
        self._route_recommend = RouteRecommend(places)

    def recommend_shops(
        self,
        user_lat: float,
        user_lng: float,
        radius_km: float = 2.0,
        category: Category = None,
        local_only: bool = True,
    ) -> list[Place]:
        """주변 상점 추천 (별점 내림차순)"""
        return self._shop_recommend.recommend(
            user_lat, user_lng, radius_km, category, local_only
        )

    def recommend_route(
        self,
        start_lat: float,
        start_lng: float,
        course: list[Category] = None,
        max_step_km: float = 1.5,
        local_only: bool = True,
    ) -> list[Place]:
        """동선 추천 (코스 순서대로 가장 가까운 장소 연결)"""
        return self._route_recommend.recommend(
            start_lat, start_lng, course, max_step_km, local_only
        )
