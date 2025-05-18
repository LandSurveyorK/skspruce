skspruce
========

|build| |wheels| |rtd| |pypi| |pyversions|

.. |build| image:: https://github.com/crflynn/skspruce/actions/workflows/build_and_test.yml/badge.svg
    :target: https://github.com/crflynn/skspruce/actions

.. |wheels| image:: https://github.com/crflynn/skspruce/actions/workflows/release.yml/badge.svg
    :target: https://github.com/crflynn/skspruce/actions

.. |rtd| image:: https://img.shields.io/readthedocs/skspruce.svg
    :target: http://skspruce.readthedocs.io/en/latest/

.. |pypi| image:: https://img.shields.io/pypi/v/skspruce.svg
    :target: https://pypi.python.org/pypi/skspruce

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/skspruce.svg
    :target: https://pypi.python.org/pypi/skspruce

``skspruce`` provides `scikit-learn <https://scikit-learn.org/stable/index.html>`__ compatible Python bindings to the C++ random forest implementation, `spruce <https://github.com/imbs-hl/spruce>`__, using `Cython <https://cython.readthedocs.io/en/latest/>`__.

The latest release of ``skspruce`` uses version `0.12.1 <https://github.com/imbs-hl/spruce/releases/tag/0.12.1>`__ of ``spruce``.


Installation
------------

``skspruce`` is available on `pypi <https://pypi.org/project/skspruce>`__ and can be installed via pip:

.. code-block:: bash

    pip install skspruce


Usage
-----

There are two ``sklearn`` compatible classes, ``spruceForestClassifier`` and ``spruceForestRegressor``. There is also the ``spruceForestSurvival`` class, which aims to be compatible with the `scikit-survival <https://github.com/sebp/scikit-survival>`__ API.


spruceForestClassifier
~~~~~~~~~~~~~~~~~~~~~~

The ``spruceForestClassifier`` predictor uses ``spruce``'s ForestProbability class to enable both ``predict`` and ``predict_proba`` methods.

.. code-block:: python

    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    from skspruce.ensemble import spruceForestClassifier

    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    rfc = spruceForestClassifier()
    rfc.fit(X_train, y_train)

    predictions = rfc.predict(X_test)
    print(predictions)
    # [1 2 0 0 0 0 1 2 1 1 2 2 2 1 1 0 1 1 0 1 1 1 0 2 1 0 0 1 2 2 0 1 2 2 0 2 0 0]

    probabilities = rfc.predict_proba(X_test)
    print(probabilities)
    # [[0.01333333 0.98666667 0.        ]
    #  [0.         0.         1.        ]
    #  ...
    #  [0.98746032 0.01253968 0.        ]
    #  [0.99       0.01       0.        ]]


spruceForestRegressor
~~~~~~~~~~~~~~~~~~~~~

The ``spruceForestRegressor`` predictor uses ``spruce``'s ForestRegression class. It also supports quantile regression using the ``predict_quantiles`` method.

.. code-block:: python

    from sklearn.datasets import load_boston
    from sklearn.model_selection import train_test_split
    from skspruce.ensemble import spruceForestRegressor

    X, y = load_boston(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    rfr = spruceForestRegressor()
    rfr.fit(X_train, y_train)

    predictions = rfr.predict(X_test)
    print(predictions)
    # [26.27401667  8.96549989 24.82981667 27.92506667 28.04606667 45.4693
    #  21.89681787 40.30345    11.53959613 19.13675    15.88567273 16.69713567
    #  ...
    #  20.29025364 26.21245833 23.79643333 14.03546362 21.24893333 34.8825
    #  21.22463333]

    # enable quantile regression on instantiation
    rfr = spruceForestRegressor(quantiles=True)
    rfr.fit(X_train, y_train)

    quantile_lower = rfr.predict_quantiles(X_test, quantiles=[0.1])
    print(quantile_lower)
    # [22.    5.   21.88 23.08 23.1  35.89 10.85 31.5   7.04 14.5  11.7  10.9
    #   8.1  28.38  7.2  19.6  29.1  13.1  24.94 21.09 15.6  11.7  10.41 14.5
    #  ...
    #  18.9  21.4   9.43  8.7  26.46 18.99  7.2  19.27 18.5  21.19 18.99 18.88
    #  14.07 21.87 22.18  9.43 17.28 29.6  18.2 ]
    quantile_upper = rfr.predict_quantiles(X_test, quantiles=[0.9])
    print(quantile_upper)
    # [30.83 12.85 29.01 33.1  33.1  50.   29.75 50.   15.   23.   19.96 21.4
    #  20.53 50.   13.35 25.   48.5  19.6  46.   26.6  23.7  20.1  17.8  21.4
    #  ...
    #  26.78 28.1  17.86 27.5  46.25 24.4  16.74 24.4  28.7  29.1  24.4  25.
    #  25.   31.51 28.   20.8  26.7  42.13 24.24]


spruceForestSurvival
~~~~~~~~~~~~~~~~~~~~

The ``spruceForestSurvival`` predictor uses ``spruce``'s ForestSurvival class, and has an interface similar to the RandomSurvivalForest found in the ``scikit-survival`` package.

.. code-block:: python

    from sksurv.datasets import load_veterans_lung_cancer
    from sklearn.model_selection import train_test_split
    from skspruce.ensemble import spruceForestSurvival

    X, y = load_veterans_lung_cancer()
    # select the numeric columns as features
    X = X[["Age_in_years", "Karnofsky_score", "Months_from_Diagnosis"]]
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    rfs = spruceForestSurvival()
    rfs.fit(X_train, y_train)

    predictions = rfs.predict(X_test)
    print(predictions)
    # [107.99634921  47.41235714  88.39933333  91.23566667  61.82104762
    #   61.15052381  90.29888492  47.88706349  21.25111508  85.5768254
    #   ...
    #   56.85498016  53.98227381  48.88464683  95.58649206  48.9142619
    #   57.68516667  71.96549206 101.79123016  58.95402381  98.36299206]

    chf = rfs.predict_cumulative_hazard_function(X_test)
    print(chf)
    # [[0.04233333 0.0605     0.24305556 ... 1.6216627  1.6216627  1.6216627 ]
    #  [0.00583333 0.00583333 0.00583333 ... 1.55410714 1.56410714 1.58410714]
    #  ...
    #  [0.12933333 0.14766667 0.14766667 ... 1.64342857 1.64342857 1.65342857]
    #  [0.00983333 0.0112619  0.04815079 ... 1.79304365 1.79304365 1.79304365]]

    survival = rfs.predict_survival_function(X_test)
    print(survival)
    # [[0.95855021 0.94129377 0.78422794 ... 0.19756993 0.19756993 0.19756993]
    #  [0.99418365 0.99418365 0.99418365 ... 0.21137803 0.20927478 0.20513086]
    #  ...
    #  [0.87868102 0.86271864 0.86271864 ... 0.19331611 0.19331611 0.19139258]
    #  [0.99021486 0.98880127 0.95299007 ... 0.16645277 0.16645277 0.16645277]]


License
-------

``skspruce`` is licensed under `GPLv3 <https://github.com/crflynn/skspruce/blob/master/LICENSE.txt>`__.

Development
-----------

To develop locally, it is recommended to have ``asdf``, ``make`` and a C++ compiler already installed. After cloning, run ``make setup``. This will setup the spruce submodule, install python and poetry from ``.tool-versions``, install dependencies using poetry, copy the spruce source code into skspruce, and then build and install skspruce in the local virtualenv.

To format code, run ``make fmt``. This will run isort and black against the .py files.

To run tests and inspect coverage, run ``make test``.

To rebuild in place after making changes, run ``make build``.

To create python package artifacts, run ``make dist``.

To build and view documentation, run ``make docs``.
