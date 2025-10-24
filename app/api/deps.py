from app.services.extractor import VeranstaltungExtractor


# Простой DI-фабричный метод


def get_extractor() -> VeranstaltungExtractor:
    return VeranstaltungExtractor()