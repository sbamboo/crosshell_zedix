def get_circle_coords(radius, x0, y0):
  coords = []
  for y in range(y0 - radius, y0 + radius + 1):
    for x in range(x0 - radius, x0 + radius + 1):
      if (x - x0)**2 + (y - y0)**2 <= radius**2:
        coords.append((x, y))
  return coords

for cord in get_circle_coords(radius,10,10):
  draw_point("#",cord[0],cord[1])