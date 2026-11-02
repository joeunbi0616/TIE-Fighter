import numpy as np
from matplotlib.patches import Polygon

INF = 1000  # 그림판 크기
LEN = 100   # 처음 사각형의 크기


# ==============================
# 축 그리기 및 사각형 그리기
# ==============================
def draw_axis(ax):
  ax.axhline(0, color='black', alpha=0.3)  # x-axis line
  ax.axvline(0, color='black', alpha=0.3)  # y-axis line
  ax.set_xlim(-INF, INF)
  ax.set_ylim(-INF, INF)
  ax.set_aspect('equal')  # 정사각형 모양으로 backboard 그리기


def draw_rectangle(ax, p1, p2, p3, p4):
  my_polygon = Polygon([p1, p2, p3, p4])
  ax.add_patch(my_polygon)


# ==============================
# 1. 변환 구현
# ==============================
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


# ==============================
# 2. 파트 그리기
# ==============================
def draw_cockpit(ax, p1, p2, p3, p4):  # 중앙 조종석
  # 1. 사각형을 원점으로 이동 변환: T(-LEN/2, -LEN/2)
  q1 = translate(p1, -LEN/2, -LEN/2)
  q2 = translate(p2, -LEN/2, -LEN/2)
  q3 = translate(p3, -LEN/2, -LEN/2)
  q4 = translate(p4, -LEN/2, -LEN/2)

  # 2. 크기 변환: S(5, 5)
  s = 5
  q1 = scale(q1, s, s)
  q2 = scale(q2, s, s)
  q3 = scale(q3, s, s)
  q4 = scale(q4, s, s)

  # 3. 회전 변환: R(pi/4)
  q1 = rotate(q1, np.pi/4.0)
  q2 = rotate(q2, np.pi/4.0)
  q3 = rotate(q3, np.pi/4.0)
  q4 = rotate(q4, np.pi/4.0)

  # 4. polygon 그리기
  draw_rectangle(ax, q1, q2, q3, q4)


# 왼쪽 날개축을 이루는 사각형 2개 꼭짓점
def left_arm_points(p1, p2, p3, p4):
  points = [p1, p2, p3, p4]

  # 1. 위쪽 날개축
  upper = [translate(shear_y(scale(p, 6, 0.8), 0.13), -750, -35) for p in points]

  # 2. 아래쪽 날개축: 위쪽 날개축을 x축 반전
  lower = [reflect_x(q) for q in upper]

  return [upper, lower]


def draw_left_arm(ax, p1, p2, p3, p4):  # 왼쪽 날개축
  for q1, q2, q3, q4 in left_arm_points(p1, p2, p3, p4):
    draw_rectangle(ax, q1, q2, q3, q4)


def draw_right_arm(ax, p1, p2, p3, p4):  # 오른쪽 날개축
  # 왼쪽 날개축을 y축 반전
  for part in left_arm_points(p1, p2, p3, p4):
    q1, q2, q3, q4 = [reflect_y(q) for q in part]
    draw_rectangle(ax, q1, q2, q3, q4)


# 왼쪽 날개를 이루는 몸통과 위쪽 끝 꼭짓점
def left_wing_points(p1, p2, p3, p4):
  points = [p1, p2, p3, p4]

  # 1. 몸통: 가로로 긴 사각형을 만든 뒤 y=x 반전으로 세움
  body = [reflect_xy(translate(scale(p, 8, 1), -400, -850)) for p in points]

  # 2. 위쪽 끝(사선)
  top = [translate(shear_y(scale(p, 1, 2), -2), -850, 400) for p in points]

  return body, top


def draw_left_wing(ax, p1, p2, p3, p4):  # 왼쪽 날개
  body, top = left_wing_points(p1, p2, p3, p4)
  bottom = [reflect_x(q) for q in top]  # 아래쪽 끝: x축 반전

  draw_rectangle(ax, *body)
  draw_rectangle(ax, *top)
  draw_rectangle(ax, *bottom)


def draw_right_wing(ax, p1, p2, p3, p4):  # 오른쪽 날개
  body, top = left_wing_points(p1, p2, p3, p4)
  body_r   = [reflect_y(q) for q in body]       # 몸통: y축 반전
  top_r    = [reflect_y(q) for q in top]        # 위쪽 끝: y축 반전
  bottom_r = [reflect_origin(q) for q in top]   # 아래쪽 끝: 원점 반전

  draw_rectangle(ax, *body_r)
  draw_rectangle(ax, *top_r)
  draw_rectangle(ax, *bottom_r)


# TIE Fighter 그리기
def draw_object(ax):
  p1 = np.array([0, 0])
  p2 = np.array([LEN, 0])
  p3 = np.array([LEN, LEN])
  p4 = np.array([0, LEN])

  # 1. 중앙 조종석 그리기
  draw_cockpit(ax, p1, p2, p3, p4)

  # 2. 왼쪽 날개축, 왼쪽 날개 그리기
  draw_left_arm(ax, p1, p2, p3, p4)
  draw_left_wing(ax, p1, p2, p3, p4)

  # 3. 오른쪽 날개축, 오른쪽 날개 그리기
  draw_right_arm(ax, p1, p2, p3, p4)
  draw_right_wing(ax, p1, p2, p3, p4)
