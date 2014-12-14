uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
attribute vec3 position;
attribute vec2 texcoord;
varying vec2 v_texcoord;

void main()
{
    gl_Position = projection * view * model * vec4(position, 1.0);
    v_texcoord = texcoord;
}