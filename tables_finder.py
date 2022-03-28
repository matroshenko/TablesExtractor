import math

import tensorflow as tf
import PIL

from rect import Rect


class TablesFinder(object):
    def __init__(self, page_objects):
        self._page_objects = page_objects
        self._detection_model = tf.saved_model.load('models/tables_detector_v2/')['prediction_pipeline']

    def find(self):
        result = self._find_rects_on_page_image()
        return [self._compress_rect_by_text(rect) for rect in result]

    def _find_rects_on_page_image(self):
        page_image = self._page_objects.page_image
        original_width, original_height = page_image.size
        resized_page_image = self._resize_image_for_detection_model(page_image)
        resized_width, resized_height = resized_page_image.size

        scale = math.sqrt(resized_width / original_width * resized_height / original_height)
        resized_page_image_array = tf.keras.utils.img_to_array(resized_page_image, dtype='float32')
        outputs = self._detection_model(resized_page_image_array)

        boxes = outputs['output/boxes:0']
        scores = outputs['output/scores:0']

        # Convert to original page image coordinates.
        boxes = boxes / scale

        rects = []
        for box, score in zip(boxes, scores):
            left, top, right, bottom = box
            if score >= 0.5:
                rects.append(Rect(left, top, right, bottom))

        return rects

    def _resize_image_for_detection_model(self, image):
        short_edge = 800
        max_size = 1333

        w, h = image.size
        scale = short_edge / min(w, h)
        if h < w:
            newh, neww = short_edge, scale * w
        else:
            newh, neww = scale * h, short_edge
        if max(newh, neww) > max_size:
            scale = max_size / max(newh, neww)
            newh = newh * scale
            neww = neww * scale
        newh = math.ceil(newh)
        neww = math.ceil(neww)

        return image.resize((neww, newh), PIL.Image.BILINEAR)

    def _compress_rect_by_text(self, rect):
        words = self._page_objects.words

        overlapping_words_rects = []
        for word in words:
            word_rect = word.rect
            overlap_area = word_rect.get_overlap_area(rect)
            if 2 * overlap_area > word_rect.get_area():
                overlapping_words_rects.append(word_rect)
        
        if not overlapping_words_rects:
            return rect

        compressed_rect = overlapping_words_rects[0]
        for i in range(1, len(overlapping_words_rects)):
            compressed_rect |= overlapping_words_rects[i]

        return compressed_rect