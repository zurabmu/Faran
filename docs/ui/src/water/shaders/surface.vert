in vec3 position;
in vec2 uv;
out vec2 place;

void main() {
    place = vec2(uv.x, 1.0 - uv.y);
    gl_Position = vec4(position.xy, 0.0, 1.0);
}
