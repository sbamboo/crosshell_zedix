def beethams_line_algorithm(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    points = []
    while True:
        points.append([x1, y1])
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    return points

def beethams_circle_algorithm(x_center, y_center, radius):
    points = []
    x = 0
    y = radius
    d = 3 - 2 * radius
    while x <= y:
        points.append((x_center + x, y_center + y))
        points.append((x_center + y, y_center + x))
        points.append((x_center - y, y_center + x))
        points.append((x_center - x, y_center + y))
        points.append((x_center - x, y_center - y))
        points.append((x_center - y, y_center - x))
        points.append((x_center + y, y_center - x))
        points.append((x_center + x, y_center - y))
        if d < 0:
            d = d + 4 * x + 6
        else:
            d = d + 4 * (x - y) + 10
            y -= 1
        x += 1
    return points


def beethams_ellipse_algorithm(center_x, center_y, xRadius, yRadius):
    points = []
    a = xRadius
    b = yRadius
    x = 0
    y = b
    a_squared = a * a
    b_squared = b * b
    two_a_squared = 2 * a_squared
    two_b_squared = 2 * b_squared
    x_change = b_squared * (1 - 2 * b)  # Initial decision parameter in region 1
    while b_squared * x <= a_squared * y:  # Region 1
        points.append((center_x + x, center_y + y))
        points.append((center_x - x, center_y + y))
        points.append((center_x - x, center_y - y))
        points.append((center_x + x, center_y - y))
        x += 1
        if x_change < 0:
            x_change += two_b_squared * x + b_squared
        else:
            y -= 1
            x_change += two_b_squared * x - two_a_squared * y + b_squared
    y_change = a_squared * (1 - 2 * a)  # Initial decision parameter in region 2
    while y >= 0:  # Region 2
        points.append((center_x + x, center_y + y))
        points.append((center_x - x, center_y + y))
        points.append((center_x - x, center_y - y))
        points.append((center_x + x, center_y - y))
        y -= 1
        if y_change < 0:
            x += 1
            y_change += two_b_squared * x - two_a_squared * y + a_squared
        else:
            y_change -= two_a_squared * y + a_squared
    return points

def generate_quadratic_bezier(x0, y0, x1, y1, x2, y2):
    '''
    0: Start
    1: Control
    2: End
    '''
    points = []
    for t in range(0, 101):
        t_normalized = t / 100.0
        x = (1 - t_normalized) ** 2 * x0 + 2 * (1 - t_normalized) * t_normalized * x1 + t_normalized ** 2 * x2
        y = (1 - t_normalized) ** 2 * y0 + 2 * (1 - t_normalized) * t_normalized * y1 + t_normalized ** 2 * y2
        points.append((round(x), round(y)))
    return points

def generate_cubic_bezier(sX, sY, c1X, c1Y, c2X, c2Y, eX, eY, algorithm="step",modifier=None):
    '''
    Alogrithm: "step" or "point"
    Modifier: With step algorithm, def: 0.01; With point algorithm, def: 100
    '''
    # STEP
    if algorithm.lower() == "step":
        if modifier == None:
            step = 0.01
        else:
            step = modifier
        points = []
        for t in range(int(1/step) + 1):
            t = t * step
            x = int((1 - t)**3 * sX + 3 * t * (1 - t)**2 * c1X + 3 * t**2 * (1 - t) * c2X + t**3 * eX)
            y = int((1 - t)**3 * sY + 3 * t * (1 - t)**2 * c1Y + 3 * t**2 * (1 - t) * c2Y + t**3 * eY)
            points.append((x, y))
        return points
    # POINT
    elif algorithm.lower() == "point":
        if modifier == None:
            num_points = 100
        else:
            num_points = modifier
        points = []
        for t in range(num_points + 1):
            t_normalized = t / num_points
            u = 1 - t_normalized
            uu = u * u
            tt = t_normalized * t_normalized
            uuu = uu * u
            ttt = tt * t_normalized
            x = uuu * sX + 3 * uu * t_normalized * c1X + 3 * u * tt * c2X + ttt * eX
            y = uuu * sY + 3 * uu * t_normalized * c1Y + 3 * u * tt * c2Y + ttt * eY
            points.append((int(x), int(y)))
        return points