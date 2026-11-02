import numpy as np
from matplotlib.patches import Polygon
from my_utils import translate, rotate, scale, reflect_y

# 색
WHITE      = '#f7f5f0'   # 털
EAR        = '#efeae2'   # 귀 털   # 털 그림자
CREAM      = '#efe2cf'   # 주둥이 주변
BLACK      = '#1c1a1a'   # 눈, 코
PINK       = '#f2c6d6'   # 옷 (분홍)
YELLOW     = '#f3ecc2'   # 옷 (노랑)
MINT       = '#a9d8c8'   # 옷 끈 (민트)
BLANKET    = '#e3edf9'   # 체크 담요
BLANKET_LN = '#c9dbf2'   # 체크 무늬 줄


# ==============================
# 기본 도형 그리기
# ==============================
def draw_shape(ax, points, color, z=1):
  ax.add_patch(Polygon(points, facecolor=color, edgecolor='none', zorder=z + 3))  # 축 선보다 위에 그리기


def ellipse_points(cx, cy, rx, ry, angle=0.0, n=48):
  # 점 (1, 0)을 조금씩 회전 → 크기 변환 → 회전 → 이동 변환해서 타원 꼭짓점을 만듦
  base = np.array([1.0, 0.0])
  points = []
  for k in range(n):
    p = rotate(base, 2 * np.pi * k / n)  # 단위원 위의 점
    p = scale(p, rx, ry)                 # 타원으로 늘리기
    p = rotate(p, angle)                 # 기울이기
    p = translate(p, cx, cy)             # 위치로 이동
    points.append(p)
  return points


def draw_ellipse(ax, cx, cy, rx, ry, color, angle=0.0, z=1):
  draw_shape(ax, ellipse_points(cx, cy, rx, ry, angle), color, z)


def rect_points(x, y, w, h, angle=0.0):
  # 단위 정사각형을 크기 변환 → 회전 → 이동 변환
  unit = [np.array([0, 0]), np.array([1, 0]), np.array([1, 1]), np.array([0, 1])]
  return [translate(rotate(scale(p, w, h), angle), x, y) for p in unit]

# 파트 그리기
def draw_blanket(ax):  # 바닥의 하늘색 체크 담요
  draw_shape(ax, rect_points(-1000, -1000, 2000, 2000), BLANKET, z=0)
  for i in range(-1000, 1000, 120):
    draw_shape(ax, rect_points(i, -1000, 40, 2000), BLANKET_LN, z=0)  # 세로줄
    draw_shape(ax, rect_points(-1000, i, 2000, 40), BLANKET_LN, z=0)  # 가로줄


def draw_body(ax):  # 몸통 + 앞발
  draw_ellipse(ax, 200, -430, 420, 330, WHITE, z=1)
  draw_ellipse(ax, 250, -760, 110, 90, WHITE, z=4)       # 오른쪽 앞발
  draw_ellipse(ax, -170, -600, 120, 120, WHITE, z=1)     # 왼쪽 몸 털


def draw_clothes(ax):  # 분홍/노랑 줄무늬 옷
  draw_ellipse(ax, 300, -400, 340, 270, YELLOW, angle=-0.25, z=2)
  # 줄무늬
  for k in range(3):
    p = rotate(np.array([0.0, 150.0 - 110 * k]), -0.25)
    draw_ellipse(ax, 330 + p[0], -400 + p[1], 280 - 50 * k, 35, PINK, angle=-0.25, z=2)
  draw_shape(ax, rect_points(60, -640, 45, 430, angle=-0.5), MINT, z=3)  # 어깨 끈


def draw_ear(ax, cx, cy, angle):  # 늘어진 귀
  for dx, dy, r in [(0, 0, 130), (0, -120, 120), (10, -230, 100)]:
    p = rotate(np.array([dx, dy]), angle)
    draw_ellipse(ax, cx + p[0], cy + p[1], r, r * 1.1, EAR, z=5)


def draw_head(ax):  # 동그랗고 복슬복슬한 머리
  hx, hy, r = -60, 150, 330

  # 귀
  draw_ear(ax, hx - 330, hy + 20, 0.2)
  right = reflect_y(np.array([-330.0, 20.0]))
  draw_ear(ax, hx + right[0], hy + right[1], -0.2)

  # 머리 본체
  draw_ellipse(ax, hx, hy, r, r * 0.95, WHITE, z=6)

  # 머리 둘레 털 뭉치
  for k in range(16):
    p = rotate(np.array([r * 0.92, 0.0]), 2 * np.pi * k / 16)
    draw_ellipse(ax, hx + p[0], hy + p[1] * 0.95, 80, 80, WHITE, z=6)


def draw_face(ax):  # 눈, 주둥이, 코
  hx, hy = -60, 150

  # 주둥이 주변 크림색 털
  draw_ellipse(ax, hx + 10, hy - 140, 170, 140, CREAM, z=8)
  draw_ellipse(ax, hx + 10, hy - 170, 140, 100, WHITE, z=8)

  # 눈
  for ex, ey in [np.array([-120.0, 10.0]), reflect_y(np.array([-120.0, 10.0]))]:
    draw_ellipse(ax, hx + ex, hy + ey, 52, 58, BLACK, z=9)
    draw_ellipse(ax, hx + ex - 15, hy + ey + 22, 14, 12, WHITE, z=10)  # 눈 반짝임

  # 코
  draw_ellipse(ax, hx + 10, hy - 140, 70, 52, BLACK, z=10)
  draw_ellipse(ax, hx - 15, hy - 120, 16, 10, '#5a5656', z=11)       # 코 반짝임

  # 입
  draw_shape(ax, rect_points(hx + 6, hy - 215, 8, 40), '#6b6262', z=10)


# 강아지 그리기
def draw_dog(ax):
  draw_blanket(ax)
  draw_body(ax)
  draw_clothes(ax)
  draw_head(ax)
  draw_face(ax)
