__all__ = ["imgur"]

from .imgur import ImgurEx

_ALL_CLASSES = [class_ for name, class_ in globals().items() if name.endswith('Ex')] #Based on youtube-dl

def gen_extractors():
    """
    Return a list of extractor instances.
    """
    return [class_() for class_ in  _ALL_CLASSES]
