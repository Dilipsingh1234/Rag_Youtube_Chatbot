from urllib.parse import urlparse, parse_qs


def extract_video_id(url_or_id: str) -> str:
    value = url_or_id.strip()

    if "youtube.com" in value or "youtu.be" in value:
        parsed = urlparse(value)

        if "youtube.com" in parsed.netloc:
            return parse_qs(parsed.query).get("v", [""])[0]

        if "youtu.be" in parsed.netloc:
            return parsed.path.lstrip("/")

    return value