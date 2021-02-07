import numpy as np
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo
from OpenGLContext import testingcontext
from OpenGLContext.events.timer import Timer

BaseContext = testingcontext.getInteractive()


class TestContext(BaseContext):
    """Creates a simple vertex shader..."""

    def OnInit(self):
        vs_source = """
        #version 120
        uniform float end_fog;
        uniform vec4 fog_color;
        
        uniform float tween;
        attribute vec3 position;
        attribute vec3 tweened;
        // attribute vec3 color;
        
        void main(){
            float fog;
            float fog_coord;
            // gl_Position = gl_ModelViewProjectionMatrix* gl_Vertex;
            // gl_Position = ftransform();
            gl_Position = gl_ModelViewProjectionMatrix * mix(
                vec4(position,1.0),
                vec4(tweened,1.0),
                tween
            );
            
            fog_coord = abs(gl_Position.z);
            fog_coord = clamp(fog_coord, 0.0, end_fog);
            fog = (end_fog - fog_coord)/end_fog;
            fog = clamp(fog,0.0,1.0);
            gl_FrontColor=mix(fog_color,gl_Color,fog);
        }
        """
        VERTEX_SHADER = shaders.compileShader(vs_source, GL_VERTEX_SHADER)
        fs_source = """
        #version 120
        void main(){
            // gl_FragColor=vec4(1,0,0,1);
            gl_FragColor = gl_Color;
        }
        """
        FRAGMENT_SHADER = shaders.compileShader(fs_source, GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(VERTEX_SHADER, FRAGMENT_SHADER)
        self.vbo = vbo.VBO(
            np.array(
                [
                    [0, 1, 0, 1, 3, 0, 1, 0, 0],
                    [-1, -1, 0, -1, -1, 0, 0, 1, 1],
                    [1, -1, 0, 1, -1, 0, 0, 0, 1],

                    [2, -1, 0, 2, -1, 0, 1, 1, 0],
                    [4, -1, 0, 4, -1, 0, 1, 0, 1],
                    [4, 1, 0, 4, 9, 0, 0, 1, 1],

                    [2, -1, 0, 2, -1, 0, 1, 1, 0],
                    [4, 1, 0, 1, 3, 0, 0, 1, 1],
                    [2, 1, 0, 1, -1, 0, 1, 1, 1],
                ],
                'f'
            )
        )
        self.UNIFORM_LOCATIONS = {
            'end_fog': glGetUniformLocation(self.shader, 'end_fog'),
            'fog_color': glGetUniformLocation(self.shader, 'fog_color'),
        }

        self.position_location = glGetAttribLocation(
            self.shader, 'position'
        )
        self.tweened_location = glGetAttribLocation(
            self.shader, 'tweened',
        )
        self.color_location = glGetAttribLocation(
            self.shader, 'color'
        )
        self.tween_location = glGetUniformLocation(
            self.shader, 'tween',
        )
        self.time = Timer(duration=40.0, repeating=30)
        self.time.addEventHandler("fraction", self.OnTimerFraction)
        self.time.register(self)
        self.time.start()

    def Render(self, mode):
        """Render the geometry for the scene."""
        shaders.glUseProgram(self.shader)
        glUniform1f(self.tween_location, self.tween_fraction)
        glUniform1f(self.UNIFORM_LOCATIONS['end_fog'], 20)
        glUniform4f(self.UNIFORM_LOCATIONS['fog_color'], 1, 1, 1, 1)
        glScale(6, 6, 6)
        try:
            self.vbo.bind()
            try:
                glEnableVertexAttribArray(self.position_location)
                glEnableVertexAttribArray(self.tweened_location)
                # glEnableVertexAttribArray(self.color_location)

                # glEnableClientState(GL_VERTEX_ARRAY)
                glEnableClientState(GL_COLOR_ARRAY)

                glVertexAttribPointer(
                    self.position_location,
                    3, GL_FLOAT, False, 36, self.vbo
                )
                glVertexAttribPointer(
                    self.tweened_location,
                    3, GL_FLOAT, False, 36, self.vbo + 12
                )
                # glVertexAttribPointer(
                #     self.color_location,
                #     3, GL_FLOAT, False, 36, self.vbo + 24
                # )

                # glVertexPointer(3, GL_FLOAT, 24, self.vbo)
                glColorPointer(3, GL_FLOAT, 36, self.vbo+24 )

                glDrawArrays(GL_TRIANGLES, 0, 9)
            finally:
                self.vbo.unbind()
                glDisableVertexAttribArray(self.position_location)
                glDisableVertexAttribArray(self.tweened_location)
                # glDisableVertexAttribArray(self.color_location)
                # glDisableClientState(GL_VERTEX_ARRAY)
                glDisableClientState(GL_COLOR_ARRAY)
        finally:
            shaders.glUseProgram(0)
        self.tween_fraction = 0.0

    def OnTimerFraction(self, event):
        frac = event.fraction()
        if frac > .5:
            frac = 1.0 - frac
        frac *= 2
        self.tween_fraction = frac
        self.triggerRedraw()


if __name__ == "__main__":
    TestContext.ContextMainLoop()
