# TODO 1
### Sphere
$ x = r cos(\phi)cos(\theta) $\
$ y = r cos(\phi)sin(\theta) $\
$ z = r sin(\phi) $\
$ \phi \in [-0.5\pi, 0.5\pi]$\
$ \theta \in [-\pi, \pi)$

### Ellipsoid
$ x = a cos(\phi)cos(\theta) $\
$ y = b cos(\phi)sin(\theta) $\
$ z = c sin(\phi) $\
$ \phi \in [-0.5\pi, 0.5\pi]$\
$ \theta \in [-\pi, \pi)$

### Cylinder (Side)
$ x = r cos(\theta) $\
$ y = r sin(\theta) $\
$ z = \phi $\
$ \phi \in [-0.5h, 0.5h)$\
$ \theta \in [-\pi, \pi)$


### Torus
$ x = (R + rcos(\phi)) cos(\theta) $\
$ y = (R + rcos(\phi)) sin(\theta) $\
$ z = r sin(\phi) $\
$ \phi \in [-\pi, \pi)$\
$ \theta \in [-\pi, \pi)$

# TODO 2
$ (n_x, n_y, n_z) = ( \frac{\partial f}{\partial x}, \frac{\partial f}{\partial y}, \frac{\partial f}{\partial zs})$

# TODO 3
Notations are the same as the slide. See GLProgram.py.\
- `I_amb`: The ambient light
- `I_dif`: The diffuse light
- `I_spe`: The specular light

- `i_dif`: The diffuse light caused by i-th light
- `i_spe`: The specular light caused by i-th light 

# TODO 4
- `f_ang`: angle attenuation
- `f_rad`: radial attenuation
- `1234`: User interface

# TODO 5
### `SceneThree.py`: current scene: 3
- Green: regular light
- Blue: regular light
- 2 Purple: spotlight
- Yellow: infinite light

### `SceneFour.py`: current scene: 4
- Planet system

### `SceneFive.py`: current scene: 5
- Red: regular light
- Green: spotlight
- Yellow: infinite light


# TODO 6
See `SceneSix.py` or switch to `current scene: 6`

The first & last elements in vbo array,  v_arr[0] and v_arr[-1], should refer to a same position on the sphere stack

# TODO 7
In tangent space u-v-w,
- `u` = (1,0,0) (local) <=> `P_u` (global)
- `v` = (0,1,0) (local) <=> `P_v` (global)
- `w` = (0,0,1) (local) <=> `vNormal` (global)

In tangent space, 
- `tangent_normal` = (r, g, b)

Map from the tangent space to the global space, and find the corresponding vector, `sphere_normal`, of `tangent_normal`.

`sphere_normal` = `TBN` * `tangent_normal` , where TBN = [`P_u`; `P_v`; `vNormal`]