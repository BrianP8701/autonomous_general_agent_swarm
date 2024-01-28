import json
from pydantic import validate_arguments
import traceback

from aga_swarm.swarm.types import NodeOutput, SwarmID, SwarmCommand, LifecycleCommand, NodeOutput
from aga_swarm.swarm.oai_agent import OAI_Agent

def decompose_directive(directive: str, swarm_id: SwarmID) -> NodeOutput:
    with open('aga_swarm/actions/reasoning/decompose_directive/tool.json', 'r') as file:
        decompose_directive_blueprint = json.load(file)
    
    tools = decompose_directive_blueprint['decompose_directive']['tools']
    instructions = decompose_directive_blueprint['decompose_directive']['instructions']
    decompose_directive = OAI_Agent(instructions=instructions, tools=tools, tool_choice="break_down_directive", openai_key=swarm_id.configs.openai_key)
    
    try:
        subdirectives = decompose_directive.chat(directive)['subdirectives']
    except Exception as e:
        return NodeOutput(
            lifecycle_command=LifecycleCommand.NODE_FAILURE,
            swarm_commands=[],
            report=str(e) + "\nTraceback:\n" + traceback.format_exc()
        )

    swarm_commands = []
    for subdirective in subdirectives:
        swarm_command = SwarmCommand(
            action_id='aga_swarm/actions/swarm/action_router/action_router.py',
            params = {
                'directive': subdirective,
                'swarm_id': swarm_id
            }
        )
        swarm_commands.append(swarm_command)
    
    return NodeOutput(
        lifecycle_command=LifecycleCommand.SPAWN,
        swarm_commands=swarm_commands,
        report=f'Directive: {directive}\n\nSubdirectives:\n' + '\n'.join(subdirectives)
    )

@validate_arguments
def main(directive: str, swarm_id: SwarmID) -> NodeOutput:
    return decompose_directive(directive, swarm_id)