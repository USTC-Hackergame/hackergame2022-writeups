window.fragmentShader = `
precision highp float;

uniform vec2 iResolution;
uniform vec2 iMouse;
uniform float iTime;
#define RAYMARCH_MAX_STEPS 50
#define RAYMARCH_MAX_DIST 100.5
#define RAYMARCH_SURF_DIST 1e-2
#define RAYMARCH_CONSERVATIVE_FACTOR 1.0
#define GRAD_APPROX_EPS 1e-3
#define PI 3.14159265359

// Third-party code from Stefan Gustavson (stefan.gustavson@liu.se)
// https://github.com/ashima/webgl-noise
// https://thebookofshaders.com/edit.php#11/2d-pnoise.frag
// Licensed under MIT License
// =============================================================================
vec4 mod289(vec4 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
vec4 permute(vec4 x) { return mod289(((x*34.0)+1.0)*x); }
vec4 taylorInvSqrt(vec4 r) { return 1.79284291400159 - 0.85373472095314 * r; }
vec2 fade(vec2 t) { return t*t*t*(t*(t*6.0-15.0)+10.0); }

// Classic Perlin noise
float cnoise(vec2 P) {
    vec4 Pi = floor(P.xyxy) + vec4(0.0, 0.0, 1.0, 1.0);
    vec4 Pf = fract(P.xyxy) - vec4(0.0, 0.0, 1.0, 1.0);
    Pi = mod289(Pi); // To avoid truncation effects in permutation
    vec4 ix = Pi.xzxz;
    vec4 iy = Pi.yyww;
    vec4 fx = Pf.xzxz;
    vec4 fy = Pf.yyww;

    vec4 i = permute(permute(ix) + iy);

    vec4 gx = fract(i * (1.0 / 41.0)) * 2.0 - 1.0 ;
    vec4 gy = abs(gx) - 0.5 ;
    vec4 tx = floor(gx + 0.5);
    gx = gx - tx;

    vec2 g00 = vec2(gx.x,gy.x);
    vec2 g10 = vec2(gx.y,gy.y);
    vec2 g01 = vec2(gx.z,gy.z);
    vec2 g11 = vec2(gx.w,gy.w);

    vec4 norm = taylorInvSqrt(vec4(dot(g00, g00), dot(g01, g01), dot(g10, g10), dot(g11, g11)));
    g00 *= norm.x;
    g01 *= norm.y;
    g10 *= norm.z;
    g11 *= norm.w;

    float n00 = dot(g00, vec2(fx.x, fy.x));
    float n10 = dot(g10, vec2(fx.y, fy.y));
    float n01 = dot(g01, vec2(fx.z, fy.z));
    float n11 = dot(g11, vec2(fx.w, fy.w));

    vec2 fade_xy = fade(Pf.xy);
    vec2 n_x = mix(vec2(n00, n01), vec2(n10, n11), fade_xy.x);
    float n_xy = mix(n_x.x, n_x.y, fade_xy.y);
    return 2.3 * n_xy;
}
// ======================================================

mat4 mk_trans(float x, float y, float z) {
    return mat4(1.0, 0.0, 0.0, 0.0,  // 1. column
                0.0, 1.0, 0.0, 0.0,  // 2. column
                0.0, 0.0, 1.0, 0.0,  // 3. column
                  x,   y,   z, 1.0); // 4. column
}

mat4 mk_scale(float x, float y, float z) {
    return mat4(  x, 0.0, 0.0, 0.0,  // 1. column
                0.0,   y, 0.0, 0.0,  // 2. column
                0.0, 0.0,   z, 0.0,  // 3. column
                0.0, 0.0, 0.0, 1.0); // 4. column
}

vec4 mk_homo(vec3 orig) {
    return vec4(orig.x, orig.y, orig.z, 1.0);
}

// == terrain functionalities ==

float heightMap(vec3 p) {
    vec2 pPlane = vec2(p.z + iTime, p.x);
    float hMap = 0.25 * cnoise(pPlane) + 0.5 * cnoise(pPlane / 2.0) + cnoise(pPlane / 4.0);
    return hMap * 1.0;
}

vec3 colorMap(vec3 p) {
    return vec3(0.6, 0.6, 0.4);
}

float elevation(vec3 p) {
    return p.y - heightMap(p);
}

// =============================

float t1SDF(vec3 qPnt) {
    return min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min
        (min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min
            (min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min
                (min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min
                    (min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min((length(((qPnt - vec3(2,13,0))))-0.4), 
                    (length(((qPnt - vec3(3,13,0))))-0.4)), (length(((qPnt - vec3(4,13,0))))-0.4)), (length(((qPnt - vec3(1,12,0))))-0.4)), 
                    (length(((qPnt - vec3(2,12,0))))-0.4)), (length(((qPnt - vec3(4,12,0))))-0.4)), (length(((qPnt - vec3(5,12,0))))-0.4)), 
                    (length(((qPnt - vec3(1,11,0))))-0.4)), (length(((qPnt - vec3(2,11,0))))-0.4)), (length(((qPnt - vec3(5,11,0))))-0.4)), 
                    (length(((qPnt - vec3(1,10,0))))-0.4)), (length(((qPnt - vec3(2,10,0))))-0.4)), (length(((qPnt - vec3(0,9,0))))-0.4)), 
                    (length(((qPnt - vec3(1,9,0))))-0.4)), (length(((qPnt - vec3(2,9,0))))-0.4)), (length(((qPnt - vec3(3,9,0))))-0.4)), 
                    (length(((qPnt - vec3(1,8,0))))-0.4)), (length(((qPnt - vec3(2,8,0))))-0.4)), (length(((qPnt - vec3(1,7,0))))-0.4)), 
                    (length(((qPnt - vec3(2,7,0))))-0.4)), (length(((qPnt - vec3(1,6,0))))-0.4)), (length(((qPnt - vec3(2,6,0))))-0.4)), 
                    (length(((qPnt - vec3(1,5,0))))-0.4)), (length(((qPnt - vec3(2,5,0))))-0.4)), (length(((qPnt - vec3(0,4,0))))-0.4)), 
                    (length(((qPnt - vec3(1,4,0))))-0.4)), (length(((qPnt - vec3(2,4,0))))-0.4)), (length(((qPnt - vec3(3,4,0))))-0.4)), 
                    (length(((qPnt - vec3(11,13,0))))-0.4)), (length(((qPnt - vec3(12,13,0))))-0.4)), (length(((qPnt - vec3(13,13,0))))-0.4)), 
                    (length(((qPnt - vec3(12,12,0))))-0.4)), (length(((qPnt - vec3(13,12,0))))-0.4)), (length(((qPnt - vec3(12,11,0))))-0.4)), 
                    (length(((qPnt - vec3(13,11,0))))-0.4)), (length(((qPnt - vec3(12,10,0))))-0.4)), (length(((qPnt - vec3(13,10,0))))-0.4)), 
                    (length(((qPnt - vec3(12,9,0))))-0.4)), (length(((qPnt - vec3(13,9,0))))-0.4)), (length(((qPnt - vec3(12,8,0))))-0.4)), 
                    (length(((qPnt - vec3(13,8,0))))-0.4)), (length(((qPnt - vec3(12,7,0))))-0.4)), (length(((qPnt - vec3(13,7,0))))-0.4)), 
                    (length(((qPnt - vec3(12,6,0))))-0.4)), (length(((qPnt - vec3(13,6,0))))-0.4)), (length(((qPnt - vec3(12,5,0))))-0.4)), 
                    (length(((qPnt - vec3(13,5,0))))-0.4)), (length(((qPnt - vec3(11,4,0))))-0.4)), (length(((qPnt - vec3(12,4,0))))-0.4)), 
                    (length(((qPnt - vec3(13,4,0))))-0.4)), (length(((qPnt - vec3(14,4,0))))-0.4)), (length(((qPnt - vec3(19,10,0))))-0.4)), 
                    (length(((qPnt - vec3(20,10,0))))-0.4)), (length(((qPnt - vec3(21,10,0))))-0.4)), (length(((qPnt - vec3(22,10,0))))-0.4)), 
                    (length(((qPnt - vec3(22,9,0))))-0.4)), (length(((qPnt - vec3(23,9,0))))-0.4)), (length(((qPnt - vec3(19,8,0))))-0.4)), 
                    (length(((qPnt - vec3(20,8,0))))-0.4)), (length(((qPnt - vec3(21,8,0))))-0.4)), (length(((qPnt - vec3(22,8,0))))-0.4)), 
                    (length(((qPnt - vec3(23,8,0))))-0.4)), (length(((qPnt - vec3(18,7,0))))-0.4)), (length(((qPnt - vec3(19,7,0))))-0.4)), 
                    (length(((qPnt - vec3(22,7,0))))-0.4)), (length(((qPnt - vec3(23,7,0))))-0.4)), (length(((qPnt - vec3(18,6,0))))-0.4)), 
                    (length(((qPnt - vec3(19,6,0))))-0.4)), (length(((qPnt - vec3(22,6,0))))-0.4)), (length(((qPnt - vec3(23,6,0))))-0.4)), 
                    (length(((qPnt - vec3(18,5,0))))-0.4)), (length(((qPnt - vec3(19,5,0))))-0.4)), (length(((qPnt - vec3(22,5,0))))-0.4)), 
                    (length(((qPnt - vec3(23,5,0))))-0.4)), (length(((qPnt - vec3(19,4,0))))-0.4)), (length(((qPnt - vec3(20,4,0))))-0.4)), 
                    (length(((qPnt - vec3(21,4,0))))-0.4)), (length(((qPnt - vec3(23,4,0))))-0.4)), (length(((qPnt - vec3(24,4,0))))-0.4)), 
                    (length(((qPnt - vec3(28,10,0))))-0.4)), (length(((qPnt - vec3(29,10,0))))-0.4)), (length(((qPnt - vec3(30,10,0))))-0.4)), 
                    (length(((qPnt - vec3(32,10,0))))-0.4)), (length(((qPnt - vec3(33,10,0))))-0.4)), (length(((qPnt - vec3(27,9,0))))-0.4)), 
                    (length(((qPnt - vec3(28,9,0))))-0.4)), (length(((qPnt - vec3(31,9,0))))-0.4)), (length(((qPnt - vec3(32,9,0))))-0.4)), 
                    (length(((qPnt - vec3(27,8,0))))-0.4)), (length(((qPnt - vec3(28,8,0))))-0.4)), (length(((qPnt - vec3(31,8,0))))-0.4)), 
                    (length(((qPnt - vec3(32,8,0))))-0.4)), (length(((qPnt - vec3(27,7,0))))-0.4)), (length(((qPnt - vec3(28,7,0))))-0.4)), 
                    (length(((qPnt - vec3(31,7,0))))-0.4)), (length(((qPnt - vec3(32,7,0))))-0.4)), (length(((qPnt - vec3(27,6,0))))-0.4)), 
                    (length(((qPnt - vec3(28,6,0))))-0.4)), (length(((qPnt - vec3(31,6,0))))-0.4)), (length(((qPnt - vec3(32,6,0))))-0.4)), 
                    (length(((qPnt - vec3(27,5,0))))-0.4)), (length(((qPnt - vec3(28,5,0))))-0.4)), (length(((qPnt - vec3(31,5,0))))-0.4)), 
                    (length(((qPnt - vec3(32,5,0))))-0.4)), (length(((qPnt - vec3(28,4,0))))-0.4)), (length(((qPnt - vec3(29,4,0))))-0.4)), 
                    (length(((qPnt - vec3(30,4,0))))-0.4)), (length(((qPnt - vec3(31,4,0))))-0.4)), (length(((qPnt - vec3(32,4,0))))-0.4)), 
                    (length(((qPnt - vec3(31,3,0))))-0.4)), (length(((qPnt - vec3(32,3,0))))-0.4)), (length(((qPnt - vec3(27,2,0))))-0.4)), 
                    (length(((qPnt - vec3(28,2,0))))-0.4)), (length(((qPnt - vec3(31,2,0))))-0.4)), (length(((qPnt - vec3(32,2,0))))-0.4)), 
                    (length(((qPnt - vec3(28,1,0))))-0.4)), (length(((qPnt - vec3(29,1,0))))-0.4)), (length(((qPnt - vec3(30,1,0))))-0.4)), 
                    (length(((qPnt - vec3(31,1,0))))-0.4)), (length(((qPnt - vec3(40,13,0))))-0.4)), (length(((qPnt - vec3(41,13,0))))-0.4)), 
                    (length(((qPnt - vec3(42,13,0))))-0.4)), (length(((qPnt - vec3(39,12,0))))-0.4)), (length(((qPnt - vec3(40,12,0))))-0.4)), 
                    (length(((qPnt - vec3(39,11,0))))-0.4)), (length(((qPnt - vec3(40,11,0))))-0.4)), (length(((qPnt - vec3(39,10,0))))-0.4)), 
                    (length(((qPnt - vec3(40,10,0))))-0.4)), (length(((qPnt - vec3(37,9,0))))-0.4)), (length(((qPnt - vec3(38,9,0))))-0.4)), 
                    (length(((qPnt - vec3(39,9,0))))-0.4)), (length(((qPnt - vec3(39,8,0))))-0.4)), (length(((qPnt - vec3(40,8,0))))-0.4)), 
                    (length(((qPnt - vec3(39,7,0))))-0.4)), (length(((qPnt - vec3(40,7,0))))-0.4)), (length(((qPnt - vec3(39,6,0))))-0.4)), 
                    (length(((qPnt - vec3(40,6,0))))-0.4)), (length(((qPnt - vec3(39,5,0))))-0.4)), (length(((qPnt - vec3(40,5,0))))-0.4)), 
                    (length(((qPnt - vec3(40,4,0))))-0.4)), (length(((qPnt - vec3(41,4,0))))-0.4)), (length(((qPnt - vec3(42,4,0))))-0.4));
}

float t2SDF(vec3 qPnt) {
    return min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min
        (min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min
            (min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min
                (min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min((length(((qPnt - vec3(1,13,0))))-0.4), 
                (length(((qPnt - vec3(2,13,0))))-0.4)), (length(((qPnt - vec3(3,13,0))))-0.4)), (length(((qPnt - vec3(4,13,0))))-0.4)), 
                (length(((qPnt - vec3(5,13,0))))-0.4)), (length(((qPnt - vec3(0,12,0))))-0.4)), (length(((qPnt - vec3(1,12,0))))-0.4)), 
                (length(((qPnt - vec3(5,12,0))))-0.4)), (length(((qPnt - vec3(6,12,0))))-0.4)), (length(((qPnt - vec3(0,11,0))))-0.4)), 
                (length(((qPnt - vec3(1,11,0))))-0.4)), (length(((qPnt - vec3(5,11,0))))-0.4)), (length(((qPnt - vec3(6,11,0))))-0.4)), 
                (length(((qPnt - vec3(1,10,0))))-0.4)), (length(((qPnt - vec3(2,10,0))))-0.4)), (length(((qPnt - vec3(2,9,0))))-0.4)), 
                (length(((qPnt - vec3(3,9,0))))-0.4)), (length(((qPnt - vec3(4,9,0))))-0.4)), (length(((qPnt - vec3(4,8,0))))-0.4)), 
                (length(((qPnt - vec3(5,8,0))))-0.4)), (length(((qPnt - vec3(5,7,0))))-0.4)), (length(((qPnt - vec3(6,7,0))))-0.4)), 
                (length(((qPnt - vec3(0,6,0))))-0.4)), (length(((qPnt - vec3(1,6,0))))-0.4)), (length(((qPnt - vec3(5,6,0))))-0.4)), 
                (length(((qPnt - vec3(6,6,0))))-0.4)), (length(((qPnt - vec3(0,5,0))))-0.4)), (length(((qPnt - vec3(1,5,0))))-0.4)), 
                (length(((qPnt - vec3(5,5,0))))-0.4)), (length(((qPnt - vec3(6,5,0))))-0.4)), (length(((qPnt - vec3(1,4,0))))-0.4)), 
                (length(((qPnt - vec3(2,4,0))))-0.4)), (length(((qPnt - vec3(3,4,0))))-0.4)), (length(((qPnt - vec3(4,4,0))))-0.4)), 
                (length(((qPnt - vec3(5,4,0))))-0.4)), (length(((qPnt - vec3(9,13,0))))-0.4)), (length(((qPnt - vec3(10,13,0))))-0.4)), 
                (length(((qPnt - vec3(11,13,0))))-0.4)), (length(((qPnt - vec3(12,13,0))))-0.4)), (length(((qPnt - vec3(13,13,0))))-0.4)), 
                (length(((qPnt - vec3(10,12,0))))-0.4)), (length(((qPnt - vec3(11,12,0))))-0.4)), (length(((qPnt - vec3(13,12,0))))-0.4)), 
                (length(((qPnt - vec3(14,12,0))))-0.4)), (length(((qPnt - vec3(10,11,0))))-0.4)), (length(((qPnt - vec3(11,11,0))))-0.4)), 
                (length(((qPnt - vec3(14,11,0))))-0.4)), (length(((qPnt - vec3(15,11,0))))-0.4)), (length(((qPnt - vec3(10,10,0))))-0.4)), 
                (length(((qPnt - vec3(11,10,0))))-0.4)), (length(((qPnt - vec3(14,10,0))))-0.4)), (length(((qPnt - vec3(15,10,0))))-0.4)), 
                (length(((qPnt - vec3(10,9,0))))-0.4)), (length(((qPnt - vec3(11,9,0))))-0.4)), (length(((qPnt - vec3(14,9,0))))-0.4)), 
                (length(((qPnt - vec3(15,9,0))))-0.4)), (length(((qPnt - vec3(10,8,0))))-0.4)), (length(((qPnt - vec3(11,8,0))))-0.4)), 
                (length(((qPnt - vec3(14,8,0))))-0.4)), (length(((qPnt - vec3(15,8,0))))-0.4)), (length(((qPnt - vec3(10,7,0))))-0.4)), 
                (length(((qPnt - vec3(11,7,0))))-0.4)), (length(((qPnt - vec3(14,7,0))))-0.4)), (length(((qPnt - vec3(15,7,0))))-0.4)), 
                (length(((qPnt - vec3(10,6,0))))-0.4)), (length(((qPnt - vec3(11,6,0))))-0.4)), (length(((qPnt - vec3(14,6,0))))-0.4)), 
                (length(((qPnt - vec3(15,6,0))))-0.4)), (length(((qPnt - vec3(10,5,0))))-0.4)), (length(((qPnt - vec3(11,5,0))))-0.4)), 
                (length(((qPnt - vec3(13,5,0))))-0.4)), (length(((qPnt - vec3(14,5,0))))-0.4)), (length(((qPnt - vec3(9,4,0))))-0.4)), 
                (length(((qPnt - vec3(10,4,0))))-0.4)), (length(((qPnt - vec3(11,4,0))))-0.4)), (length(((qPnt - vec3(12,4,0))))-0.4)), 
                (length(((qPnt - vec3(13,4,0))))-0.4)), (length(((qPnt - vec3(18,13,0))))-0.4)), (length(((qPnt - vec3(19,13,0))))-0.4)), 
                (length(((qPnt - vec3(20,13,0))))-0.4)), (length(((qPnt - vec3(21,13,0))))-0.4)), (length(((qPnt - vec3(22,13,0))))-0.4)), 
                (length(((qPnt - vec3(23,13,0))))-0.4)), (length(((qPnt - vec3(24,13,0))))-0.4)), (length(((qPnt - vec3(19,12,0))))-0.4)), 
                (length(((qPnt - vec3(20,12,0))))-0.4)), (length(((qPnt - vec3(23,12,0))))-0.4)), (length(((qPnt - vec3(24,12,0))))-0.4)), 
                (length(((qPnt - vec3(19,11,0))))-0.4)), (length(((qPnt - vec3(20,11,0))))-0.4)), (length(((qPnt - vec3(24,11,0))))-0.4)), 
                (length(((qPnt - vec3(19,10,0))))-0.4)), (length(((qPnt - vec3(20,10,0))))-0.4)), (length(((qPnt - vec3(22,10,0))))-0.4)), 
                (length(((qPnt - vec3(19,9,0))))-0.4)), (length(((qPnt - vec3(20,9,0))))-0.4)), (length(((qPnt - vec3(21,9,0))))-0.4)), 
                (length(((qPnt - vec3(22,9,0))))-0.4)), (length(((qPnt - vec3(19,8,0))))-0.4)), (length(((qPnt - vec3(20,8,0))))-0.4)), 
                (length(((qPnt - vec3(22,8,0))))-0.4)), (length(((qPnt - vec3(19,7,0))))-0.4)), (length(((qPnt - vec3(20,7,0))))-0.4)), 
                (length(((qPnt - vec3(19,6,0))))-0.4)), (length(((qPnt - vec3(20,6,0))))-0.4)), (length(((qPnt - vec3(19,5,0))))-0.4)), 
                (length(((qPnt - vec3(20,5,0))))-0.4)), (length(((qPnt - vec3(18,4,0))))-0.4)), (length(((qPnt - vec3(19,4,0))))-0.4)), 
                (length(((qPnt - vec3(20,4,0))))-0.4)), (length(((qPnt - vec3(21,4,0))))-0.4)), (length(((qPnt - vec3(27,8,0))))-0.4)), 
                (length(((qPnt - vec3(28,8,0))))-0.4)), (length(((qPnt - vec3(29,8,0))))-0.4)), (length(((qPnt - vec3(30,8,0))))-0.4)), 
                (length(((qPnt - vec3(31,8,0))))-0.4)), (length(((qPnt - vec3(32,8,0))))-0.4)), (length(((qPnt - vec3(33,8,0))))-0.4));
}

float t3SDF(vec3 qPnt) {
    return min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min
        (min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min
            ((length(((qPnt - vec3(3,13,0))))-0.4), (length(((qPnt - vec3(4,13,0))))-0.4)), (length(((qPnt - vec3(3,12,0))))-0.4)), 
            (length(((qPnt - vec3(4,12,0))))-0.4)), (length(((qPnt - vec3(2,10,0))))-0.4)), (length(((qPnt - vec3(3,10,0))))-0.4)), 
            (length(((qPnt - vec3(4,10,0))))-0.4)), (length(((qPnt - vec3(3,9,0))))-0.4)), (length(((qPnt - vec3(4,9,0))))-0.4)), 
            (length(((qPnt - vec3(3,8,0))))-0.4)), (length(((qPnt - vec3(4,8,0))))-0.4)), (length(((qPnt - vec3(3,7,0))))-0.4)), 
            (length(((qPnt - vec3(4,7,0))))-0.4)), (length(((qPnt - vec3(3,6,0))))-0.4)), (length(((qPnt - vec3(4,6,0))))-0.4)), 
            (length(((qPnt - vec3(3,5,0))))-0.4)), (length(((qPnt - vec3(4,5,0))))-0.4)), (length(((qPnt - vec3(2,4,0))))-0.4)), 
            (length(((qPnt - vec3(3,4,0))))-0.4)), (length(((qPnt - vec3(4,4,0))))-0.4)), (length(((qPnt - vec3(5,4,0))))-0.4)), 
            (length(((qPnt - vec3(10,13,0))))-0.4)), (length(((qPnt - vec3(11,13,0))))-0.4)), (length(((qPnt - vec3(12,13,0))))-0.4)), 
            (length(((qPnt - vec3(13,13,0))))-0.4)), (length(((qPnt - vec3(14,13,0))))-0.4)), (length(((qPnt - vec3(9,12,0))))-0.4)), 
            (length(((qPnt - vec3(10,12,0))))-0.4)), (length(((qPnt - vec3(14,12,0))))-0.4)), (length(((qPnt - vec3(15,12,0))))-0.4)), 
            (length(((qPnt - vec3(14,11,0))))-0.4)), (length(((qPnt - vec3(15,11,0))))-0.4)), (length(((qPnt - vec3(14,10,0))))-0.4)), 
            (length(((qPnt - vec3(15,10,0))))-0.4)), (length(((qPnt - vec3(11,9,0))))-0.4)), (length(((qPnt - vec3(12,9,0))))-0.4)), 
            (length(((qPnt - vec3(13,9,0))))-0.4)), (length(((qPnt - vec3(14,9,0))))-0.4)), (length(((qPnt - vec3(14,8,0))))-0.4)), 
            (length(((qPnt - vec3(15,8,0))))-0.4)), (length(((qPnt - vec3(14,7,0))))-0.4)), (length(((qPnt - vec3(15,7,0))))-0.4)), 
            (length(((qPnt - vec3(14,6,0))))-0.4)), (length(((qPnt - vec3(15,6,0))))-0.4)), (length(((qPnt - vec3(9,5,0))))-0.4)), 
            (length(((qPnt - vec3(10,5,0))))-0.4)), (length(((qPnt - vec3(14,5,0))))-0.4)), (length(((qPnt - vec3(15,5,0))))-0.4)), 
            (length(((qPnt - vec3(10,4,0))))-0.4)), (length(((qPnt - vec3(11,4,0))))-0.4)), (length(((qPnt - vec3(12,4,0))))-0.4)), 
            (length(((qPnt - vec3(13,4,0))))-0.4)), (length(((qPnt - vec3(14,4,0))))-0.4)), (length(((qPnt - vec3(18,8,0))))-0.4)), 
            (length(((qPnt - vec3(19,8,0))))-0.4)), (length(((qPnt - vec3(20,8,0))))-0.4)), (length(((qPnt - vec3(21,8,0))))-0.4)), 
            (length(((qPnt - vec3(22,8,0))))-0.4)), (length(((qPnt - vec3(23,8,0))))-0.4)), (length(((qPnt - vec3(24,8,0))))-0.4));
}

float t4SDF(vec3 qPnt) {
    return min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min
        (min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min
            (min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min
                (min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min
                    (min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min(min((length(((qPnt - vec3(0,13,0))))-0.4), 
                    (length(((qPnt - vec3(1,13,0))))-0.4)), (length(((qPnt - vec3(2,13,0))))-0.4)), (length(((qPnt - vec3(3,13,0))))-0.4)), 
                    (length(((qPnt - vec3(4,13,0))))-0.4)), (length(((qPnt - vec3(5,13,0))))-0.4)), (length(((qPnt - vec3(6,13,0))))-0.4)), 
                    (length(((qPnt - vec3(1,12,0))))-0.4)), (length(((qPnt - vec3(2,12,0))))-0.4)), (length(((qPnt - vec3(5,12,0))))-0.4)), 
                    (length(((qPnt - vec3(6,12,0))))-0.4)), (length(((qPnt - vec3(1,11,0))))-0.4)), (length(((qPnt - vec3(2,11,0))))-0.4)), 
                    (length(((qPnt - vec3(6,11,0))))-0.4)), (length(((qPnt - vec3(1,10,0))))-0.4)), (length(((qPnt - vec3(2,10,0))))-0.4)), 
                    (length(((qPnt - vec3(4,10,0))))-0.4)), (length(((qPnt - vec3(1,9,0))))-0.4)), (length(((qPnt - vec3(2,9,0))))-0.4)), 
                    (length(((qPnt - vec3(3,9,0))))-0.4)), (length(((qPnt - vec3(4,9,0))))-0.4)), (length(((qPnt - vec3(1,8,0))))-0.4)), 
                    (length(((qPnt - vec3(2,8,0))))-0.4)), (length(((qPnt - vec3(4,8,0))))-0.4)), (length(((qPnt - vec3(1,7,0))))-0.4)), 
                    (length(((qPnt - vec3(2,7,0))))-0.4)), (length(((qPnt - vec3(1,6,0))))-0.4)), (length(((qPnt - vec3(2,6,0))))-0.4)), 
                    (length(((qPnt - vec3(1,5,0))))-0.4)), (length(((qPnt - vec3(2,5,0))))-0.4)), (length(((qPnt - vec3(0,4,0))))-0.4)), 
                    (length(((qPnt - vec3(1,4,0))))-0.4)), (length(((qPnt - vec3(2,4,0))))-0.4)), (length(((qPnt - vec3(3,4,0))))-0.4)), 
                    (length(((qPnt - vec3(9,10,0))))-0.4)), (length(((qPnt - vec3(10,10,0))))-0.4)), (length(((qPnt - vec3(13,10,0))))-0.4)), 
                    (length(((qPnt - vec3(14,10,0))))-0.4)), (length(((qPnt - vec3(9,9,0))))-0.4)), (length(((qPnt - vec3(10,9,0))))-0.4)), 
                    (length(((qPnt - vec3(13,9,0))))-0.4)), (length(((qPnt - vec3(14,9,0))))-0.4)), (length(((qPnt - vec3(9,8,0))))-0.4)), 
                    (length(((qPnt - vec3(10,8,0))))-0.4)), (length(((qPnt - vec3(13,8,0))))-0.4)), (length(((qPnt - vec3(14,8,0))))-0.4)), 
                    (length(((qPnt - vec3(9,7,0))))-0.4)), (length(((qPnt - vec3(10,7,0))))-0.4)), (length(((qPnt - vec3(13,7,0))))-0.4)), 
                    (length(((qPnt - vec3(14,7,0))))-0.4)), (length(((qPnt - vec3(9,6,0))))-0.4)), (length(((qPnt - vec3(10,6,0))))-0.4)), 
                    (length(((qPnt - vec3(13,6,0))))-0.4)), (length(((qPnt - vec3(14,6,0))))-0.4)), (length(((qPnt - vec3(9,5,0))))-0.4)), 
                    (length(((qPnt - vec3(10,5,0))))-0.4)), (length(((qPnt - vec3(13,5,0))))-0.4)), (length(((qPnt - vec3(14,5,0))))-0.4)), 
                    (length(((qPnt - vec3(10,4,0))))-0.4)), (length(((qPnt - vec3(11,4,0))))-0.4)), (length(((qPnt - vec3(12,4,0))))-0.4)), 
                    (length(((qPnt - vec3(14,4,0))))-0.4)), (length(((qPnt - vec3(15,4,0))))-0.4)), (length(((qPnt - vec3(18,13,0))))-0.4)), 
                    (length(((qPnt - vec3(19,13,0))))-0.4)), (length(((qPnt - vec3(23,13,0))))-0.4)), (length(((qPnt - vec3(24,13,0))))-0.4)), 
                    (length(((qPnt - vec3(18,12,0))))-0.4)), (length(((qPnt - vec3(19,12,0))))-0.4)), (length(((qPnt - vec3(20,12,0))))-0.4)), 
                    (length(((qPnt - vec3(23,12,0))))-0.4)), (length(((qPnt - vec3(24,12,0))))-0.4)), (length(((qPnt - vec3(18,11,0))))-0.4)), 
                    (length(((qPnt - vec3(19,11,0))))-0.4)), (length(((qPnt - vec3(20,11,0))))-0.4)), (length(((qPnt - vec3(21,11,0))))-0.4)), 
                    (length(((qPnt - vec3(23,11,0))))-0.4)), (length(((qPnt - vec3(24,11,0))))-0.4)), (length(((qPnt - vec3(18,10,0))))-0.4)), 
                    (length(((qPnt - vec3(19,10,0))))-0.4)), (length(((qPnt - vec3(20,10,0))))-0.4)), (length(((qPnt - vec3(21,10,0))))-0.4)), 
                    (length(((qPnt - vec3(22,10,0))))-0.4)), (length(((qPnt - vec3(23,10,0))))-0.4)), (length(((qPnt - vec3(24,10,0))))-0.4)), 
                    (length(((qPnt - vec3(18,9,0))))-0.4)), (length(((qPnt - vec3(19,9,0))))-0.4)), (length(((qPnt - vec3(21,9,0))))-0.4)), 
                    (length(((qPnt - vec3(22,9,0))))-0.4)), (length(((qPnt - vec3(23,9,0))))-0.4)), (length(((qPnt - vec3(24,9,0))))-0.4)), 
                    (length(((qPnt - vec3(18,8,0))))-0.4)), (length(((qPnt - vec3(19,8,0))))-0.4)), (length(((qPnt - vec3(22,8,0))))-0.4)), 
                    (length(((qPnt - vec3(23,8,0))))-0.4)), (length(((qPnt - vec3(24,8,0))))-0.4)), (length(((qPnt - vec3(18,7,0))))-0.4)), 
                    (length(((qPnt - vec3(19,7,0))))-0.4)), (length(((qPnt - vec3(23,7,0))))-0.4)), (length(((qPnt - vec3(24,7,0))))-0.4)), 
                    (length(((qPnt - vec3(18,6,0))))-0.4)), (length(((qPnt - vec3(19,6,0))))-0.4)), (length(((qPnt - vec3(23,6,0))))-0.4)), 
                    (length(((qPnt - vec3(24,6,0))))-0.4)), (length(((qPnt - vec3(18,5,0))))-0.4)), (length(((qPnt - vec3(19,5,0))))-0.4)), 
                    (length(((qPnt - vec3(23,5,0))))-0.4)), (length(((qPnt - vec3(24,5,0))))-0.4)), (length(((qPnt - vec3(18,4,0))))-0.4)), 
                    (length(((qPnt - vec3(19,4,0))))-0.4)), (length(((qPnt - vec3(23,4,0))))-0.4)), (length(((qPnt - vec3(24,4,0))))-0.4)), 
                    (length(((qPnt - vec3(30,13,0))))-0.4)), (length(((qPnt - vec3(31,13,0))))-0.4)), (length(((qPnt - vec3(29,12,0))))-0.4)), 
                    (length(((qPnt - vec3(30,12,0))))-0.4)), (length(((qPnt - vec3(31,12,0))))-0.4)), (length(((qPnt - vec3(32,12,0))))-0.4)), 
                    (length(((qPnt - vec3(29,11,0))))-0.4)), (length(((qPnt - vec3(30,11,0))))-0.4)), (length(((qPnt - vec3(31,11,0))))-0.4)), 
                    (length(((qPnt - vec3(32,11,0))))-0.4)), (length(((qPnt - vec3(29,10,0))))-0.4)), (length(((qPnt - vec3(30,10,0))))-0.4)), 
                    (length(((qPnt - vec3(31,10,0))))-0.4)), (length(((qPnt - vec3(32,10,0))))-0.4)), (length(((qPnt - vec3(30,9,0))))-0.4)), 
                    (length(((qPnt - vec3(31,9,0))))-0.4)), (length(((qPnt - vec3(30,8,0))))-0.4)), (length(((qPnt - vec3(31,8,0))))-0.4)), 
                    (length(((qPnt - vec3(30,7,0))))-0.4)), (length(((qPnt - vec3(31,7,0))))-0.4)), (length(((qPnt - vec3(30,5,0))))-0.4)), 
                    (length(((qPnt - vec3(31,5,0))))-0.4)), (length(((qPnt - vec3(30,4,0))))-0.4)), (length(((qPnt - vec3(31,4,0))))-0.4)), 
                    (length(((qPnt - vec3(37,13,0))))-0.4)), (length(((qPnt - vec3(38,13,0))))-0.4)), (length(((qPnt - vec3(39,13,0))))-0.4)), 
                    (length(((qPnt - vec3(39,12,0))))-0.4)), (length(((qPnt - vec3(40,12,0))))-0.4)), (length(((qPnt - vec3(39,11,0))))-0.4)), 
                    (length(((qPnt - vec3(40,11,0))))-0.4)), (length(((qPnt - vec3(39,10,0))))-0.4)), (length(((qPnt - vec3(40,10,0))))-0.4)), 
                    (length(((qPnt - vec3(40,9,0))))-0.4)), (length(((qPnt - vec3(41,9,0))))-0.4)), (length(((qPnt - vec3(42,9,0))))-0.4)), 
                    (length(((qPnt - vec3(39,8,0))))-0.4)), (length(((qPnt - vec3(40,8,0))))-0.4)), (length(((qPnt - vec3(39,7,0))))-0.4)), 
                    (length(((qPnt - vec3(40,7,0))))-0.4)), (length(((qPnt - vec3(39,6,0))))-0.4)), (length(((qPnt - vec3(40,6,0))))-0.4)), 
                    (length(((qPnt - vec3(39,5,0))))-0.4)), (length(((qPnt - vec3(40,5,0))))-0.4)), (length(((qPnt - vec3(37,4,0))))-0.4)), 
                    (length(((qPnt - vec3(38,4,0))))-0.4)), (length(((qPnt - vec3(39,4,0))))-0.4));
}

float t5SDF(vec3 p, vec3 b, float r) {
  vec3 q = abs(p) - b;
  return length(max(q,0.0)) + min(max(q.x,max(q.y,q.z)),0.0) - r;
}

float sceneSDF(vec3 p, out vec3 pColor) {
    pColor = vec3(1.0, 1.0, 1.0);
    
    vec4 pH = mk_homo(p);
    vec4 pTO = mk_trans(35.0, -5.0, -20.0) * mk_scale(1.5, 1.5, 1.0) * pH;
    
    float t1 = t1SDF(pTO.xyz);
    float t2 = t2SDF((mk_trans(-45.0, 0.0, 0.0) * pTO).xyz);
    float t3 = t3SDF((mk_trans(-80.0, 0.0, 0.0) * pTO).xyz);
    float t4 = t4SDF((mk_trans(-106.0, 0.0, 0.0) * pTO).xyz);
    float t5 = t5SDF(p - vec3(36.0, 10.0, 15.0), vec3(30.0, 5.0, 5.0), 2.0);
    
    float tmin = min(min(min(min(t1, t2), t3), t4), t5);
    return tmin;
}

#define INTERSECT_MAX_ITER 75
#define INTERSECT_BISECT_THRESHOLD -0.3
#define INTERSECT_MAX_STEP 0.14
#define INTERSECT_T_BONUS_FACTOR 0.01
#define INTERSECT_HEIGHT_STEP_FACTOR 0.6
#define INTERSECT_BISECT_ITER 3
float intersectHeightMap(vec3 rayO, vec3 rayD, out float dist, out vec3 pColor) {
    vec3 curIsect = rayO;
    rayD = normalize(rayD);
    float t = 0.0, tPrev = 0.0, h = 0.0, hNew = 0.0;
    bool found = false;
    for (int i = 0; i < INTERSECT_MAX_ITER; i++) {
        h = elevation(rayO + t * rayD);
        if (h < INTERSECT_BISECT_THRESHOLD) {
            found = true;
            break;
        }
        
        float delta = max(INTERSECT_MAX_STEP, INTERSECT_HEIGHT_STEP_FACTOR * h) + 
                      (t * INTERSECT_T_BONUS_FACTOR);
        tPrev = t;
        t += delta;
    }
    
    if (found) {
        float tRefined = t, hRefined = h;
        hNew = h;
        vec2 tLH = vec2(tPrev, t);
        for (int j = 0; j < INTERSECT_BISECT_ITER; j++) {
            tRefined = dot(tLH, vec2(0.5));
            hNew = elevation(rayO + tRefined * rayD);
            tLH = mix(
                vec2(tLH.x, tRefined),
                vec2(tRefined, tLH.y),
                step(INTERSECT_BISECT_THRESHOLD, hNew)
            );
            hRefined = hNew;
        }
        
        // just an approx, never mind
        dist = max(hNew, RAYMARCH_SURF_DIST);
        pColor = colorMap(rayO + tRefined * rayD);
        return tRefined;
    }
    
    pColor = vec3(0.0);
    
    return t;
}

float rayMarchConservative(vec3 rayO, vec3 rayD, out float dist, out vec3 pColor) {
    vec3 curIsect = rayO;
    rayD = normalize(rayD);
    float t = 0.0;
    for (int i = 0; i < RAYMARCH_MAX_STEPS; i++) {
        dist = sceneSDF(curIsect, pColor);
        if (dist < RAYMARCH_SURF_DIST) {
            pColor = vec3(1.0);
            break;
        } else if (dist > RAYMARCH_MAX_DIST) {
            pColor = vec3(0.0);
            return t;
        }
        
        t += dist * RAYMARCH_CONSERVATIVE_FACTOR;
        curIsect = rayO + t * rayD;
    }
    return t;
}

float rayMarchHybrid(vec3 rayO, vec3 rayD, out float dist, out vec3 pColor, out bool isTerrain) {
    vec3 pColorMap = vec3(0.0), pColorSDF = vec3(0.0);
    float distHMap = 1e6, distSDF = 1e6;
    
    float tHMap = intersectHeightMap(rayO, rayD, distHMap, pColorMap);
    float tSDF = rayMarchConservative(rayO, rayD, distSDF, pColorSDF);
    
    if (tHMap < tSDF) {
        dist = distHMap;
        pColor = pColorMap;
        isTerrain = true;
        return tHMap;
    } else {
        dist = distSDF;
        pColor = pColorSDF;
        isTerrain = false;
        return tSDF;
    }
}


// grad f(x,y,z) = (df/dx, df/dy, df/dz)
// normal at (x_0, y_0, z_0) is normalized grad SDF(x,y,z)
//     evaluated at (x_0, y_0, z_0)
vec3 sceneNormal(vec3 p) {
    vec3 dummy = vec3(0.0, 0.0, 0.0);
    float pSDF = sceneSDF(p, dummy);
    vec2 eps = vec2(1e-2, 0);
    vec3 grad = pSDF - vec3(
        sceneSDF(p - eps.xyy, dummy),    // f(x_0 - eps.x, y_0, z_0)
        sceneSDF(p - eps.yxy, dummy),    // f(x_0, y_0 - eps.x, z_0)
        sceneSDF(p - eps.yyx, dummy)     // f(x_0, y_0, z_0 - eps.x)
    );
    
    // normalize does the rest
    return normalize(grad);
}

// TODO: numerical derivative
vec3 heightMapNormal(vec3 p) {
    vec2 eps = vec2(1e-1, 0);
    vec3 grad = elevation(p) - vec3(
        elevation(p - eps.xyy),    // f(x_0 - eps.x, y_0, z_0)
        elevation(p - eps.yxy),    // f(x_0, y_0 - eps.x, z_0)
        elevation(p - eps.yyx)     // f(x_0, y_0, z_0 - eps.x)
    );
    
    return normalize(grad);
}

vec3 shadeScene(vec3 isect, bool terrain) {
    // contrib from mainLight - point light
    vec3 lightPos = vec3(25.0, 10.0, -38.0);
    
    // test if the light can reach our ball
    vec3 light2Isect = normalize(isect - lightPos);
    vec3 objColor = vec3(0.0, 1.0, 0.0);
    bool dummy = false;

    float rayDist, lightT = rayMarchHybrid(lightPos, light2Isect, rayDist, objColor, dummy);
    float visibility = 0.0;
    if (length(lightPos + lightT * light2Isect - isect) < 10. * RAYMARCH_SURF_DIST) {
        // shall contribute light
        visibility = 1.0;
    }
    
    vec3 lightColor = vec3(0.5, 0.5, 0.5);
    vec3 lightL = lightColor * 40.5;
    
    vec3 isectN = terrain ? heightMapNormal(isect) : sceneNormal(isect);
    vec3 lightContrib = \
        visibility * clamp(dot(isectN, normalize(lightPos - isect)), 0., 1.) * lightL * objColor / length(isect - lightPos);
    
    return lightContrib;
}

vec3 shadeSkybox(vec3 rayD) {
    return vec3(0.0, 0.0, 0.0);
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    // Normalized pixel coordinates (from 0 to 1)
    vec2 uv = fragCoord/iResolution.xy;
    float aspectRatio = iResolution.x / iResolution.y;

    // Compute camera properties
    vec3 camPos = vec3(25.0, 5.0, -50.0);
    vec3 camLookat = vec3(25.0, 5.0, 1.0);
    vec3 camUp = vec3(1.0, 0.0, 0.0);
    vec3 camZ = normalize(camLookat - camPos);
    vec3 camX = normalize(cross(camZ, normalize(camUp)));
    vec3 camY = cross(camX, camZ);
    float camVertFOV = 120.0 * (PI / 180.0) / 2.;
    vec3 camScrC = camPos + camZ;
    vec3 camScrP = camScrC + camY * (uv.x -0.5) * tan(camVertFOV) + camX * (uv.y-0.5) * tan(camVertFOV) / aspectRatio;
    
    vec3 rayD = normalize(camScrP - camPos);
    vec3 rayO = camPos;
    vec3 dummy = vec3(0.0, 1.0, 0.0);
    bool isTerrain = false;
    float distClosest, tClosest = rayMarchHybrid(rayO, rayD, distClosest, dummy, isTerrain);
    
    vec3 outColor;
    if (distClosest > 10.0 * RAYMARCH_SURF_DIST) {
        outColor = shadeSkybox(rayD);
    } else {
        outColor = shadeScene(rayO + tClosest * rayD, isTerrain);
    }

    // Output to screen
    fragColor = vec4(outColor, 1.0);
}

void main() {
    mainImage(gl_FragColor, gl_FragCoord.xy);
}
`;