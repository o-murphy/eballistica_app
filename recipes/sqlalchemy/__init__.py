from pythonforandroid.recipe import CompiledComponentsPythonRecipe


class SQLAlchemyRecipe(CompiledComponentsPythonRecipe):
    name = 'sqlalchemy'
    version = '2.0.0'
    url = 'https://pypi.python.org/packages/source/S/SQLAlchemy/SQLAlchemy-{version}.tar.gz'
    call_hostpython_via_targetpython = False

    depends = ['setuptools']

    # patches = ['zipsafe.patch']

recipe = SQLAlchemyRecipe()