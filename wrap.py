from typing import Iterable, List, Tuple


class RectWrappingCollection:
    def _get_lines(self) -> [List[Tuple[int, float, float, float]], float, float]:
        cum_width = 0
        cum_space = 0
        cum_total_width = 0
        last_min_space = 0
        max_height = 0
        line = []

        for i, (width, height, min_space) in enumerate(zip(self._widths, self._heights, self._min_spaces)):

            if (cum_total_width + width > self._wrap) or i == self.count:
                yield line, max_height, cum_total_width, cum_width
                cum_width = 0
                cum_space = 0
                last_min_space = 0
                max_height = 0
                line = []
            space = max(min_space, last_min_space)
            cum_space += space
            cum_width += width
            cum_total_width = cum_width + cum_space
            max_height = max(height, max_height)
            last_min_space = min_space
            line.append((i, width, height, space))
        yield line, max_height, cum_total_width, cum_width

    def _process_lines(self):
        y0 = 0
        for i, (line, max_height, cum_total_width, cum_width) in enumerate(self._get_lines()):
            if self._line_fixed_height:
                y0 += self._line_fixed_height * self._line_height
            else:
                y0 += max_height * self._line_height

            x0 = 0
            ov_space = None
            if self._text_align == 1:
                x0 = (self._wrap - cum_total_width) / 2.0
            if self._text_align == 2:
                x0 = self._wrap - cum_total_width
            if self._text_align == 3:
                ov_space = (self._wrap - cum_width) / len(line)

            for j, (k, width, height, space) in enumerate(line):
                y1 = y0 - height
                yield (x0, y1)
                x0 += width + (ov_space or space)

    def set_wrap(self, value):
        self._wrap = value

    def set_line_fixed_height(self, value):
        self._line_fixed_height = value

    def set_line_height(self, value):
        self._line_height = value

    def set_align(self, value):
        self._text_align = value

    def get_sizes(self):
        yield from self._process_lines()

    @property
    def count(self) -> int:
        return len(self._widths)

    def __init__(self,
                 wrap: float = -1,
                 widths: Iterable[float] = None,
                 heights: Iterable[float] = None,
                 min_spaces: Iterable[float] = None,
                 line_fixed_height: float = 0,
                 line_height: float = 1.2,
                 text_align: int = 0,
                 default_min_space: float = 10.0,
                 ):
        self._wrap: float = wrap
        self._widths: List[float] = list(widths) if widths else []
        self._heights: List[float] = list(heights) if heights else []
        self._min_spaces: List[float] = list(min_spaces) if min_spaces else []

        self._line_fixed_height = line_fixed_height
        self._line_height = line_height
        self._text_align = text_align

        self._min_spaces: List[float] = []
        if min_spaces:
            self._min_spaces = list(min_spaces)
        else:
            if self.count:
                self._min_spaces = [[default_min_space] * self.count]

        self.default_min_space: float = default_min_space

    def add_rect(self, width: float, height: float, min_space: float = None):
        self._widths.append(width)
        self._heights.append(height)
        self._min_spaces.append(min_space if min_space else self.default_min_space)
