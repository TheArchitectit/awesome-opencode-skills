"""Pydantic models for MCP tool inputs and outputs."""

from pydantic import BaseModel, Field


class ListSkillsInput(BaseModel):
    """Input for listing skills."""
    category: str | None = Field(
        default=None,
        description="Filter by skill category (e.g., 'Development', 'Writing', 'Document Processing')"
    )
    depth: str | None = Field(
        default=None,
        description="Filter by depth (e.g., 'Comprehensive', 'Standard', 'Quick Reference')"
    )
    installed_only: bool = Field(
        default=False,
        description="Only show installed skills"
    )


class GetSkillInfoInput(BaseModel):
    """Input for getting skill information."""
    skill_name: str = Field(
        ...,
        description="Name of the skill to get information about"
    )


class InstallSkillInput(BaseModel):
    """Input for installing a skill."""
    skill_name: str = Field(
        ...,
        description="Name of the skill to install"
    )
    scope: str = Field(
        default="global",
        description="Installation scope: 'global' or 'project'"
    )


class UninstallSkillInput(BaseModel):
    """Input for uninstalling a skill."""
    skill_name: str = Field(
        ...,
        description="Name of the skill to uninstall"
    )
    scope: str = Field(
        default="global",
        description="Uninstallation scope: 'global' or 'project'"
    )


class SearchSkillsInput(BaseModel):
    """Input for searching skills."""
    query: str = Field(
        ...,
        description="Search query (keywords or description)"
    )


class ValidateSkillInput(BaseModel):
    """Input for validating a skill."""
    skill_path: str = Field(
        ...,
        description="Path to the skill directory to validate"
    )


class GetCombinationsInput(BaseModel):
    """Input for getting skill combinations."""
    category: str | None = Field(
        default=None,
        description="Filter by workflow category (e.g., 'Writing', 'Development', 'Business')"
    )


class InstallWorkflowInput(BaseModel):
    """Input for installing a workflow."""
    workflow_name: str = Field(
        ...,
        description="Name of the workflow to install (e.g., 'content-pipeline', 'product-launch', 'development-cycle')"
    )
    scope: str = Field(
        default="global",
        description="Installation scope: 'global' or 'project'"
    )
