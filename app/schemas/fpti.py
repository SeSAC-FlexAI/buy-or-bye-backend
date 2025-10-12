# app/schemas/fpti.py
from pydantic import BaseModel, ConfigDict, field_validator, field_serializer
from typing import Optional, Any, Dict

# 점수 묶음
class FptiScores(BaseModel):
    who_score: float
    when_score: float
    what_score: float
    how_score: float

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "who_score": 0.82,
            "when_score": 0.74,
            "what_score": 0.65,
            "how_score": 0.33,
        }
    })

class FptiBase(BaseModel):
    # 화면에 보이는 필드들
    title: Optional[str] = None                       # "전략적 효율 기획자(ENTJ)" 등 전체 타이틀
    type_code: Optional[str] = None                   # "ENTJ"
    type_alias: Optional[str] = None                  # "전략적 효율 기획자"
    type_name_en: Optional[str] = None                # "Event-Novelty-Tech-Judge"
    summary: Optional[str] = None                     # 요약 설명(프론트 설명 저장)
    who_text: Optional[str] = None                    # "모임 E" 같은 라벨
    when_text: Optional[str] = None                   # "가격이 좋을 때 N"
    what_text: Optional[str] = None                   # "감성 중심 F"
    how_text: Optional[str] = None                    # "즉흥적 소비 P"
    scores: Optional[FptiScores] = None               # 축별 점수

    # 내부 저장용(호환성 유지): 기존 answers/result 컬럼에 그대로 넣고 빼기
    #answers: Optional[str] = None   # 문자열로 고정
    result: Optional[Dict[str, Any]] = None

    # DB -> 응답 : result JSON을 펼쳐서 위 필드들에 채움
    @field_validator("type_code", mode="before")
    @classmethod
    def _fill_from_result(cls, v, info):
        data = info.data
        res = data.get("result") or {}
        if v is None:
            return res.get("type_code")
        return v

    @field_validator("type_alias", mode="before")
    @classmethod
    def _fill_alias(cls, v, info):
        res = (info.data.get("result") or {})
        return v if v is not None else res.get("type_alias")

    @field_validator("type_name_en", mode="before")
    @classmethod
    def _fill_name_en(cls, v, info):
        res = (info.data.get("result") or {})
        return v if v is not None else res.get("type_name_en")

    @field_validator("summary", mode="before")
    @classmethod
    def _fill_summary(cls, v, info):
        res = (info.data.get("result") or {})
        return v if v is not None else res.get("summary")

    @field_validator("who_text", mode="before")
    @classmethod
    def _fill_who_text(cls, v, info):
        res = (info.data.get("result") or {})
        return v if v is not None else res.get("who_text")

    @field_validator("when_text", mode="before")
    @classmethod
    def _fill_when_text(cls, v, info):
        res = (info.data.get("result") or {})
        return v if v is not None else res.get("when_text")

    @field_validator("what_text", mode="before")
    @classmethod
    def _fill_what_text(cls, v, info):
        res = (info.data.get("result") or {})
        return v if v is not None else res.get("what_text")

    @field_validator("how_text", mode="before")
    @classmethod
    def _fill_how_text(cls, v, info):
        res = (info.data.get("result") or {})
        return v if v is not None else res.get("how_text")

    @field_validator("scores", mode="before")
    @classmethod
    def _fill_scores(cls, v, info):
        if v is not None:
            return v
        res = (info.data.get("result") or {})
        s = res.get("scores")
        if isinstance(s, dict):
            return FptiScores(**s)
        return None

    # 요청 -> DB 저장 : 위의 단일 필드들을 다시 result JSON으로 합쳐서 저장
    @field_serializer("result")
    def _compose_result(self, result: Optional[Dict[str, Any]], _info):
        if result:
            return result
        out = {
            "type_code": self.type_code,
            "type_alias": self.type_alias,
            "type_name_en": self.type_name_en,
            "summary": self.summary,
            "who_text": self.who_text,
            "when_text": self.when_text,
            "what_text": self.what_text,
            "how_text": self.how_text,
            "scores": (
                self.scores.model_dump() if isinstance(self.scores, BaseModel) else self.scores
            ),
        }
        return out

class FptiCreate(FptiBase):
    # 게스트 가능, 필수 없음
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "title": "전략적 효율 기획자(ENTJ)",
            "type_code": "ENTJ",
            "type_alias": "전략적 효율 기획자",
            "type_name_en": "Event-Novelty-Tech-Judge",
            "summary": "소비에도 전략이 필요합니다. 이 지표는 ... '성공 지향형' 소비자입니다.",
            "who_text": "모임 E",
            "when_text": "가격이 좋을 때 N",
            "what_text": "감성 중심 F",
            "how_text": "즉흥적 소비 P",
            "scores": {
                "who_score": 0.82,
                "when_score": 0.74,
                "what_score": 0.65,
                "how_score": 0.33
            }
            # answers/result 는 요청에서 굳이 보낼 필요 없으면 생략 가능
        }
    })

class FptiUpdate(BaseModel):
    title: Optional[str] = None
    type_code: Optional[str] = None
    type_alias: Optional[str] = None
    type_name_en: Optional[str] = None
    summary: Optional[str] = None
    who_text: Optional[str] = None
    when_text: Optional[str] = None
    what_text: Optional[str] = None
    how_text: Optional[str] = None
    scores: Optional[FptiScores] = None
    # 호환용
    # answers: Optional[Any] = None
    result: Optional[Dict[str, Any]] = None

class FptiOut(FptiBase):
    id: int
    post_id: str
    user_id: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "post_id": "7f2a7c9d-3a5e-4d2b-8e8a-1234567890ab",
                "user_id": 1,
                "title": "전략적 효율 기획자(ENTJ)",
                "type_code": "ENTJ",
                "type_alias": "전략적 효율 기획자",
                "type_name_en": "Event-Novelty-Tech-Judge",
                "summary": "소비에도 전략이 필요합니다. ...",
                "who_text": "모임 E",
                "when_text": "가격이 좋을 때 N",
                "what_text": "감성 중심 F",
                "how_text": "즉흥적 소비 P",
                "scores": {
                    "who_score": 0.82,
                    "when_score": 0.74,
                    "what_score": 0.65,
                    "how_score": 0.33
                }
            }
        }
    )
