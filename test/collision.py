import pyxel
import utils.my_quadtree as mq
pyxel.init(256,256)

region1= mq.Rect(80,80, 50, 50)
region2= mq.Rect(60,60, 50, 50)

delta_east = region1.w_edge - region2.e_edge
delta_west = region1.w_edge - region2.e_edge
delta_north = region1.s_edge - region2.n_edge
delta_south = region1.n_edge - region2.w_edge

new_vector_x = min([delta_east, delta_west])
new_vector_y = min([delta_north, delta_south])


region3 = mq.Rect(region2.x_pos + new_vector_x, region2.y_pos + new_vector_y, region2.width, region2.height)

def update():
    global region
    delta_east = region1.w_edge - region2.e_edge
    delta_west = region1.w_edge - region2.e_edge
    delta_north = region1.s_edge - region2.n_edge
    delta_south = region1.n_edge - region2.w_edge

    new_vector_x = min([delta_east, delta_west])
    new_vector_y = min([delta_north, delta_south])


    if new_vector_x == new_vector_y:
        region3 = mq.Rect(region2.x_pos + new_vector_x, region2.y_pos + new_vector_y, region2.width, region2.height)

    print(f'New vector x: {new_vector_x}\nNew vector y: {new_vector_y}')

    # if not new_vector_y == new_vector_x:
    #     if new_vector_x > new_vector_y:
    #         dx += dx * (dy / new_vector_y) + 1
    #         dy += new_vector_y + 1
    #     else:
    #         dy += dy * (dx / new_vector_x) + 1
    #         dx += new_vector_x + 1
    # else:
    #     dx += new_vector_x + 1
    #     dy += new_vector_y + 1
    #
    # test_hitbox.x_pos += dx
    # test_hitbox.y_pos += dy

def draw():
    pyxel.cls(0)
    region1.draw()
    region2.draw()
    pyxel.rectb(region3.x_pos, region3.y_pos, region3.width, region3.height, 7)




pyxel.run(update, draw)