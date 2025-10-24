import re
from typing import Optional, Tuple, Iterable


def kw_min_max_from_any(value) -> Tuple[Optional[int], Optional[int]]:
    """
    Принимает: int | str ('41,42' / '41-46' / 'KW 41–46') | Iterable[int|str]
    Возвращает (min, max) или (n, None) или (None, None).
    """
    if value is None:
        return None, None
    # список/кортеж
    if isinstance(value, (list, tuple)):
        nums = [int(x) for x in value if str(x).isdigit()]
        if not nums:
            return None, None
        return min(nums), max(nums)
    # одиночное число
    if isinstance(value, int):
        return value, None
    # строка: вытаскиваем все 1–2-значные числа
    s = str(value).replace("–", "-").replace("—", "-")
    nums = [int(n) for n in re.findall(r"\d{1,2}", s)]
    if not nums:
        return None, None
    if len(nums) == 1:
        return nums[0], None
    return min(nums), max(nums)