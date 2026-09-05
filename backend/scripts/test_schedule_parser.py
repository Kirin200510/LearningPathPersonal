from app.rag.schedule_parser import (
    parse_schedule_preference,
)


def main():

    result = parse_schedule_preference(
        "Tôi rảnh thứ 3 và thứ 7 "
        "từ 5 giờ chiều tới 9 giờ tối"
    )

    print(result)


if __name__ == "__main__":
    main()