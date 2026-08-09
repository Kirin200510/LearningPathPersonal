
def build_context(points) -> str:
    context_parts: list[str] = []

    for index, point in enumerate(points, start=1):
        payload = point.payload or {}

        text = payload.get("text")

        if not text:
            continue

        context_part = (
            f"[Context {index}]\n"
            f"{text}"
        )

        context_parts.append(context_part)

    return "\n\n".join(context_parts)