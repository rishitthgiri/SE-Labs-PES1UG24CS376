def is_caught(basket_rect, obj):
    closest_x = max(basket_rect.left, min(obj.x, basket_rect.right))
    closest_y = max(basket_rect.top, min(obj.y, basket_rect.bottom))

    dx = obj.x - closest_x
    dy = obj.y - closest_y

    return dx * dx + dy * dy <= obj.radius * obj.radius