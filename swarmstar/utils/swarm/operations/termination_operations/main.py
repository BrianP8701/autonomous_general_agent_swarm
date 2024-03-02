from importlib import import_module
from typing import Union

from swarmstar.utils.swarm.swarmstar_space.swarm_state import get_node_from_swarm_state
from swarmstar.utils.swarm.swarmstar_space.swarm_history import add_event_to_swarm_history
from swarmstar.swarm.types import (
    SwarmConfig,
    TerminationOperation,
)


def terminate(
    swarm: SwarmConfig, termination_operation: TerminationOperation
) -> Union[TerminationOperation, None]:
    termination_policy_map = {
        "simple": "swarmstar.utils.swarm_utils.termination_operations.simple",
        "parallel_review": "swarmstar.utils.swarm_utils.termination_operations.parallel_review",
        "clone_with_questions_answered": "swarmstar.utils.swarm_utils.termination_operations.clone_with_questions_answered",
    }

    node_id = termination_operation.node_id
    node = get_node_from_swarm_state(swarm, node_id)
    termination_policy = node.termination_policy

    if termination_policy not in termination_policy_map:
        raise ValueError(
            f"Termination policy: `{termination_policy}` is not supported."
        )
    else:
        pass

    termination_policy_module = import_module(
        termination_policy_map[termination_policy]
    )

    output = termination_policy_module.terminate(swarm, termination_operation)
    add_event_to_swarm_history(swarm, termination_operation)

    return output