"""ARENA-style tests for the HMM exercises.

Each ``test_<method>(HMM)`` takes the reader's ``HMM`` class (with the relevant
method monkeypatched on) and checks it against the reference implementation in
``solutions.py``, across the Z1R and Mess3 processes. Inputs to the
method-under-test are always built from the *reference*, so each test isolates a
single method. Prints "All tests passed!" on success; raises ``AssertionError``
(or surfaces an unexpected exception) otherwise.
"""

from itertools import product

import numpy as np

import processes
import solutions


def _fixtures():
    """(label, transition_tensor, initial_vect) cases covering 2- and 3-symbol processes."""
    return [
        ("Z1R", processes.z1r(0.5), processes.uniform_initial(3)),
        ("Mess3", processes.mess3(0.15, 0.2), processes.uniform_initial(3)),
    ]


def _all_seqs(n_obs, max_len=4):
    seqs = [()]
    for length in range(1, max_len + 1):
        seqs.extend(product(range(n_obs), repeat=length))
    return seqs


def _reachable_seqs(ref, n_obs, max_len=4):
    return [s for s in _all_seqs(n_obs, max_len)
            if ref.sequence_probability(list(s)) > 1e-12]


def _first_zero_prob_seq(ref, n_obs, max_len=4):
    for s in _all_seqs(n_obs, max_len):
        if s and np.isclose(ref.sequence_probability(list(s)), 0.0):
            return s
    raise RuntimeError("no zero-probability sequence found for this fixture")


# ----------------------------------------------------------------------------
# Part 1: sequence probabilities / next-token distributions
# ----------------------------------------------------------------------------

def test_validate(HMM):
    # well-formed processes must pass
    for label, tensor, init in _fixtures():
        HMM(tensor, init).validate()
    # each malformed case must raise AssertionError
    good_t, good_i = processes.z1r(0.5), processes.uniform_initial(3)
    neg_t = good_t.copy()
    neg_t[0, 2, 0] = -neg_t[0, 2, 0] - 0.1
    bad_cases = [
        ("non-row-stochastic transition matrix", good_t * 2.0, good_i),
        ("initial_vect that does not sum to 1", good_t, np.ones(3)),
        ("negative initial_vect", good_t, np.array([1.5, -0.5, 0.0])),
        ("negative transition_tensor entry", neg_t, good_i),
    ]
    for desc, tensor, init in bad_cases:
        try:
            HMM(tensor, init).validate()
        except AssertionError:
            pass
        else:
            raise AssertionError(f"validate() should have rejected: {desc}")
    print("All tests passed!")


def test_propagate(HMM):
    for label, tensor, init in _fixtures():
        ref, cand = solutions.HMM(tensor, init), HMM(tensor, init)
        n_obs = tensor.shape[0]
        for s in _all_seqs(n_obs):
            expected = ref._propagate(list(s))
            actual = cand._propagate(list(s))
            assert np.shape(actual) == np.shape(expected), (
                f"[{label}] _propagate{tuple(s)} has shape {np.shape(actual)}, "
                f"expected {np.shape(expected)}")
            assert np.allclose(actual, expected), (
                f"[{label}] _propagate{tuple(s)} = {actual}, expected {expected}")
        # passing an explicit `vect` should start from that vector, not the initial one
        custom = np.array([1.0, 0.0, 0.0])
        assert np.allclose(cand._propagate([0], vect=custom),
                           ref._propagate([0], vect=custom)), (
            f"[{label}] _propagate with explicit vect argument is incorrect")
    print("All tests passed!")


def test_sequence_probability(HMM):
    for label, tensor, init in _fixtures():
        ref, cand = solutions.HMM(tensor, init), HMM(tensor, init)
        n_obs = tensor.shape[0]
        for s in _all_seqs(n_obs):
            expected = ref.sequence_probability(list(s))
            actual = cand.sequence_probability(list(s))
            assert np.isclose(actual, expected), (
                f"[{label}] sequence_probability{tuple(s)} = {actual}, expected {expected}")
        # proper distribution: probabilities over all length-L sequences sum to 1
        for length in range(1, 5):
            total = sum(cand.sequence_probability(list(s))
                        for s in product(range(n_obs), repeat=length))
            assert np.isclose(total, 1.0), (
                f"[{label}] sum of P(length-{length} sequences) = {total}, expected 1")
    print("All tests passed!")


def test_conditional_next_token_probabilities(HMM):
    for label, tensor, init in _fixtures():
        ref, cand = solutions.HMM(tensor, init), HMM(tensor, init)
        n_obs = tensor.shape[0]
        for s in _reachable_seqs(ref, n_obs):
            expected = ref.conditional_next_token_probabilities(s)
            actual = cand.conditional_next_token_probabilities(s)
            assert np.allclose(actual, expected), (
                f"[{label}] conditional_next_token_probabilities{tuple(s)} = {actual}, "
                f"expected {expected}")
            assert np.isclose(np.sum(actual), 1.0), (
                f"[{label}] NTP{tuple(s)} sums to {np.sum(actual)}, expected 1")
    # a zero-probability sequence must raise ValueError (Z1R has unreachable sequences)
    tensor, init = processes.z1r(0.5), processes.uniform_initial(3)
    ref, cand = solutions.HMM(tensor, init), HMM(tensor, init)
    zero_seq = _first_zero_prob_seq(ref, 2)
    try:
        cand.conditional_next_token_probabilities(zero_seq)
    except ValueError:
        pass
    else:
        raise AssertionError(
            f"expected ValueError for zero-probability sequence {zero_seq}")
    print("All tests passed!")


def test_all_next_token_probabilities(HMM):
    for label, tensor, init in _fixtures():
        ref, cand = solutions.HMM(tensor, init), HMM(tensor, init)
        expected = ref.all_next_token_probabilities(4)
        actual = cand.all_next_token_probabilities(4)
        assert () in actual, f"[{label}] missing the empty-sequence () entry"
        assert set(actual) == set(expected), (
            f"[{label}] sequence key sets differ: "
            f"extra={set(actual) - set(expected)}, missing={set(expected) - set(actual)}")
        for k in expected:
            assert np.allclose(actual[k], expected[k]), (
                f"[{label}] all_next_token_probabilities[{k}] = {actual[k]}, "
                f"expected {expected[k]}")
    print("All tests passed!")


# ----------------------------------------------------------------------------
# Part 2: belief states
# ----------------------------------------------------------------------------

def test_belief_state(HMM):
    for label, tensor, init in _fixtures():
        ref, cand = solutions.HMM(tensor, init), HMM(tensor, init)
        n_obs = tensor.shape[0]
        for s in _reachable_seqs(ref, n_obs):
            expected = ref.belief_state(s)
            actual = cand.belief_state(s)
            assert np.allclose(actual, expected), (
                f"[{label}] belief_state{tuple(s)} = {actual}, expected {expected}")
            assert np.isclose(np.sum(actual), 1.0), (
                f"[{label}] belief_state{tuple(s)} sums to {np.sum(actual)}, expected 1")
    # a zero-probability sequence must raise ValueError
    tensor, init = processes.z1r(0.5), processes.uniform_initial(3)
    ref, cand = solutions.HMM(tensor, init), HMM(tensor, init)
    zero_seq = _first_zero_prob_seq(ref, 2)
    try:
        cand.belief_state(zero_seq)
    except ValueError:
        pass
    else:
        raise AssertionError(
            f"expected ValueError for zero-probability sequence {zero_seq}")
    print("All tests passed!")


def test_belief_update(HMM):
    for label, tensor, init in _fixtures():
        ref, cand = solutions.HMM(tensor, init), HMM(tensor, init)
        n_obs = tensor.shape[0]
        for s in _reachable_seqs(ref, n_obs, max_len=3):
            belief = ref.belief_state(s)
            reachable = ref.ntp_from_belief_state(belief)
            for obs in range(n_obs):
                if reachable[obs] <= 1e-12:
                    continue
                expected = ref.belief_update(belief, obs)
                actual = cand.belief_update(belief, obs)
                assert np.allclose(actual, expected), (
                    f"[{label}] belief_update(belief_state{tuple(s)}, {obs}) = {actual}, "
                    f"expected {expected}")
                assert np.isclose(np.sum(actual), 1.0), (
                    f"[{label}] belief_update result sums to {np.sum(actual)}, expected 1")
    # an impossible observation from a belief state must raise ValueError (Z1R)
    tensor, init = processes.z1r(0.5), processes.uniform_initial(3)
    ref, cand = solutions.HMM(tensor, init), HMM(tensor, init)
    found = False
    for s in _reachable_seqs(ref, 2, max_len=3):
        belief = ref.belief_state(s)
        reachable = ref.ntp_from_belief_state(belief)
        for obs in range(2):
            if reachable[obs] <= 1e-12:
                try:
                    cand.belief_update(belief, obs)
                except ValueError:
                    found = True
                else:
                    raise AssertionError(
                        f"expected ValueError for impossible observation {obs} "
                        f"from belief_state{tuple(s)}")
                break
        if found:
            break
    assert found, "could not find an impossible (belief, obs) pair to exercise the guard"
    print("All tests passed!")


def test_ntp_from_belief_state(HMM):
    for label, tensor, init in _fixtures():
        ref, cand = solutions.HMM(tensor, init), HMM(tensor, init)
        n_obs = tensor.shape[0]
        for s in _reachable_seqs(ref, n_obs):
            belief = ref.belief_state(s)
            expected = ref.ntp_from_belief_state(belief)
            actual = cand.ntp_from_belief_state(belief)
            assert np.allclose(actual, expected), (
                f"[{label}] ntp_from_belief_state(belief_state{tuple(s)}) = {actual}, "
                f"expected {expected}")
            assert np.isclose(np.sum(actual), 1.0), (
                f"[{label}] next-token distribution sums to {np.sum(actual)}, expected 1")
    print("All tests passed!")


def test_all_belief_states(HMM):
    for label, tensor, init in _fixtures():
        ref, cand = solutions.HMM(tensor, init), HMM(tensor, init)
        expected = ref.all_belief_states(4)
        actual = cand.all_belief_states(4)
        assert () in actual, f"[{label}] missing the empty-sequence () entry"
        assert set(actual) == set(expected), (
            f"[{label}] sequence key sets differ: "
            f"extra={set(actual) - set(expected)}, missing={set(expected) - set(actual)}")
        for k in expected:
            assert np.allclose(actual[k], expected[k]), (
                f"[{label}] all_belief_states[{k}] = {actual[k]}, expected {expected[k]}")
    print("All tests passed!")
