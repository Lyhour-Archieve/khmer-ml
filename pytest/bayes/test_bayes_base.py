import collections
import numpy as np
from decimal import Decimal
import pytest

import sys, os
syspath = '/Users/lion/Documents/py-workspare/openml/khmer-ml'
sys.path.append(syspath)
# sys.path.append(os.path.abspath(os.path.join('..', syspath)))

from khmerml.algorithms.bayes.bayes_base import BayesBase


def pytest_generate_tests(metafunc):
    # called once per each test function
    funcarglist = metafunc.cls.params[metafunc.function.__name__]
    argnames = sorted(funcarglist[0])

    print('funcarglist', metafunc.function.__name__)

    metafunc.parametrize(argnames, [[funcargs[name] for name in argnames]
            for funcargs in funcarglist])

class TestBayesBase(object):
  """
    BayesBase class is use for calculation in
    Naive Bayes Algorithm
  """

  CONFIG = {

  }

  sample_data = np.array(([5.1, 3.5, 1.4, 0.2, 1.0],
                        [4.9, 3.0, 1.4, 0.2, 1.0],
                        [4.7, 3.2, 1.3, 0.2, 1.0],
                        [5.2, 2.7, 3.9, 1.4, 2.0],
                        [5.0, 2.0, 3.5, 1.0, 2.0],
                        [5.9, 3.0, 4.2, 1.5, 2.0]))

  # test_data = np.array(([4.4, 3.0, 1.3, 0.2, 1.0],
  #                       [5.8, 2.7, 3.9, 1.2, 2.0]))

  test_vector = np.array(([4.4, 3.0, 1.3, 0.2, 1.0]))

  expected_train_model = {}
  expected_train_model[1.0] = [0.5, [0.47432024169184295, 0.3232628398791541, 0.15407854984894262, 0.04833836858006044]]
  expected_train_model[2.0] = [0.5, [0.394919168591224, 0.20092378752886833, 0.2909930715935335, 0.11316397228637413]]

  params = {
    'test_calculate_priori': [dict(X_train=sample_data), ],
    'test_calculate_likelihood': [dict(X_train=sample_data), ],
    'test_train': [dict(X_train=sample_data), ],
    'test_calculate_posteriori': [dict(model=expected_train_model, test_vector=test_vector), ],
  }


  def test_calculate_priori(self, X_train):
    """
      Calculate Priori Probability
    """

    # Count class occurences from X_train
    bayes_base = BayesBase(**self.CONFIG)
    # Output
    prioris = bayes_base.calculate_priori(X_train)

    # Expected prioris
    expected_prioris = {}
    expected_prioris[1.0] = 0.5
    expected_prioris[2.0] = 0.5

    # Compare the 2 dictionaries
    assert np.array_equal(prioris, expected_prioris)


  def test_calculate_likelihood(self, X_train):
    """
      Calculate likelihoods
    """

    # Count class occurences from X_train
    bayes_base = BayesBase(**self.CONFIG)
    # Output likelihood as dict(list)
    likelihoods = bayes_base.calculate_likelihood(X_train)

    # Expected likelihoods
    expected_likelihoods = {}
    expected_likelihoods[1.0] = [0.47432024169184295, 0.3232628398791541, 0.15407854984894262, 0.04833836858006044]
    expected_likelihoods[2.0] = [0.394919168591224, 0.20092378752886833, 0.2909930715935335, 0.11316397228637413]

    assert np.array_equal(likelihoods, expected_likelihoods)


  def test_train(self, X_train):
    """
      Train model
    """

    # Expected prioris
    prioris = {}
    prioris[1.0] = 0.5
    prioris[2.0] = 0.5

    # Expected liklihoods
    likelihoods = {}
    likelihoods[1.0] = [0.47432024169184295, 0.3232628398791541, 0.15407854984894262, 0.04833836858006044]
    likelihoods[2.0] = [0.394919168591224, 0.20092378752886833, 0.2909930715935335, 0.11316397228637413]

    train_model = {}
    for label, likelihood in likelihoods.items():

      # Get priori for corresponding class
      priori = prioris[label]
      if label not in train_model:
        train_model[label] = []

      # Push priori and likelihood of each label to stack
      train_model[label].append(priori)
      train_model[label].append(likelihood)

    expected_train_model = {}
    expected_train_model[1.0] = [0.5, [0.47432024169184295, 0.3232628398791541, 0.15407854984894262, 0.04833836858006044]]
    expected_train_model[2.0] = [0.5, [0.394919168591224, 0.20092378752886833, 0.2909930715935335, 0.11316397228637413]]

    assert np.array_equal(train_model, expected_train_model)


  def test_calculate_posteriori(self, model, test_vector):
    """
      Calculate the probability of all classes
      one class at a time.
    """

    # Count class occurences from X_train
    bayes_base = BayesBase(**self.CONFIG)
    # Output likelihood as dict(list)
    best_posteriori, best_label = bayes_base.calculate_posteriori(model, test_vector)

    # Expected best label and best posteriori
    expected_best_posteriori = Decimal('0.00003042817384543617539311613415')
    expected_best_label = 1.0

    assert best_posteriori == expected_best_posteriori
    assert expected_best_label == best_label
