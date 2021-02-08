import numpy as np
from OpenGLContext import testingcontext
from OpenGLContext.scenegraph.basenodes import Sphere
BaseContext = testingcontext.getInteractive()
from OpenGL.GL import *
from OpenGL.arrays import vbo
from OpenGL.GL import shaders


class TestContext(BaseContext):
    """Demonstrates use of attribute types in GLSL
    """

    def OnInit(self):
        """Initialize the context"""
        materialStruct = """
        struct Material {
            vec4 ambient;
            vec4 diffuse;
            vec4 specular;
            float shininess;
        };
        """
        phong_weightCalc = """
        float phong_weightCalc(
            in vec3 light_pos, // light position
            in vec3 frag_normal // geometry normal
        ) {
            // returns vec2( ambientMult, diffuseMult )
            float n_dot_pos = max( 0.0, dot(
                frag_normal, light_pos
            ));
            return n_dot_pos;
        }
        """
        phong_weightCalc2 = """
        vec2 phong_weightCalc2(
            in vec3 light_pos, // light position
            in vec3 half_light, // half-way vector between light and view
            in vec3 frag_normal, // geometry normal
            in float shininess
        ) {
            // returns vec2( ambientMult, diffuseMult )
            float n_dot_pos = max( 0.0, dot(
                frag_normal, light_pos
            ));
            float n_dot_half = 0.0;
            if (n_dot_pos > -.05) {
                n_dot_half = pow(max(0.0,dot(
                    half_light, frag_normal
                )), shininess);
            }
            return vec2( n_dot_pos, n_dot_half);
        }
        """
        vertex = shaders.compileShader(
            phong_weightCalc +
            """
            uniform vec4 Global_ambient;
            uniform vec4 Light_ambient;
            uniform vec4 Light_diffuse;
            uniform vec3 Light_location;
            uniform vec4 Material_ambient;
            uniform vec4 Material_diffuse;
            
            attribute vec3 Vertex_position;
            attribute vec3 Vertex_normal;
            
            varying vec4 baseColor;
            varying vec4 baseColor_LightDiff;
            varying vec3 baseNormal;
            varying vec3 EC_Light_location;
            
            void main() {
                gl_Position = gl_ModelViewProjectionMatrix * vec4(
                    Vertex_position, 1.0
                );
                EC_Light_location = normalize(gl_NormalMatrix * Light_location);
                baseNormal = gl_NormalMatrix * normalize(Vertex_normal);
                float diffuse_weight = phong_weightCalc(
                    EC_Light_location,
                    // normalize(gl_NormalMatrix * Vertex_normal)
                    baseNormal
                );
                baseColor = (
                    (Global_ambient * Material_ambient) +
                    (Light_ambient * Material_ambient)
                );
                baseColor_LightDiff=(Light_diffuse * Material_diffuse * diffuse_weight);
            }
            """,
            GL_VERTEX_SHADER
        )
        # """
        # vec2 weights = phong_weightCalc(
        #     normalize(Light_location),
        #     normalize(Vertex_normal)
        # );"""
        fragment = shaders.compileShader(
            materialStruct +
            phong_weightCalc2 +
            """
            uniform vec4 Light_specular;
            uniform float Material_shininess;
            uniform vec4 Material_specular;
            
            varying vec4 baseColor;
            varying vec4 baseColor_LightDiff;
            varying vec3 baseNormal;
            varying vec3 EC_Light_location;
            
            void main() {
                vec3 Light_half = normalize(
                    EC_Light_location - vec3( 0,0,-1 )
                );
                vec2 weights = phong_weightCalc2(
                    EC_Light_location,
                    Light_half,
                    baseNormal,
                    Material_shininess
                );
                gl_FragColor = clamp(
                    (
                        baseColor +
                        baseColor_LightDiff * weights.x +
                        Light_specular * Material_specular * weights.y
                    ), 
                    0.0, 
                    1.0
                );
            }
            """,
            GL_FRAGMENT_SHADER
        )
        self.shader = shaders.compileProgram(vertex, fragment)
        self.coords, self.indices, self.count = Sphere(
            radius=10
        ).compile()
        # self.vbo = vbo.VBO(
        #     np.array(
        #         [
        #             [-1, 0, 0, -1, 0, 1],
        #             [0, 0, 1, -1, 0, 2],
        #             [0, 1, 1, -1, 0, 2],
        #             [-1, 0, 0, -1, 0, 1],
        #             [0, 1, 1, -1, 0, 2],
        #             [-1, 1, 0, -1, 0, 1],
        #             [0, 0, 1, -1, 0, 2],
        #             [1, 0, 1, 1, 0, 2],
        #             [1, 1, 1, 1, 0, 2],
        #             [0, 0, 1, -1, 0, 2],
        #             [1, 1, 1, 1, 0, 2],
        #             [0, 1, 1, -1, 0, 2],
        #             [1, 0, 1, 1, 0, 2],
        #             [2, 0, 0, 1, 0, 1],
        #             [2, 1, 0, 1, 0, 1],
        #             [1, 0, 1, 1, 0, 2],
        #             [2, 1, 0, 1, 0, 1],
        #             [1, 1, 1, 1, 0, 2],
        #         ],
        #         'f'
        #     )
        # )

        for uniform in (
            'Global_ambient',
            'Light_ambient',
            'Light_diffuse',
            'Light_location',
            'Light_specular',
            'Material_ambient',
            'Material_diffuse',
            'Material_shininess',
            'Material_specular'
        ):
            location = glGetUniformLocation(self.shader, uniform)
            if location in (None, -1):
                print('Warning, no uniform: %s' % uniform)
            setattr(self, uniform + '_loc', location)

        for attribute in (
                'Vertex_position',
                'Vertex_normal',
        ):
            location = glGetAttribLocation(self.shader, attribute)
            if location in (None, -1):
                print('Warning, no attribute: %s' % uniform)
            setattr(self, attribute + '_loc', location)

    def Render(self, mode=None):
        """Render the geometry for the scene."""
        BaseContext.Render(self, mode)
        glUseProgram(self.shader)
        try:
            # self.vbo.bind()
            self.coords.bind()
            self.indices.bind()
            try:
                glUniform4f(self.Global_ambient_loc, .3, .05, .05, .1)
                glUniform4f(self.Light_ambient_loc, .2, .2, .2, 1.0)
                glUniform4f(self.Light_diffuse_loc, 1, 1, 1, 1)
                glUniform3f(self.Light_location_loc, 2, 2, 10)
                glUniform4f(self.Light_specular_loc, 0.5, 0.0, 0.5, 1)
                glUniform4f(self.Material_ambient_loc, .2, 0.2, 0.2, 1.0)
                glUniform4f(self.Material_diffuse_loc, 1, 1, 1, 1)
                glUniform4f(self.Material_specular_loc, 1.0, 1.0, 1.0, 1.0)
                glUniform1f(self.Material_shininess_loc, .95)

                glEnableVertexAttribArray(self.Vertex_position_loc)
                glEnableVertexAttribArray(self.Vertex_normal_loc)

                stride = self.coords.data[0].nbytes
                # stride = 6 * 4
                glVertexAttribPointer(
                    self.Vertex_position_loc,
                    3, GL_FLOAT, False, stride, self.coords
                )
                glVertexAttribPointer(
                    self.Vertex_normal_loc,
                    3, GL_FLOAT, False, stride, self.coords + (5 * 4)
                )
                # glVertexAttribPointer(
                #     self.Vertex_position_loc,
                #     3, GL_FLOAT, False, stride, self.vbo
                # )
                # glVertexAttribPointer(
                #     self.Vertex_normal_loc,
                #     3, GL_FLOAT, False, stride, self.vbo + 12
                # )
                glDrawElements(
                    GL_TRIANGLES, self.count,
                    GL_UNSIGNED_SHORT, self.indices
                )
                # glDrawArrays(GL_TRIANGLES, 0, 18)
            finally:
                self.coords.unbind()
                self.indices.unbind()
                # self.vbo.unbind()
                glDisableVertexAttribArray(self.Vertex_position_loc)
                glDisableVertexAttribArray(self.Vertex_normal_loc)
        finally:
            glUseProgram(0)


if __name__ == "__main__":
    TestContext.ContextMainLoop()
