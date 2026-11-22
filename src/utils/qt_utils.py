from config import STYLES_DIR


def get_stylesheet() -> str:
    styles = []

    for qss_path in STYLES_DIR.glob("*.qss"):
        qss = qss_path.read_text(encoding="utf-8")
        styles.append(qss)

    return "\n".join(styles)
