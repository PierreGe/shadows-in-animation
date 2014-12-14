varying vec4 v_color;
varying vec2 v_texcoord;

void main()
{
    //float ty = v_texcoord.y;
    //float tx = sin(ty*50.0)*0.01 + v_texcoord.x;
    gl_FragColor = v_color;
}