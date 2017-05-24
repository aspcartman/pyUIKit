from ctypes import *

from pyglet.gl import *


class Shader:
    def __init__(self):
        super().__init__()
        self.handle = glCreateProgram()
        print(self.handle)
        self.create_shader(GL_VERTEX_SHADER, self.vertex_shader_source())
        self.create_shader(GL_FRAGMENT_SHADER, self.fragment_shader_source())
        self.link()

    def create_shader(self, type, source: str):
        if not source:
            return None
        shader = glCreateShader(type)
        count = 1
        src = (c_char_p * count)(*[source.encode('utf-8')])
        glShaderSource(shader, count, cast(pointer(src), POINTER(POINTER(c_char))), None)

        glCompileShader(shader)
        code = c_int(0)
        glGetShaderiv(shader, GL_COMPILE_STATUS, byref(code))
        if not code:
            glGetShaderiv(shader, GL_INFO_LOG_LENGTH, byref(code))
            buffer = create_string_buffer(code.value)
            glGetShaderInfoLog(shader, code, None, buffer)
            raise Exception(buffer.value)
        glAttachShader(self.handle, shader)

    def link(self):
        glLinkProgram(self.handle)
        code = c_int(0)
        glGetProgramiv(self.handle, GL_LINK_STATUS, byref(code))
        if not code:
            glGetProgramiv(self.handle, GL_INFO_LOG_LENGTH, byref(code))
            buffer = create_string_buffer(code.value)
            glGetProgramInfoLog(self.handle, code, None, buffer)
            raise Exception(buffer.value)

    def vertex_shader_source(self):
        pass

    def fragment_shader_source(self):
        pass

    def bind(self):
        # bind the program
        glUseProgram(self.handle)
        print('Shader enabled')

    def unbind(self):
        # unbind whatever program is currently bound - not necessarily this program,
        # so this should probably be a class method instead
        glUseProgram(0)
        print('Shader disabled')

    # upload a floating point uniform
    # this program must be currently bound
    def uniformf(self, name, vals):
        # check there are 1-4 values
        setUniform = [glUniform1f, glUniform2f, glUniform3f, glUniform4f][len(vals) - 1]
        uniform = glGetUniformLocation(self.handle, name.encode('utf-8'))
        if uniform == -1:
            raise Exception()
        data = (c_float * len(vals))(*vals)
        setUniform(uniform, *data)

    # upload an integer uniform
    # this program must be currently bound
    def uniformi(self, name, *vals):
        # check there are 1-4 values
        if len(vals) in range(1, 5):
            # select the correct function
            {1: glUniform1i,
             2: glUniform2i,
             3: glUniform3i,
             4: glUniform4i
             # retrieve the uniform location, and set
             }[len(vals)](glGetUniformLocation(self.handle, name.encode('utf-8')), *vals)


class SimpleShader(Shader):
    def __init__(self):
        super().__init__()
        self._color = None
        self._position = None

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, pos):
        self._position = pos
        self.uniformf('position', (pos.x, pos.y, 0, 0))

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self.uniformf('color', color.tuple())

    def vertex_shader_source(self):
        return '''
            uniform vec4 position;
            void main()
            {
                gl_Position = gl_ModelViewProjectionMatrix * (gl_Vertex + position);
            }
        '''

    def fragment_shader_source(self):
        return '''
            uniform vec4 color;
            void main (void)
            {
                gl_FragColor = color;
            }
        '''
