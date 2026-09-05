from app.rag.ingest import (
    ingest_all_rag_data,
)


def main():
    total = ingest_all_rag_data()

    print(
        "Ingest thành công."
    )

    print(
        "Tổng chunks đã lưu:",
        total,
    )


if __name__ == "__main__":
    main()