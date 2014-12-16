uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_normal;

uniform vec3 u_light_intensity;
uniform vec3 u_light_position;
uniform sampler2D u_shadow_map;

varying vec3 v_position;
varying vec3 v_normal;
varying vec4 v_color;
varying vec4 v_shadow_coord;

void main()
{
    // Calculate normal in world coordinates
    vec3 normal = normalize(u_normal * vec4(v_normal,1.0)).xyz;

    // Calculate the location of this fragment (pixel) in world coordinates
    vec3 position = vec3(u_view*u_model * vec4(v_position, 1));

    // Calculate the vector from this pixels surface to the light source
    vec3 surfaceToLight = u_light_position - position;

    // Calculate the cosine of the angle of incidence (brightness)
    float brightness = dot(normal, surfaceToLight) /
                      (length(surfaceToLight) * length(normal));
    brightness = max(min(brightness,1.0),0.0);

    // Calculate final color of the pixel, based on:
    // 1. The angle of incidence: brightness
    // 2. The color/intensities of the light: light.intensities
    // 3. The texture and texture coord: texture(tex, fragTexCoord)

    float visibility = 1.0;
    if ( texture2D( u_shadow_map, v_shadow_coord.xy ).z  <  v_shadow_coord.z){
        visibility = 0.5;
    }
    gl_FragColor = v_color * visibility;
    // gl_FragColor = vec4(texture2D( u_shadow_map, v_shadow_coord.xy ).z,texture2D( u_shadow_map, v_shadow_coord.xy ).z,texture2D( u_shadow_map, v_shadow_coord.xy ).z,texture2D( u_shadow_map, v_shadow_coord.xy ).z);
    // gl_FragColor = vec4(v_shadow_coord.z,v_shadow_coord.z,v_shadow_coord.z,v_shadow_coord.z);
}