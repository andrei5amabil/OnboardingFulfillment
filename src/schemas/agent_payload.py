from typing import List, Optional, Literal
from pydantic import BaseModel, Field, model_validator

class PolicyCitation(BaseModel):
    rule_id: str = Field(..., description="Exact rule identifier (e.g., 'POL-SAAS-3.1')")
    document_name: str = Field(..., description="Source document name")
    quote: str = Field(..., description="Direct snippet justifying the decision")

class ProposedAction(BaseModel):
    action_type: Literal[
        "assign_license", 
        "allocate_asset", 
        "provision_account", 
        "revoke_license", 
        "reclaim_asset", 
        "flag_exception"
    ]
    target_id: str
    requires_approval: bool = False
    approval_reason: Optional[str] = None

    @model_validator(mode='after')
    def enforce_action_flags(self) -> 'ProposedAction':
        # Guarantee 1: flag_exception MUST require approval
        if self.action_type == "flag_exception" and not self.requires_approval:
            self.requires_approval = True
            
        # Guarantee 2: If approval is required, ensure a reason exists
        if self.requires_approval and not self.approval_reason:
            self.approval_reason = "System-enforced approval due to risk policies or stock deficits."
            
        return self

class OnboardingPlan(BaseModel):
    request_id: str
    employee_id: str
    risk_level: Literal["low", "medium", "high"]
    citations: List[PolicyCitation] = Field(default_factory=list)
    actions: List[ProposedAction] = Field(default_factory=list)
    hitl_required: bool
    summary: str

    @model_validator(mode='after')
    def enforce_global_security(self) -> 'OnboardingPlan':
        # Guarantee 3: If any action requires approval, HITL is mandatory globally
        if any(action.requires_approval for action in self.actions):
            self.hitl_required = True
            
        # Guarantee 4: High risk absolutely requires HITL
        if self.risk_level == "high":
            self.hitl_required = True
            
        # Guarantee 5: A plan requiring HITL cannot be classified as low risk
        if self.hitl_required and self.risk_level == "low":
            self.risk_level = "medium"
            
        return self
