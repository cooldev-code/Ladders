from app.config import FEEDS_DIR
from app.pipeline import JobPipeline
from app.storage.repository import ApprovedJobRepository, RejectionLogger


EXPECTED_APPROVED_TITLES = {
    "Backend Engineer",
    "Machine Learning Engineer",
    "Agile Project Lead",
    "Senior Software Engineer",
    "Data Scientist",
    "QA Automation Engineer",
    "UX Designer",
    "Product Analyst",
    "Cybersecurity Specialist",
    "Growth Marketing Manager",
    "Customer Success Manager",
}


def test_full_pipeline_on_sample_feed(tmp_path):
    repo = ApprovedJobRepository()
    logger = RejectionLogger(tmp_path / "rejected.jsonl")
    pipeline = JobPipeline(repo, logger, feeds_dir=FEEDS_DIR)

    result = pipeline.run()

    assert len(result.ingestion.jobs) == 20
    assert len(result.ingestion.errors) == 0
    assert len(result.approved) == 11
    assert len(result.rejected) == 9

    approved_titles = {job.title for job in result.approved}
    assert approved_titles == EXPECTED_APPROVED_TITLES
