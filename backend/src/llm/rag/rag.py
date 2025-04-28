from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from litellm import embedding

from config import settings
from db.models import ResumeModelPublicWithDetails


class CollectionName:
    RESUME = "resume"
    EDUCATION = "education"
    EXPERIENCE = "experience"


class RagManager:
    def __init__(self, qdrant_db_url: str):
        self.qdrant_client = QdrantClient(qdrant_db_url)

    def init_collections(self):
        for collection in CollectionName.__dict__.values():
            if not self.qdrant_client.collection_exists(collection):
                self.qdrant_client.create_collection(
                    collection_name=collection,
                    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
                )

    def vectorize_and_insert(self, resume: ResumeModelPublicWithDetails):
        experience_vector = embedding(
            model=settings.OPENAI_EMBEDDING_MODEL,
            input=[str(experience) for experience in resume.experiences],
        )

        for experience, vector in zip(resume.experiences, experience_vector):
            self.qdrant_client.upsert(
                collection_name=CollectionName.EXPERIENCE,
                points=[experience.id],
                vectors=[vector],
                payload={"resume_id": resume.id},
            )

        for education in resume.educations:
            pass
