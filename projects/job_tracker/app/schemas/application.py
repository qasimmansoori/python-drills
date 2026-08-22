from pydantic import BaseModel, Field


class JobApplicationBase(BaseModel):
    company: str = Field(min_length=2, max_length=50, description="Company name")
    role: str = Field(min_length=2, max_length=50, description="Job title or role")
    salary: int | None = Field(default=None, gt=0, description="Annual compensation in USD/INR")
    status: str = Field(default="Applied", description="Current status: Applied, Interviewing, Offer, Rejected")


class JobApplicationCreate(JobApplicationBase):
    pass


class JobApplicationResponse(JobApplicationBase):
    id: int
    created_at: str
