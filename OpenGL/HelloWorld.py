import numpy as np
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo
from OpenGLContext import testingcontext

BaseContext = testingcontext.getInteractive()


class TestContext(BaseContext):
    """Creates a simple vertex shader..."""

    def OnInit(self):
        vs_source = """
        #version 120
        varying vec4 vertex_color;
        uniform float end_fog;
        uniform vec4 fog_color;
        void main(){
            float fog;
            float fog_coord;
            // gl_Position = gl_ModelViewProjectionMatrix* gl_Vertex;
            gl_Position = ftransform();
            fog_coord = abs(gl_Position.z);
            fog_coord = clamp(fog_coord, 0.0, end_fog);
            fog = (end_fog - fog_coord)/end_fog;
            fog = clamp(fog,0.0,1.0);
            gl_FrontColor=mix(fog_color,gl_Color,fog);
            vertex_color = gl_Color;
        }
        """
        VERTEX_SHADER = shaders.compileShader(vs_source, GL_VERTEX_SHADER)
        fs_source = """
        #version 120
        varying vec4 vertex_color;
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
                    [0, 1, 0, 1, 0, 0],
                    [-1, -1, 0, 0, 1, 1],
                    [1, -1, 0, 0, 0, 1],

                    [2, -1, 0, 1, 1, 0],
                    [4, -1, 0, 1, 0, 1],
                    [4, 1, 0, 0, 1, 1],

                    [2, -1, 0, 1, 1, 0],
                    [4, 1, 0, 0, 1, 1],
                    [2, 1, 0, 1, 1, 1],
                ],
                'f'
            )
        )
        self.UNIFORM_LOCATIONS = {
            'end_fog': glGetUniformLocation(self.shader, 'end_fog'),
            'fog_color': glGetUniformLocation(self.shader, 'fog_color'),
        }
    def Render(self, mode):
        """Render the geometry for the scene."""
        shaders.glUseProgram(self.shader)
        glUniform1f(self.UNIFORM_LOCATIONS['end_fog'], 30)
        glUniform4f(self.UNIFORM_LOCATIONS['fog_color'], 1, 1, 1, 1)
        glScale(6, 6, 6)
        try:
            self.vbo.bind()
            try:
                glEnableClientState(GL_VERTEX_ARRAY)
                glEnableClientState(GL_COLOR_ARRAY)
                glVertexPointer(3, GL_FLOAT, 24, self.vbo)
                glColorPointer(3, GL_FLOAT, 24, self.vbo + 12)
                glDrawArrays(GL_TRIANGLES, 0, 9)
            finally:
                self.vbo.unbind()
                glDisableClientState(GL_VERTEX_ARRAY)
                glDisableClientState(GL_COLOR_ARRAY)
        finally:
            shaders.glUseProgram(0)


if __name__ == "__main__":
    TestContext.ContextMainLoop()
