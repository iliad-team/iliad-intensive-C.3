"""Reference HMM implementation for the exercises.

The exercise notebooks ask the reader to
reconstruct these methods; the tests in ``tests.py`` compare the reader's work
against this reference.
"""

import numpy as np
from collections.abc import Sequence

type TransitionTensor = np.ndarray  # (n_obs, n_states, n_states)
type StateVector = np.ndarray       # (n_states,) -- belief / propagated state vector
type TokenDist = np.ndarray         # (n_obs,)    -- distribution over next tokens


class HMM:
    """HMM defined by an observation-indexed transition tensor and an initial vector.

    Shapes
    ------
    transition_tensor        : (n_obs, n_states, n_states)
    belief / state vectors   : (n_states,)
    next-token distributions : (n_obs,)
    """

    def __init__(self, transition_tensor: TransitionTensor, initial_vect: StateVector) -> None:
        self.transition_tensor = np.asarray(transition_tensor)
        self.initial_vect = np.atleast_1d(np.asarray(initial_vect)).ravel()

    def validate(self) -> None:
        """Assert that transition_tensor and initial_vect define a valid HMM.

        The observation-summed state-transition matrix must be row-stochastic and
        the initial vector must be a probability distribution. Raises AssertionError
        otherwise.
        """
        assert (self.transition_tensor >= 0).all(), "transition_tensor must be non-negative"
        transition_matrix = self.transition_tensor.sum(axis=0)
        assert np.allclose(transition_matrix.sum(axis=1), 1.0), \
            "summed transition matrix must be row-stochastic (each row sums to 1)"
        assert (self.initial_vect >= 0).all(), "initial_vect must be non-negative"
        assert np.isclose(self.initial_vect.sum(), 1.0), "initial_vect must sum to 1"

    def _propagate(self, sequence: Sequence[int], vect: StateVector | None = None) -> StateVector:
        """Run a sequence through the tensor, returning the unnormalized state vector."""
        vect = self.initial_vect if vect is None else vect
        for obs in sequence:
            vect = np.einsum("i,ij->j", vect, self.transition_tensor[obs])
        return vect

    def sequence_probability(self, sequence: Sequence[int]) -> float:
        return np.sum(self._propagate(sequence))

    def conditional_next_token_probabilities(self, sequence: Sequence[int]) -> TokenDist:
        seq = list(sequence)
        p_seq = self.sequence_probability(seq)
        if np.allclose(p_seq, 0.0):
            raise ValueError(f"sequence {tuple(sequence)} has zero probability; "
                             "next-token distribution is undefined.")
        n_obs = self.transition_tensor.shape[0]
        joint = np.array([self.sequence_probability(seq + [k]) for k in range(n_obs)])
        return joint / p_seq

    def all_next_token_probabilities(self, max_depth: int) -> dict[tuple[int, ...], TokenDist]:
        """Next-token distribution for every reachable sequence of length 0..max_depth.

        Built breadth-first; a continuation is reachable iff its probability in the
        current distribution is nonzero (zero-probability branches are pruned).
        Uses conditional_next_token_probabilities directly -- no belief-state machinery.
        Includes () -> the prior next-token distribution.
        """
        prior = self.conditional_next_token_probabilities(())
        result = {(): prior}
        frontier = [((), prior)]
        for _ in range(max_depth):
            next_frontier = []
            for seq, ntp in frontier:
                for obs in range(len(ntp)):
                    if np.allclose(ntp[obs], 0.0):
                        continue  # zero-probability continuation -> prune
                    new_seq = seq + (obs,)
                    child = self.conditional_next_token_probabilities(new_seq)
                    result[new_seq] = child
                    next_frontier.append((new_seq, child))
            frontier = next_frontier
        return result

    #######################
    # Belief State Methods #
    #######################

    def belief_state(self, sequence: Sequence[int]) -> StateVector:
        vect = self._propagate(sequence)
        norm = np.sum(vect)
        if np.allclose(norm, 0.0):
            raise ValueError(f"sequence {tuple(sequence)} has zero probability; belief state is undefined.")
        return vect / norm

    def belief_update(self, belief_state: StateVector, obs: int) -> StateVector:
        update = np.einsum("i,ij->j", belief_state, self.transition_tensor[obs])
        norm = np.sum(update)
        if np.allclose(norm, 0.0):
            raise ValueError(f"observation {obs} has zero probability from this belief state; cannot update.")
        return update / norm

    def ntp_from_belief_state(self, belief_state: StateVector) -> TokenDist:
        return np.einsum("i,kij->k", belief_state, self.transition_tensor)

    def all_belief_states(self, max_depth: int) -> dict[tuple[int, ...], StateVector]:
        """Belief state for every reachable sequence of length 0..max_depth.

        Returns a dict mapping each observation sequence (as a tuple) to its
        belief state, starting from the empty sequence () -> prior belief.
        Built breadth-first via belief_update; zero-probability continuations
        are pruned (they have no defined belief state).
        """
        n_obs = self.transition_tensor.shape[0]
        prior = self.belief_state(())
        result = {(): prior}
        frontier = [((), prior)]
        for _ in range(max_depth):
            next_frontier = []
            for seq, belief in frontier:
                for obs in range(n_obs):
                    try:
                        updated = self.belief_update(belief, obs)
                    except ValueError:
                        continue  # zero-probability continuation -> prune
                    new_seq = seq + (obs,)
                    result[new_seq] = updated
                    next_frontier.append((new_seq, updated))
            frontier = next_frontier
        return result
