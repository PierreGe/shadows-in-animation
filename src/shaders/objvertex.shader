uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform vec4 color;

attribute vec3 a_position;
attribute vec2 a_texcoord;

varying vec2 v_texcoord;
varying vec4 v_color;

void main()
{
    v_texcoord = a_texcoord;
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    v_color = color;
}