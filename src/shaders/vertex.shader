uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform vec4 color;
attribute vec3 position;
varying vec4 v_color;
void main()
{
    gl_Position = projection * view * model * vec4(position, 1.0);
    v_color = color;
}