from cx_Freeze import setup, Executable

setup(
    name='Servidor',
    version='8000',
    url='',
    license='',
    author='Samuel',
    author_email='',
    description='Servidor IoT de sensores DHT22',
    executables = [Executable("Servidor.py")]
)
