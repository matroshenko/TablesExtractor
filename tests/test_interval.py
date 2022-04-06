from unittest import TestCase, main

import context
from lib.interval import Interval, sort_and_merge_intervals


class IntervalTestCase(TestCase):
    def test_merge_intervals(self):
        intervals = [
            Interval(0, 4),
            Interval(6, 9),
            Interval(2, 5),
            Interval(7, 8),
            Interval(1, 3)
        ]
        result = sort_and_merge_intervals(intervals)
        expected_result = [Interval(0, 5), Interval(6, 9)]
        
        self.assertListEqual(result, expected_result)


if __name__ == '__main__':
    main()