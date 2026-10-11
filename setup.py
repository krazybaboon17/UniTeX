from setuptools import setup

setup(
    name = "unitex",
    version = "1.0.1",
    description = "Auto-completing unicode text",
    
    author = "Saharsh Kaparthi, Bowen Li, Akhil Kora",
    py_modules = ['keyboardInput', 'shortcutDetection', 'deletingShortcut', 'writingValue', 'mathShortcuts', 'mathTyping', 'runner'],
    install_requires=['keyboard', 'pynput'],

    entry_points = {
        'console_scripts': [
            'unitex=runner:main',
        ],
    },
)