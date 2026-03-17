"""Global job status routes."""

from flask import current_app
from flask_restx import Resource
from server.swagger import ns_jobs
from server.models import api_response, job_data
from helpers.response_helper import ResponseHelper


@ns_jobs.route("/<string:job_id>")
@ns_jobs.param("job_id", "The job identifier")
class JobResource(Resource):
    """Job status resource."""

    @ns_jobs.doc("get_job_status")
    @ns_jobs.response(200, "Success", api_response)
    @ns_jobs.response(404, "Job not found")
    def get(self, job_id: str):
        """Get job status by ID."""
        queue_service = current_app.config["queue_service"]

        job = queue_service.get_job(job_id)
        if job is None:
            return ResponseHelper.error(message="Job not found", status_code=404)

        return ResponseHelper.success(data=job.to_dict())
