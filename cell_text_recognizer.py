from collections import deque


class Line(object):
    def __init__(self, word):
        self.vert_interval = word.rect.get_vert_interval()
        self.words = [word]

    def append_word(self, word):
        self.vert_interval |= word.rect.get_vert_interval()
        self.words.append(word)

    def get_text(self):
        sorted_words = sorted(self.words, key=lambda word: word.rect.left)
        return ' '.join(word.text for word in sorted_words)


class CellTextRecognizer(object):
    def __init__(self, page_objects, cell_rect):
        self._page_objects = page_objects
        self._cell_rect = cell_rect

    def recognize(self):
        words = self.get_overlapping_words()
        lines = self.split_words_by_lines(words)
        return '\n'.join(line.get_text() for line in lines)

    def get_overlapping_words(self):
        words = self._page_objects.words

        result = []
        for word in words:
            overlap_area = word.rect.get_overlap_area(self._cell_rect)
            if 2 * overlap_area > word.rect.get_area():
                result.append(word)

        return result

    def split_words_by_lines(self, words):
        if not words:
            return []
        
        sorted_words = sorted(words, key=lambda word: word.rect.top)
        sorted_words_to_distribute = deque(sorted_words)
        lines = [ Line(sorted_words_to_distribute.popleft()) ]

        while sorted_words_to_distribute:
            next_word = sorted_words_to_distribute.popleft()
            if next_word.rect.top < lines[-1].vert_interval.end:
                lines[-1].append_word(next_word)
            else:
                lines.append(Line(next_word))

        return lines