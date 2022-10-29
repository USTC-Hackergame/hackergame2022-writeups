"use strict";

// Some of the code are derived from https://webglfundamentals.org/webgl/lessons/webgl-shadertoy.html
// which is licensed under MIT License.

function main(vsSource, fsSource) {
  // Get A WebGL context
  /** @type {HTMLCanvasElement} */
  const canvas = document.querySelector("#canvas");
  const gl = canvas.getContext("webgl");
  if (!gl) {
    return;
  }

  // setup GLSL program
  const program = webglUtils.createProgramFromSources(gl, [vsSource, fsSource]);

  // look up where the vertex data needs to go.
  const positionAttributeLocation = gl.getAttribLocation(program, "a_position");

  // look up uniform locations
  const resolutionLocation = gl.getUniformLocation(program, "iResolution");
  const mouseLocation = gl.getUniformLocation(program, "iMouse");
  const timeLocation = gl.getUniformLocation(program, "iTime");

  // Create a buffer to put three 2d clip space points in
  const positionBuffer = gl.createBuffer();

  // Bind it to ARRAY_BUFFER (think of it as ARRAY_BUFFER = positionBuffer)
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);

  // fill it with a 2 triangles that cover clipspace
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
    -1, -1,  // first triangle
     1, -1,
    -1,  1,
    -1,  1,  // second triangle
     1, -1,
     1,  1,
  ]), gl.STATIC_DRAW);

  const inputElem = document.querySelector('.divcanvas');

  const playResetButton = document.getElementById('playResetButton');
  const playPauseButton = document.getElementById('playPauseButton');
  const playerTimeSpan = document.getElementById('playerTime');
  const playerFramerateSpan = document.getElementById('playerFramerate');
  const playerResolutionSpan = document.getElementById('playerResolution');
  const playerStatusSpan = document.getElementById('playerStatus');

  playResetButton.addEventListener('click', resetTime);
  playPauseButton.addEventListener('click', togglePlayPauseState);

  let isPlaying = false;
  function togglePlayPauseState() {
    isPlaying = !isPlaying;
    if (isPlaying) {
      playPauseButton.innerHTML = "PAUSE";
      requestFrame();
    } else {
      playPauseButton.innerHTML = "PLAY";
      cancelFrame();
    }
  }


  let mouseX = 0;
  let mouseY = 0;

  function setMousePosition(e) {
    const rect = inputElem.getBoundingClientRect();
    mouseX = e.clientX - rect.left;
    mouseY = rect.height - (e.clientY - rect.top) - 1;  // bottom is 0 in WebGL
  }

  inputElem.addEventListener('mousemove', setMousePosition);
  inputElem.addEventListener('touchmove', (e) => {
    e.preventDefault();
    setMousePosition(e.touches[0]);
  }, {passive: false});

  let requestId;
  function requestFrame() {
    if (!requestId) {
      requestId = requestAnimationFrame(render);
    }
  }
  function cancelFrame() {
    if (requestId) {
      cancelAnimationFrame(requestId);
      requestId = undefined;
    }
  }

  let then = 0;
  let time = 0;
  // Previous status update time
  let prevUpdateTime = 0;
  // Cumulative frome rendered for this period
  let cumuFrameRendered = 0;

  function resetTime() {
    time = 0;
    prevUpdateTime = 0;
  }

  function render(now) {
    requestId = undefined;
    now *= 0.001;  // convert to seconds
    const elapsedTime = Math.min(now - then, 0.1);
    time += elapsedTime;
    then = now;

    cumuFrameRendered += 1;
    // update player status bar
    if (time - prevUpdateTime > 0.1) {
      playerTimeSpan.innerHTML = time.toFixed(2) + " sec";
      playerFramerateSpan.innerHTML = (cumuFrameRendered / (time - prevUpdateTime)).toFixed(2) + " FPS";
      playerResolutionSpan.innerHTML = gl.canvas.width.toString() + " x " + gl.canvas.height.toString();
      prevUpdateTime = time;
      cumuFrameRendered = 0;
    }

    webglUtils.resizeCanvasToDisplaySize(gl.canvas);

    // Tell WebGL how to convert from clip space to pixels
    gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);

    // Tell it to use our program (pair of shaders)
    gl.useProgram(program);
    playerStatusSpan.innerHTML = "Program: Initialized";

    // Turn on the attribute
    gl.enableVertexAttribArray(positionAttributeLocation);

    // Bind the position buffer.
    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);

    // Tell the attribute how to get data out of positionBuffer (ARRAY_BUFFER)
    gl.vertexAttribPointer(
        positionAttributeLocation,
        2,          // 2 components per iteration
        gl.FLOAT,   // the data is 32bit floats
        false,      // don't normalize the data
        0,          // 0 = move forward size * sizeof(type) each iteration to get the next position
        0,          // start at the beginning of the buffer
    );

    gl.uniform2f(resolutionLocation, gl.canvas.width, gl.canvas.height);
    gl.uniform2f(mouseLocation, mouseX, mouseY);
    gl.uniform1f(timeLocation, time);

    gl.drawArrays(
        gl.TRIANGLES,
        0,     // offset
        6,     // num vertices to process
    );

    requestFrame();
  }

  requestFrame();
  requestAnimationFrame(cancelFrame);
}

window.onload = function () {
  const playerStatusSpan = document.getElementById('playerStatus');
  playerStatusSpan.innerHTML = "Program: Initializing...";

  const canvasObj = document.getElementById('canvas');

  canvasObj.addEventListener("webglcontextlost", (e) => {
    const playerStatusSpan = document.getElementById('playerStatus');
    const extraInfoSpan = document.getElementById('extraInfo');
    playerStatusSpan.innerHTML = "Program: Context Lost";

    extraInfoSpan.innerHTML = "Your WebGL context has lost. This might've been caused by a browser or driver bug, and we recommend you to try again with another browser or graphics driver installed.";
  });

  setTimeout(function () {
    main(window.vertexShader, window.fragmentShader);
  }, 100);
  
}
