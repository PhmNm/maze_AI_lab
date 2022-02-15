import os
import matplotlib.pyplot as plt

##support funciton
def read_file(file_name):
  f=open(file_name,'r')
  n_bonus_points = int(next(f)[:-1])
  bonus_points = []
  for i in range(n_bonus_points):
    x, y, reward = map(int, next(f)[:-1].split(' '))
    bonus_points.append((x, y, reward))
  text=f.read()
  matrix=[list(i) for i in text.splitlines()]
  f.close()
  return bonus_points, matrix
def visualize_maze(matrix, bonus, start, end, route=None, trav=None):
    """
    Args:
      1. matrix: The matrix read from the input file,
      2. bonus: The array of bonus points,
      3. start, end: The starting and ending points,
      4. route: The route from the starting point to the ending one, defined by an array of (x, y), e.g. route = [(1, 2), (1, 3), (1, 4)]
    """
    #1. Define walls and array of direction based on the route
    walls=[(i,j) for i in range(len(matrix)) for j in range(len(matrix[0])) if matrix[i][j]=='x']

    if route:
      direction=[]
      for i in range(1,len(route)):
          if route[i][0]-route[i-1][0]>0:
              direction.append('v')
          elif route[i][0]-route[i-1][0]<0:
              direction.append('^')
          elif route[i][1]-route[i-1][1]>0:
              direction.append('>')
          else:
              direction.append('<')
      direction.pop(0)
    #2. Drawing the map
    add_row = 1
    ax=plt.figure(dpi=100).add_subplot(111)

    plt.text(0,-1,'Bonus_point: ' + str(len(bonus)),fontweight='bold',color='red',
         horizontalalignment='left',
         verticalalignment='center')
    add_row += 1
    if route:
      plt.text(0,-2,'Cost: ' + str(len(route)-1) + '   Traversed: ' + str(len(trav)-1),fontweight='bold',color='red',
          horizontalalignment='left',
          verticalalignment='center')
      add_row += 1

    for i in ['top','bottom','right','left']:
        ax.spines[i].set_visible(False)

    plt.scatter([i[1] for i in walls],[-i[0] - add_row for i in walls],
                marker='X',s=100,color='black')
    
    plt.scatter([i[1] for i in bonus],[-i[0] - add_row for i in bonus],
                marker='P',s=100,color='green')

    plt.scatter(start[1],-start[0] - add_row,marker='*',
                s=100,color='gold')

    if route:
        for i in range(len(route)-2):
            plt.scatter(route[i+1][1],-route[i+1][0] - add_row,
                        marker=direction[i],color='silver')

    plt.text(end[1],-end[0] - add_row,'EXIT',color='red',
         horizontalalignment='center',
         verticalalignment='center')
    plt.xticks([])
    plt.yticks([])
    plt.show()

    print(f'Starting point (x, y) = {start[0], start[1]}')
    print(f'Ending point (x, y) = {end[0], end[1]}')
    
    for _, point in enumerate(bonus):
      print(f'Bonus point at position (x, y) = {point[0], point[1]} with point {point[2]}')

###find start & end
def find_start_end(matrix):
  for i in range(len(matrix)):
      for j in range(len(matrix[0])):
          if matrix[i][j]=='S':
              start=(i,j)
          elif matrix[i][j]==' ':
              if (i==0) or (i==len(matrix)-1) or (j==0) or (j==len(matrix[0])-1):
                  end=(i,j) 
          else:
              pass
  return start, end

#single maze[i][j] of GBFS/A*: [state = ' /X/S', path_cost = 0, heu = heuristic_(), pre = None, [(i-1)(j),
#                     (i+1)(j), (i)(j-1), (i)(j+1)]]

###transform matrix to heuristic maze
def maze_trans(matrix):
  maze = []
  for i in range(len(matrix)):
    temp = []
    for j in range(len(matrix[0])):
      state = matrix[i][j]
      path_cost = 0
      heu = 0
      prev = None
      succs = [(i-1,j),(i,j-1),(i+1,j),(i,j+1)]
      a = {'state':state,'path_cost':path_cost,'heu':heu,'prev':prev,'succs':succs}
      temp.append(a)
    maze.append(temp)
  return maze

##get_set atrribute from matrix
def get_state(maze,A):
  return maze[A[0]][A[1]]['state']
def get_succs(maze,A):
  return maze[A[0]][A[1]]['succs']
def get_path_cost(maze,A):
  return maze[A[0]][A[1]]['path_cost']
def get_prev(maze,A):
  return maze[A[0]][A[1]]['prev']
def get_heu(maze,A):
  return maze[A[0]][A[1]]['heu']
def set_path_cost(maze,A,cost):
  prev = maze[A[0]][A[1]]['prev']
  if prev != None:
    maze[A[0]][A[1]]['path_cost'] += get_path_cost(maze,prev) + cost
def set_prev(maze,A,prev):
  maze[A[0]][A[1]]['prev']=prev

###heuristic
###heuristic_euclid
def heuristic_euclid(A,end):
  h = ((A[0]-end[0])**2 + (A[1]-end[1])**2)**0.5
  return round(h,3)
###heuristic_manhattan
def heuristic_2_times_euclid(A,end):
  h = (A[0]-end[0])**2 + (A[1]-end[1])**2
  return h
###heuristic_step
def heuristic_manhattan(A,end):
  return abs(A[0]-end[0]) + abs(A[1]-end[1])

###set heuristic into points of maze
def set_heuristic(maze,heuristic,end):
  for i in range(len(maze)):
    for j in range(len(maze[0])):
      maze[i][j]['heu'] = heuristic((i,j),end)


###algorithm
###BFS
def BFS(maze,start,end):
  V = [[start]]
  visited = [start]
  k = 0
  while end not in V[k] and len(V[k]) != 0:
    V_next = []
    for s1 in V[k]:
      if get_state(maze,s1) != 'x':
        for s2 in get_succs(maze, s1):
          if get_state(maze,s2) != 'x':
            if s2 not in visited:
              visited.append(s2)
              set_prev(maze,s2,s1)
              V_next.append(s2)
    V.append(V_next)
    k += 1
  if len(V[k]) == 0:
    return None, None
  else:
    route = [end]
    s = end
    for i in range(k):
      route.append(get_prev(maze,s))
      s = get_prev(maze,s)
    route.reverse()
  return route, visited
###DFS
def DFS_Al(maze,start,end,visited):
  m = len(maze)
  n = len(maze[0])
  visited.append(start)
  check_Around = 0
  check = True
  if(start != end):
    for s1 in get_succs(maze,start):
      if get_state(maze,s1) == 'x' or s1 in visited:
        check_Around += 1
      else:
        set_prev(maze,s1,start)
        temp,trav = DFS_Al(maze,s1,end,visited)
        if(temp == -1):
          check_Around += 1
  if(check_Around == 4):
    check = False
  if(check == True):
    return 0, visited
  else:
    return -1, visited
def DFS(maze,start,end):
  visited = []
  check,visited = DFS_Al(maze,start,end,visited)
  if check != -1:
    route = [end]
    s = end
    while s != None:
      route.append(get_prev(maze,s))
      s = get_prev(maze,s)
    route.pop(-1)
    route.reverse()
    return route,visited
  else: return None,visited
###GBFS(maze,start,end)
def GBFS(maze,start,end):
  closed = []
  fringe = [start]
  while len(fringe) > 0:
    temp = [get_heu(maze,i) for i in fringe]
    index = temp.index(min(temp))
    if get_state(maze,fringe[index]) == 'x':
      fringe.remove(fringe[index])
      continue
    next = fringe.pop(index)
    if next == end:
      closed.append(next)
      break
    if next not in closed:
      closed.append(next)
    for i in get_succs(maze,next):
      if i not in fringe and i not in closed and get_state(maze,i) != 'x':
        fringe.append(i)
        set_prev(maze,i,next)
  if len(fringe) == 0 and end not in closed:
    return None, None
  else:
    route = [end]
    s = end
    while s != None:
      route.append(get_prev(maze,s))
      s = get_prev(maze,s)
    route.pop(-1)
    route.reverse()
  return route, closed
###A*
def A_star(maze,start,end):
  closed = []
  fringe = [start]
  while len(fringe) > 0:
    temp = [get_path_cost(maze,i) + get_heu(maze,i) for i in fringe]
    index = temp.index(min(temp))
    if get_state(maze,fringe[index]) == 'x':
      fringe.remove(fringe[index])
      continue
    next = fringe.pop(index)
    if next == end:
      closed.append(next)
      break
    if next not in closed:
      closed.append(next)
    for i in get_succs(maze,next):
      if i not in fringe and i not in closed and get_state(maze,i) != 'x':
        fringe.append(i)
        set_prev(maze,i,next)
        set_path_cost(maze,i,1)
  if len(fringe) == 0 and end not in closed:
    return None, None
  else:
    route = [end]
    s = end
    while s != None:
      route.append(get_prev(maze,s))
      s = get_prev(maze,s)
    route.pop(-1)
    route.reverse()
  return route, closed


###
###main

bonus_points, matrix = read_file('maze_map5_2.txt')
maze = maze_trans(matrix)
start, end = find_start_end(matrix)

##choose heuristic:
set_heuristic(maze,heuristic_euclid,end)
#set_heuristic(maze,heuristic_2_times_euclid,end)
#set_heuristic(maze,heuristic_manhattan,end)


##choose algorithm 
route, trav = BFS(maze,start,end)
#route, trav = DFS(maze,start,end)
#route, trav = GBFS(maze,start,end)
#route, trav = A_star(maze,start,end)

##result
if route == None:
  print('Tìm đường thất bại')
else:
  cost = len(route)-1
  print('Cost = ' + str(cost) + ' Trav = ' + str(len(trav)-1))
  visualize_maze(matrix,bonus_points,start,end,route,trav)