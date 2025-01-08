import uuid
from flask.views import MethodView
from flask_smorest import Blueprint
from celery.result import AsyncResult

from .schemas import TaskSchema, TaskResultSchema

blp = Blueprint("Tasks", __name__, description="Operations on tasks")


@blp.route("/task/add")
class AddTask(MethodView):
    @blp.arguments(TaskSchema)
    @blp.response(202, TaskResultSchema)
    def post(self, task_data):
        """Create a new add task"""
        from celery_blueprint.tasks import add

        task = add.apply_async(args=[task_data["x"], task_data["y"]])
        return {"task_id": task.id}, 202


@blp.route("/task/<string:task_id>")
class TaskStatus(MethodView):
    @blp.response(200, TaskResultSchema)
    def get(self, task_id):
        """Get the status of a task"""
        task_result = AsyncResult(task_id)
        result = {
            "task_id": task_id,
            "status": task_result.status,
            "result": task_result.result if task_result.ready() else None,
        }
        return result
