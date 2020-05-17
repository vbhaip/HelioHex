##maps hexagon index to offset value 
#OFFSETS = {0:0,
#           1:5,
#           2:0,
#           3:4,
#           4:3,
#           5:0,
#           6:0,
#           7:2}
#
##(a,b,c) means hexagon a connects to hexagon b at side number c of hexagon a
#CONNECTIONS = [(1,0,0),
#               (1,2,3),
#               (1,3,2),
#               (2,3,1),
#               (2,4,2),
#               (3,4,3),
#               (4,5,2),
#               (4,6,3),
#               (5,6,4),
#               (6,7,4)]
#
##the connecting side of hex a to hex b in the order the light goes
##n-1 elements where n is number of hexagons
#PATH = [3, 2, 4, 2, 2, 4, 4] 



#2 - 5 configuration
#OFFSETS = {0:0,
#           1:0,
#           2:1,
#           3:5,
#           4:4,
#           5:1,
#           6:1,
#           7:4}
#
##(a,b,c) means hexagon a connects to hexagon b at side number c of hexagon a
#CONNECTIONS = [(1,0,0),
#               (1,3,3),
#               (1,2,4),
#               (2,3,2),
#               (2,4,3),
#               (3,4,4),
#               (4,5,3),
#               (4,7,4),
#               (5,7,5),
#               (5,6,4),
#               (7,6,3)]
#
##the connecting side of hex a to hex b in the order the light goes
##n-1 elements where n is number of hexagons
#PATH = [3, 4, 2, 4, 3, 4, 0] 
#

OFFSETS = {0:0,
           1:5,
           2:0,
           3:3,
           4:5,
           5:2,
           6:2,
           7:0}

#(a,b,c) means hexagon a connects to hexagon b at side number c of hexagon a
CONNECTIONS = [(1,0,0),
               (1,2,3),
               (1,3,2),
               (2,3,1),
               (2,4,2),
               (3,4,3),
               (4,5,3),
               (5,7,2),
               (5,6,3),
               (6,7,1)]

#the connecting side of hex a to hex b in the order the light goes
#n-1 elements where n is number of hexagons
PATH = [3, 3, 1, 3, 3, 3, 1] 
