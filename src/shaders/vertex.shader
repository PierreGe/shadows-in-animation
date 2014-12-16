uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform mat4 u_bias_matrix;

uniform vec4 u_color;

attribute vec3 position;
attribute vec3 normal;

varying vec3 v_position;
varying vec3 v_normal;
varying vec4 v_color;
varying vec4 v_shadow_coord;

void main()
{
    gl_Position = u_projection * u_view * u_model * vec4(position, 1.0);
    v_shadow_coord = u_bias_matrix * vec4(position, 1.0);
    v_position = position;
    v_normal = normal;
    v_color = u_color;
}