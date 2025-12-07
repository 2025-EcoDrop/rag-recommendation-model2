from sqlalchemy.orm import Session
from torch import Tensor
from app.database.models import DrugEmbedding, Drug, Review
import sqlalchemy as sa
import math
import os

IS_TEST = os.getenv("TEST_ENV") == "true"

if not IS_TEST:
    from sentence_transformers import SentenceTransformer

    # Snowflake를 Fine-tuning한 모델
    model = SentenceTransformer("dragonkue/snowflake-arctic-embed-l-v2.0-ko" , device="cpu")

async def embed_text(text: str) -> str | Tensor:
    if not IS_TEST:
        return model.encode(text)

    return "test"

async def search_embed_text(db: Session, squery: str, k: int = 20):
    if not IS_TEST:
        q_embed = await embed_text(squery)

        rows = (db.query(DrugEmbedding.id, DrugEmbedding.embedding)
                .order_by(DrugEmbedding.embedding.op("<->")(q_embed.tolist())) # L2 distance
                .limit(k)
                .all())

        return [row[0] for row in rows]

    return "test"

async def search_knowledge_base(db: Session, squery: str, user_id: int | None = None, k: int = 20):
    if not IS_TEST:
        results = await search_embed_text(db, squery, k)

        rows = (db.query(Drug.id, Drug.company_name, Drug.product_name, Drug.efficacy, Drug.use, Drug.caution_warn, Drug.caution, Drug.interaction, Drug.side_effect)
                .filter(Drug.id.in_(results))
                .order_by(
                    sa.case(
                        {id_: index for index, id_ in enumerate(results)},
                        value=Drug.id
                    )
                )
                .all())

        similarity_score_rows = [[(k - index) * 2, row] for index, row in enumerate(rows)]

        if user_id is not None:
            # review 중 product_name이 rows.product_name과 일치하고, rating >= 3~5, "public_date == True"인 경우(공공데이터를 사용한 경우)
            user_reviews = (db.query(Review.product_name, Review.rating)
                            .filter(
                                Review.author_id == user_id,
                                Review.rating >= 3,
                                Review.public_data.is_(True),
                                Review.product_name.in_([row.product_name for row in rows])
                            )
                            .all())

            if len(user_reviews) > 0:
                review_map = {prod_name: rating for prod_name, rating in user_reviews}

                # 점수 업데이트
                for i, item in enumerate(similarity_score_rows):
                    score, row = item  # row는 Drug 테이블 row 객체

                    # row.product_name이 user_reviews에 존재하면
                    if row.product_name in review_map:
                        rating = review_map[row.product_name]
                        similarity_score_rows[i][0] = score + math.ceil(rating)  # 점수에 올림한 rating 추가

        # 점수 기준 내림차순 정렬
        similarity_score_rows.sort(key=lambda x: x[0], reverse=True)

        return [row[1][1:3] for row in similarity_score_rows[:5]]

    return "test"