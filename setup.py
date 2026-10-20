from setuptools import setup

setup(
    name = "uniflow",
    version = "1.1.0",
    description = "Auto-completing unicode text",
    
    author = "Saharsh Kaparthi, Bowen Li, Akhil Kora",
    py_modules = ['keyboardInput', 'shortcutDetection', 'deletingShortcut', 'writingValue', 'mathShortcuts', 'mathTyping', 'runner'],
    install_requires=['pynput>=1.7.6'],

    entry_points = {
        'console_scripts': [
            'uniflow=runner:main',
        ],
    },
)