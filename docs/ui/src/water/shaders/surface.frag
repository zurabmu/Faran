precision highp float;

const float SLOPE_SCALE = 1.6;
const vec2 LIGHT_DIRECTION = vec2(-0.55, 0.85);
const float GLINT = 0.42;
const float SHARP_GLINT = 0.5;
const float SHADOW = 0.22;

uniform sampler2D heights;
uniform vec2 texel;
uniform vec3 tint;
in vec2 place;
out vec4 color;

float heightAt(vec2 at) {
    return texture(heights, at).r;
}

vec2 slopeAt(vec2 at) {
    float alongX = heightAt(at + vec2(texel.x, 0.0)) - heightAt(at - vec2(texel.x, 0.0));
    float alongY = heightAt(at - vec2(0.0, texel.y)) - heightAt(at + vec2(0.0, texel.y));
    return vec2(alongX, alongY) * SLOPE_SCALE;
}

void main() {
    float facing = clamp(-dot(slopeAt(place), normalize(LIGHT_DIRECTION)), -1.0, 1.0);
    float lit = max(facing, 0.0);
    float glint = GLINT * lit + SHARP_GLINT * pow(lit, 3.0);
    float shadow = SHADOW * max(-facing, 0.0);
    color = vec4(tint * glint, glint + shadow);
}
