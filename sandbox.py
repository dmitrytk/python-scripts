from dataclasses import dataclass, field
from typing import List


@dataclass
class WellData:
    name: str
    alt: float
    x: float
    y: float
    md: float
    zone_top: List[float] = field(default_factory=list)
    zone_bot: List[float] = field(default_factory=list)
    zk: List[float] = field(default_factory=list)
    zp: List[float] = field(default_factory=list)

    def __str__(self):
        return f'"{self.name}" {self.alt} {self.x} {self.y} {self.md}'


well = WellData(456, 454, 454, 545, 454, 454)
a = str(well)
print(a)
