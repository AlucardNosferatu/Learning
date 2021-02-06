from OpenGLContext import testingcontext
from OpenGLContext.arrays import *
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo

BaseContext = testingcontext.getInteractive()


class TestContext(BaseContext):
    """Creates a simple vertex shader..."""

    def OnInit(self):
        vs_source = """
        #version 120
        void main(){
            gl_Position = gl_ModelViewProjectionMatrix* gl_Vertex;
        }
        """
        VERTEX_SHADER = shaders.compileShader(vs_source, GL_VERTEX_SHADER)
        fs_source = """
        #version 120
        void main(){
            gl_FragColor=vec4(0,1,0,1);
        }
        """
        FRAGMENT_SHADER = shaders.compileShader(fs_source, GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(VERTEX_SHADER, FRAGMENT_SHADER)
        self.vbo = vbo.VBO(
            array(
                [
                    [0, 1, 0],
                    [-1, -1, 0],
                    [1, -1, 0],
                    [2, -1, 0],
                    [4, -1, 0],
                    [4, 1, 0],
                    [2, -1, 0],
                    [4, 1, 0],
                    [2, 1, 0],
                ],
                'f'
            )
        )

    def Render(self, mode):
        """Render the geometry for the scene."""
        shaders.glUseProgram(self.shader)
        try:
            self.vbo.bind()
            try:
                glEnableClientState(GL_VERTEX_ARRAY)
                glVertexPointerf(self.vbo)
                glDrawArrays(GL_TRIANGLES, 0, 9)
            finally:
                self.vbo.unbind()
                glDisableClientState(GL_VERTEX_ARRAY)
        finally:
            shaders.glUseProgram(0)


if __name__ == "__main__":
    TestContext.ContextMainLoop()
