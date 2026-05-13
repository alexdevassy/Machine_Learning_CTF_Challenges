import asyncio
import logging

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types.a2a_pb2 import Part, TaskState
from a2a.helpers import new_task_from_user_message

from agent_smith.llm import MatrixLLM

logger = logging.getLogger(__name__)


class SmithAgentExecutor(AgentExecutor):

    def __init__(self):
        self.llm = MatrixLLM()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        query = context.get_user_input() or "hello"

        task = context.current_task
        if not task:
            task = new_task_from_user_message(context.message)
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue, task.id, task.context_id)

        await updater.update_status(TaskState.TASK_STATE_WORKING)

        # Small delay for realism
        await asyncio.sleep(2)

        response_text = await asyncio.to_thread(self.llm.invoke, query)

        await updater.add_artifact(
            [Part(text=response_text)],
            name="smith_response",
        )
        await updater.complete()

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        pass
