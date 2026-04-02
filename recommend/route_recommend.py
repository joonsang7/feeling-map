from domain.place import Place
from domain.category import Category


DEFAULT_COURSE = [Category.FOOD, Category.CAFE, Category.LEISURE]


class RouteRecommend:
    """
    동선 추천 클래스
    - 코스 템플릿(카테고리 순서)에 따라 장소를 이어붙임
    - 각 단계마다 이전 장소와 가장 가까운 곳을 선택
    - 단계 간 최대 거리를 초과하면 해당 단계는 건너뜀
    """

    def __init__(self, places: list[Place]):
        self._places = places

    def recommend(
        self,
        start_lat: float,
        start_lng: float,
        course: list[Category] = None,
        max_step_km: float = 1.5,
        local_only: bool = True,
    ) -> list[Place]:
        """
        동선 추천 메인 메서드

        :param start_lat:   출발 위도
        :param start_lng:   출발 경도
        :param course:      카테고리 순서 리스트 (기본: 식사→카페→여가)
        :param max_step_km: 단계 간 최대 허용 거리 (기본 1.5km)
        :param local_only:  True면 프렌차이즈 제외
        :return:            코스 순서대로 선택된 장소 리스트
        """
        if course is None:
            course = DEFAULT_COURSE

        candidates = self._places
        if local_only:
            candidates = [p for p in candidates if not getattr(p, "is_franchise", False)]

        route = []
        current_lat = start_lat
        current_lng = start_lng

        for category in course:
            same_category = [p for p in candidates if p.category == category]
            same_category = [p for p in same_category if p not in route]

            if not same_category:
                continue

            nearest = min(same_category, key=lambda p: p.distance_to(current_lat, current_lng))
            dist = nearest.distance_to(current_lat, current_lng)

            if dist > max_step_km:
                continue

            route.append(nearest)
            current_lat = nearest.lat
            current_lng = nearest.lng

        return route
