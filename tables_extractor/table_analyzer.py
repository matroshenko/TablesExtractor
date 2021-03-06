import os

import tensorflow as tf

from tables_extractor.grid_structure import GridStructure
from tables_extractor.rect import Rect
from tables_extractor import models_manager


class TableAnalyzer(object):
    def __init__(self, page_objects, table_rect):
        self._page_objects = page_objects
        self._table_rect = table_rect

    def analyze(self):
        table_image = self._page_objects.page_image.crop(self._table_rect.as_tuple())
        table_image_array = tf.keras.utils.img_to_array(table_image, dtype='int32')
        outputs = models_manager.analysis_model(tf.constant(table_image_array))
        grid_structure = self._create_grid_structure(outputs['h_positions'].numpy(), outputs['v_positions'].numpy())
        cells_grid_rects = self._create_cells_grid_rects(outputs['cells_grid_rects'].numpy())
        return grid_structure, cells_grid_rects

    def _create_grid_structure(self, h_positions_array, v_positions_array):
        shifted_h_positions = [pos + self._table_rect.top for pos in h_positions_array]
        shifted_v_positions = [pos + self._table_rect.left for pos in v_positions_array]
        return GridStructure(
            [self._table_rect.top] + shifted_h_positions + [self._table_rect.bottom],
            [self._table_rect.left] + shifted_v_positions + [self._table_rect.right])

    def _create_cells_grid_rects(self, cells_grid_rects_array):
        result = []
        for cell_grid_rect in cells_grid_rects_array:
            left, top, right, bottom = cell_grid_rect
            result.append(Rect(left, top, right, bottom))
        return result