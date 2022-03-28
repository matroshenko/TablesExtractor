from interval import Interval


class Rect(object):
  def __init__(self, left, top, right, bottom):
    assert left <= right and top <= bottom
    self.left = left
    self.top = top
    self.right = right
    self.bottom = bottom

  def is_empty(self):
    return self.left == self.right or self.top == self.bottom

  def get_width(self):
    return self.right - self.left

  def get_height(self):
    return self.bottom - self.top

  def get_area(self):
    return self.get_width() * self.get_height()

  def as_tuple(self):
    return (self.left, self.top, self.right, self.bottom)

  def contains(self, other):
    return (
      self.left <= other.left and other.right <= self.right
      and self.top <= other.top and other.bottom <= self.bottom
    )

  def intersects(self, other):
    return self.overlaps_horizontally(other) and self.overlaps_vertically(other)

  def overlaps_horizontally(self, other):
    return self.left < other.right and other.left < self.right
  
  def overlaps_vertically(self, other):
    return self.top < other.bottom and other.top < self.bottom

  def get_overlap_area(self, other):
    left = max(self.left, other.left)
    top = max(self.top, other.top)
    right = min(self.right, other.right)
    bottom = min(self.bottom, other.bottom)
    return max(0, right - left) * max(0, bottom - top)

  def get_horz_interval(self):
    return Interval(self.left, self.right)

  def get_vert_interval(self):
    return Interval(self.top, self.bottom)

  def __eq__(self, other):
    return self.as_tuple() == other.as_tuple()

  def __lt__(self, other):
    return self.as_tuple() < other.as_tuple()

  def __or__(self, other):
    left = min(self.left, other.left)
    top = min(self.top, other.top)
    right = max(self.right, other.right)
    bottom = max(self.bottom, other.bottom)
    return Rect(left, top, right, bottom)

  def __repr__(self):
    return '[{}, {}, {}, {}]'.format(self.left, self.top, self.right, self.bottom)

  def __hash__(self):
    return hash(self.as_tuple())