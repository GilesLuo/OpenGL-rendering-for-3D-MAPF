# OpenGL-rendering-for-3D-MAPF

The python3 file "3D_drawing" is a tiny UI for RL based 3D-MAPF demonstration.

3D example:

![image](https://github.com/GilesLuo/OpenGL-rendering-for-3D-MAPF/blob/master/example/episode_5843_256_-793.6.gif)


A 2D example of MAPF is shown here:

![image](https://github.com/GilesLuo/OpenGL-rendering-for-3D-MAPF/blob/master/gifs_primal_tests/episode_12_39.gif)

Input: 
two 3D metrices world and goals, they must be "cube" metrices, which means that height == width == length

Output:
A exe window virsualizes the given world and goals metrices, which allows you to change projection through mouse dragging.

An offscreen rendering version which allows to generate GIFs by imageio is coming soon.
