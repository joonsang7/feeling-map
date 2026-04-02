import sys
sys.stdout.reconfigure(encoding="utf-8")

from datetime import time

from domain.category import Category
from domain.shop_place import ShopPlace
from map_facade import MapFacade




def main():
    print("=== feeling-map 테스트 ===\n")

    places = [
        ShopPlace(
            place_id="S001", name="Cafe Gaga 세종점",
            lat=36.5988, lng=127.2987,
            address="세종시 조치원읍 새내로 76",
            category=Category.CAFE,
            open_time=time(9, 0), close_time=time(22, 0),
            phone="044-868-0706",
            is_franchise=False,
        ),
        ShopPlace(
            place_id="S002", name="세종전통시장",
            lat=36.6004, lng=127.2996,
            address="세종시 조치원읍 조치원8길 42",
            category=Category.FOOD,
            open_time=time(6, 0), close_time=time(20, 0),
            phone="044-868-4209",
            is_franchise=False,
        ),
        ShopPlace(
            place_id="S003", name="모시울 카페",
            lat=36.5952, lng=127.3019,
            address="세종시 조치원읍 장안로 74",
            category=Category.CAFE,
            open_time=time(10, 0), close_time=time(22, 0),
            phone="010-8370-2663",
            is_franchise=False,
        ),
        ShopPlace(
            place_id="S004", name="스타벅스 조치원점",
            lat=36.6001, lng=127.2980,
            address="세종시 조치원읍 스타벅스로 1",
            category=Category.CAFE,
            open_time=time(8, 0), close_time=time(22, 0),
            is_franchise=True,  # 프렌차이즈
        ),
        ShopPlace(
            place_id="S005", name="조치원 문화정원",
            lat=36.5990, lng=127.2995,
            address="세종시 조치원읍 문화로 10",
            category=Category.LEISURE,
            open_time=time(9, 0), close_time=time(18, 0),
            is_franchise=False,
        ),
    ]

    for p in places:
        if p.category == Category.CAFE:
            p.rating = 4.6 if p.name == "Cafe Gaga 세종점" else 4.5 if p.name == "모시울 카페" else 3.9
        elif p.category == Category.FOOD:
            p.rating = 4.2
        elif p.category == Category.LEISURE:
            p.rating = 4.4

    facade = MapFacade(places)

    # 조치원역 기준
    station_lat, station_lng = 36.6010, 127.2973

    print("[ 상점 추천 - 전체 / 프렌차이즈 제외 ]")
    shops = facade.recommend_shops(station_lat, station_lng, radius_km=2.0)
    for p in shops:
        print(f"  {p.get_summary()}")

    print("\n[ 상점 추천 - 카페만 ]")
    cafes = facade.recommend_shops(station_lat, station_lng, category=Category.CAFE)
    for p in cafes:
        print(f"  {p.get_summary()}")

    print("\n[ 동선 추천 - 기본 코스 (식사→카페→여가) ]")
    route = facade.recommend_route(station_lat, station_lng)
    for i, p in enumerate(route, 1):
        print(f"  {i}번째. {p.get_summary()}")

    print("\n[ 동선 추천 - 커스텀 코스 (카페→여가) ]")
    custom_route = facade.recommend_route(
        station_lat, station_lng,
        course=[Category.CAFE, Category.LEISURE]
    )
    for i, p in enumerate(custom_route, 1):
        print(f"  {i}번째. {p.get_summary()}")


if __name__ == "__main__":
    main()
