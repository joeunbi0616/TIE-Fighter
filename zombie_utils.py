import numpy as np
from matplotlib.patches import Polygon

INF = 1000  # 그림판 크기
LEN = 100   # 처음 사각형의 크기


def draw_axis(ax):
  ax.axhline(0, color='black', alpha=0.3)
  ax.axvline(0, color='black', alpha=0.3)
  ax.set_ylim(-INF, INF)
  ax.set_aspect('equal')


def draw_rectangle(ax, p1, p2, p3, p4):
  my_polygon = Polygon([p1, p2, p3, p4])
  ax.add_patch(my_polygon)

#변환
def transform(m, p):
  hp = np.array([p[0], p[1], 1.0])
  q = np.dot(m, hp)
  return np.array([q[0], q[1]])


def translate(p, dx, dy):
  m = np.array([[1.0, 0.0, dx],
                [0.0, 1.0, dy],
                [0.0, 0.0, 1.0]])
  return transform(m, p)


def rotate(p, theta):
  m = np.array([[np.cos(theta), -np.sin(theta), 0.0],
                [np.sin(theta),  np.cos(theta), 0.0],
                [0.0,            0.0,           1.0]])
  return transform(m, p)


def scale(p, sx, sy):
  m = np.array([[sx, 0.0, 0.0],
                [0.0, sy, 0.0],
                [0.0, 0.0, 1.0]])
  return transform(m, p)


# x축 방향 기울기
def shear_x(p, sx):
  m = np.array([[1.0, sx, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0]])
  return transform(m, p)


# y축 방향 기울기
def shear_y(p, sy):
  m = np.array([[1.0, 0.0, 0.0],
                [sy, 1.0, 0.0],
                [0.0, 0.0, 1.0]])
  return transform(m, p)


# x축 반전
def reflect_x(p):
  m = np.array([[1.0, 0.0, 0.0],
                [0.0, -1.0, 0.0],
                [0.0, 0.0, 1.0]])
  return transform(m, p)


# y축 반전
def reflect_y(p):
  m = np.array([[-1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0]])
  return transform(m, p)


# 원점 반전
def reflect_origin(p):
  m = np.array([[-1.0, 0.0, 0.0],
                [0.0, -1.0, 0.0],
                [0.0, 0.0, 1.0]])
  return transform(m, p)


# y=x 반전
def reflect_xy(p):
  m = np.array([[0.0, 1.0, 0.0],
                [1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0]])
  return transform(m, p)


SKIN       = '#a8b5a2'
SKIN_DARK  = '#7f8c7a'
SHIRT      = '#8c3b3b'
SHIRT_DARK = '#5e2626'
PANTS      = '#4a4440'
SHOE       = '#2b2724'
HAIR       = '#3a3330'
EYE_WHITE  = '#f0ead6'
PUPIL      = '#c0392b'
MOUTH      = '#2a1e1e'
TEETH      = '#e8e0c8'
GROUND     = '#d8d2c4'
GRASS      = '#8a9a6b'



def draw_box(ax, q1, q2, q3, q4, color):
  ax.add_patch(Polygon([q1, q2, q3, q4], facecolor=color, edgecolor='none', zorder=3))


def make_box(points, sx, sy, cx, cy, theta=0.0, shx=0.0):
  result = []
  for p in points:
    q = translate(p, -LEN/2, -LEN/2)
    q = scale(q, sx, sy)
    q = shear_x(q, shx)
    q = rotate(q, theta)
    q = translate(q, cx, cy)
    result.append(q)
  return result


def mirror(box):
  return [reflect_y(q) for q in box]


def draw_pair(ax, box, color):
  draw_box(ax, *box, color)
  draw_box(ax, *mirror(box), color)


def rotate_about(box, theta, cx, cy):
  return [translate(rotate(translate(q, -cx, -cy), theta), cx, cy) for q in box]


def draw_ground(ax, points):
  draw_box(ax, *make_box(points, 20, 2.2, 0, -890), GROUND)
  for k in range(12):
    x = -900 + 160 * k
    draw_box(ax, *make_box(points, 0.15, 0.6, x, -760, theta=0.3), GRASS)
    draw_box(ax, *make_box(points, 0.15, 0.5, x + 25, -765, theta=-0.3), GRASS)


def draw_legs(ax, points):
  draw_box(ax, *make_box(points, 1.3, 5.2, -115, -450, theta=-0.06), PANTS)
  draw_box(ax, *make_box(points, 1.6, 0.6, -140, -745), SHOE)

  draw_box(ax, *make_box(points, 1.3, 5.2, 110, -450), PANTS)
  draw_box(ax, *make_box(points, 1.6, 0.6, 130, -745), SHOE)

  draw_box(ax, *make_box(points, 0.7, 0.35, 110, -560, shx=0.8), SKIN)
  draw_box(ax, *make_box(points, 0.5, 0.3, -125, -420, shx=-0.8), SKIN)


def draw_body(ax, points):
  draw_box(ax, *make_box(points, 4.2, 4.0, 0, 0), SHIRT)

  draw_box(ax, *make_box(points, 1.0, 0.7, 70, 60, theta=0.3), SHIRT_DARK)
  draw_box(ax, *make_box(points, 0.6, 0.4, 70, 60, theta=0.3), SKIN_DARK)

  draw_pair(ax, make_box(points, 0.9, 0.6, -55, 185, shx=0.6), SHIRT_DARK)


def draw_arms(ax, points):
  sx, sy = -230, 150
  sleeve = make_box(points, 1.2, 1.4, sx, sy - 40)
  arm    = make_box(points, 0.9, 3.2, sx, sy - 200)
  hand   = make_box(points, 1.1, 0.9, sx, sy - 375)
  fingers = [make_box(points, 0.22, 0.6, sx - 35 + 23 * k, sy - 440) for k in range(4)]

  theta = -2.2
  parts = [(arm, SKIN), (hand, SKIN)] + [(f, SKIN_DARK) for f in fingers] + [(sleeve, SHIRT)]
  for box, color in parts:
    draw_pair(ax, rotate_about(box, theta, sx, sy), color)


def draw_head(ax, points):
  hx, hy = 10, 400
  tilt = 0.12

  def head_box(sx, sy, dx, dy, theta=0.0, shx=0.0):
    return rotate_about(make_box(points, sx, sy, hx + dx, hy + dy, theta, shx), tilt, hx, hy)

  # 목
  draw_box(ax, *make_box(points, 1.2, 0.9, 0, 230), SKIN_DARK)

  # 얼굴
  draw_box(ax, *head_box(3.4, 3.4, 0, 0), SKIN)

  # 머리카락
  draw_box(ax, *head_box(3.6, 0.7, 0, 150), HAIR)
  for k in range(5):
    theta = 0.35 if k % 2 == 0 else -0.25
    draw_box(ax, *head_box(0.6, 0.9, -140 + 70 * k, 195, theta=theta), HAIR)

  # 눈
  draw_box(ax, *head_box(0.9, 0.8, -70, 30), EYE_WHITE)
  draw_box(ax, *head_box(0.35, 0.35, -60, 25), PUPIL)
  draw_box(ax, *head_box(0.7, 0.45, 75, 15, theta=-0.25), EYE_WHITE)
  draw_box(ax, *head_box(0.25, 0.25, 70, 12), PUPIL)

  # 다크서클
  draw_box(ax, *head_box(0.9, 0.15, -70, -27), SKIN_DARK)
  draw_box(ax, *head_box(0.7, 0.15, 75, -15, theta=-0.25), SKIN_DARK)

  # 입
  draw_box(ax, *head_box(1.9, 0.5, 0, -100, theta=-0.1), MOUTH)
  for k in range(4):
    draw_box(ax, *head_box(0.22, 0.22, -55 + 37 * k, -88 + (-4 * k)), TEETH)


# 좀비 그리기
def draw_zombie(ax):
  p1 = np.array([0, 0])
  p2 = np.array([LEN, 0])
  p3 = np.array([LEN, LEN])
  p4 = np.array([0, LEN])
  points = [p1, p2, p3, p4]

  draw_ground(ax, points)
  draw_legs(ax, points)
  draw_arms(ax, points)
  draw_body(ax, points)
  draw_head(ax, points)
