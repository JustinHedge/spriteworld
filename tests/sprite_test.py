# Copyright 2019 DeepMind Technologies Limited.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
# python2 python3
"""Tests for sprite."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl.testing import absltest
from absl.testing import parameterized
import numpy as np
from six.moves import range
from spriteworld import sprite


class SpriteTest(parameterized.TestCase):

  def testBasicInitialization(self):
    sprite.Sprite(
        x=0.2,
        y=0.8,
        shape='triangle',
        angle=45,
        scale=0.3,
        c0=200,
        c1=150,
        c2=100,
        x_vel=-0.2,
        y_vel=0.1)

  @parameterized.parameters(
      (0.5, 0.5, (-0.3, 0.2), (0.2, 0.7), False),
      (0.1, 0.1, (-0.3, 0.2), (-0.2, 0.3), False),
      (0.1, 0.1, (-0.3, 0.2), (0.0, 0.3), True))
  def testMove(self, x, y, motion, final_position, keep_in_frame):
    s = sprite.Sprite(x=x, y=y)
    s.move(motion, keep_in_frame=keep_in_frame)
    self.assertSequenceAlmostEqual(s.position, final_position, delta=1e-6)

  @parameterized.parameters(
      (0.5, 0.5, 'square', 0, 0.4,
       [[False, False, False, False], [False, True, True, False],
        [False, True, True, False], [False, False, False, False]]),
      (0.5, 0.5, 'square', 25, 0.6,
       [[False, False, True, False], [True, True, True, False],
        [False, True, True, True], [False, True, False, False]]),
      (0.6, 0.55, 'square', 25, 0.6,
       [[False, False, False, False], [False, True, True, True],
        [False, True, True, True], [False, True, True, False]]),
      (0.6, 0.55, 'triangle', 0, 0.6,
       [[False, True, False, False], [False, True, True, True],
        [False, True, True, True], [False, True, True, False]]),
      (0.45, 0.5, 'star_5', 25, 0.6,
       [[False, True, False, False], [True, True, True, True],
        [True, True, True, False], [True, False, True, False]]),
  )
  def testContainsPoint(self, x, y, shape, angle, scale, containment):
    linspace = np.linspace(0.2, 0.8, 4)
    grid = np.stack(np.meshgrid(linspace, linspace), axis=-1)
    s = sprite.Sprite(x=x, y=y, shape=shape, angle=angle, scale=scale)
    eval_containment = [[s.contains_point(p) for p in row] for row in grid]  # pylint: disable=g-complex-comprehension
    self.assertSequenceEqual(
        list(np.ravel(eval_containment)), list(np.ravel(containment)))

  @parameterized.parameters(
      (0.5, 0.5, 'square', 0, 0.25),
      (0.1, 0.8, 'square', 0, 0.25),
      (0.5, 0.5, 'triangle', 0, 0.5),
      (0.5, 0.5, 'triangle', 30, 0.5))
  def testSampleContainedPosition(self, x, y, shape, angle, scale):
    s = sprite.Sprite(x=x, y=y, shape=shape, angle=angle, scale=scale)
    for _ in range(5):
      p = s.sample_contained_position()
      self.assertTrue(s.contains_point(p))

  def testResetShape(self):
    s = sprite.Sprite(angle=30, scale=0.25, shape='square')
    square_vertices = [[0.653, 0.588], [0.412, 0.653], [0.347, 0.412],
                       [0.588, 0.347]]
    self.assertSequenceAlmostEqual(
        np.ravel(s.vertices), np.ravel(square_vertices), delta=1e-3)

    s.shape = 'triangle'
    triangle_vertices = [[0.69, 0.61], [0.31, 0.61], [0.5, 0.281]]
    self.assertSequenceAlmostEqual(
        np.ravel(s.vertices), np.ravel(triangle_vertices), delta=1e-3)

  def testResetAngle(self):
    s = sprite.Sprite(angle=0, scale=0.25, shape='square')
    init_vertices = [[0.677, 0.5], [0.5, 0.677], [0.323, 0.5], [0.5, 0.323]]
    self.assertSequenceAlmostEqual(
        np.ravel(s.vertices), np.ravel(init_vertices), delta=1e-3)

    s.angle = 45
    rotated_vertices = [[0.625, 0.625], [0.375, 0.625], [0.375, 0.375],
                        [0.625, 0.375]]
    self.assertSequenceAlmostEqual(
        np.ravel(s.vertices), np.ravel(rotated_vertices), delta=1e-3)

  def testResetScale(self):
    s = sprite.Sprite(angle=45, scale=0.25, shape='square')
    init_vertices = [[0.625, 0.625], [0.375, 0.625], [0.375, 0.375],
                     [0.625, 0.375]]
    self.assertSequenceAlmostEqual(
        np.ravel(s.vertices), np.ravel(init_vertices), delta=1e-3)

    s.scale = 0.5
    scaled_vertices = [[0.531, 0.531], [0.469, 0.531], [0.469, 0.469],
                       [0.531, 0.469]]
    self.assertSequenceAlmostEqual(
        np.ravel(s.vertices), np.ravel(scaled_vertices), delta=1e-3)

if __name__ == '__main__':
  absltest.main()
